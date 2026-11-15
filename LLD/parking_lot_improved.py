"""
===============================================================================
PARKING LOT - IMPROVED VERSION
===============================================================================
What changed compared to your original (and why):

BUG FIXES
  1. One RLock for the whole lot -> no double booking, no exit races.
  2. park() result is now checked.
  3. exit uses dict.pop() under the lock -> a ticket can only be closed once.
  4. Typo active_vechicles -> active_vehicles.
  5. print() removed from business logic; exceptions and return values instead.
  6. exit_time < entry_time is rejected.

NEW FEATURES
  - PricingStrategy (Strategy) + PeakHourPricing (Decorator)
  - PaymentMethod (Strategy): Cash / Card / UPI, ticket status ACTIVE->PAID->CLOSED
  - SlotStatus enum (FREE / OCCUPIED / RESERVED / MAINTENANCE)
  - Observer: DisplayBoard shows free slots per floor
  - Lost ticket flow (lookup by vehicle number + penalty)
  - Custom exceptions
  - Gate (entry / exit points)
  - Vehicle compatibility map instead of hardcoded if/else
  - Strategies prefer an exact slot type (EV -> EV slot before CAR slot)
  - Singleton-style accessor and a Factory to build a lot from config

PATTERNS: Strategy (parking, pricing, payment), Decorator (peak pricing),
          Observer (display board), Factory (lot builder), Singleton (optional),
          Dependency Injection, Composition, Facade (ParkingLot).
SOLID:    S, O, L, D all followed (see comments on each class).
===============================================================================
"""

from abc import ABC, abstractmethod
from enum import Enum
from datetime import datetime, timedelta
import threading
import uuid
import math


# ----------------------------------------------------------------------------
# Exceptions: callers can tell "full" from "invalid ticket" from "duplicate".
# ----------------------------------------------------------------------------
class ParkingError(Exception):
    pass

class ParkingFullError(ParkingError):
    pass

class VehicleAlreadyParkedError(ParkingError):
    pass

class InvalidTicketError(ParkingError):
    pass

class PaymentFailedError(ParkingError):
    pass


# ----------------------------------------------------------------------------
# Enums
# ----------------------------------------------------------------------------
class VehicleType(Enum):
    CAR = 1
    BIKE = 2
    ELECTRIC_CAR = 3

class SlotStatus(Enum):
    FREE = 1
    OCCUPIED = 2
    RESERVED = 3
    MAINTENANCE = 4

class TicketStatus(Enum):
    ACTIVE = 1
    PAID = 2
    CLOSED = 3


# ----------------------------------------------------------------------------
# Vehicle
# ----------------------------------------------------------------------------
class Vehicle:
    def __init__(self, number, vehicle_type):
        if not number or not str(number).strip():
            raise ValueError("Vehicle number is required")
        if not isinstance(vehicle_type, VehicleType):
            raise TypeError("vehicle_type must be VehicleType")
        self.number = str(number).strip().upper()   # normalise "ka01" == "KA01"
        self.vehicle_type = vehicle_type


# ----------------------------------------------------------------------------
# Slot
# ----------------------------------------------------------------------------
class ParkingSlot:
    # Compatibility map replaces the hardcoded if/else in can_fit().
    # Open/Closed: add TRUCK or HANDICAPPED by editing data, not logic.
    COMPATIBLE = {
        VehicleType.BIKE: {VehicleType.BIKE},
        VehicleType.CAR: {VehicleType.CAR},
        VehicleType.ELECTRIC_CAR: {VehicleType.ELECTRIC_CAR, VehicleType.CAR},
    }

    def __init__(self, slot_number, slot_type, distance):
        if not isinstance(slot_type, VehicleType):
            raise TypeError("slot_type must be VehicleType")
        self.slot_number = slot_number
        self.slot_type = slot_type
        self.distance = distance        # distance from the main entrance
        self.floor_number = None        # set by ParkingFloor (single source of truth)
        self._status = SlotStatus.FREE

    @property
    def status(self):
        return self._status

    def is_free(self):
        return self._status == SlotStatus.FREE

    def can_fit(self, vehicle_type):
        return self.slot_type in self.COMPATIBLE[vehicle_type]

    def is_exact_match(self, vehicle_type):
        return self.slot_type == vehicle_type

    # NOTE: slot methods are NOT locked individually. ParkingLot holds the lot
    # lock around every state change, so the slot stays simple.
    def park(self):
        if self._status != SlotStatus.FREE:
            return False
        self._status = SlotStatus.OCCUPIED
        return True

    def free(self):
        if self._status != SlotStatus.OCCUPIED:
            return False
        self._status = SlotStatus.FREE
        return True

    def set_maintenance(self):
        if self._status == SlotStatus.OCCUPIED:
            return False
        self._status = SlotStatus.MAINTENANCE
        return True

    def reserve(self):
        if self._status != SlotStatus.FREE:
            return False
        self._status = SlotStatus.RESERVED
        return True

    def restore(self):
        """Back to FREE from MAINTENANCE or RESERVED."""
        if self._status in (SlotStatus.MAINTENANCE, SlotStatus.RESERVED):
            self._status = SlotStatus.FREE
            return True
        return False


# ----------------------------------------------------------------------------
# Floor
# ----------------------------------------------------------------------------
class ParkingFloor:
    def __init__(self, floor_no, spots):
        self.floor_no = floor_no
        self.spots = spots
        for s in spots:
            s.floor_number = floor_no

    def available_slots(self, vehicle_type=None):
        return [
            s for s in self.spots
            if s.is_free() and (vehicle_type is None or s.can_fit(vehicle_type))
        ]


# ----------------------------------------------------------------------------
# Parking strategies (Strategy pattern)
# Both now prefer an EXACT slot type, so an EV takes an EV slot before a CAR slot.
# ----------------------------------------------------------------------------
class ParkingStrategy(ABC):
    @abstractmethod
    def find_spot(self, vehicle, floors):
        pass

    @staticmethod
    def _candidates(vehicle, floors):
        return [
            s for f in floors for s in f.spots
            if s.is_free() and s.can_fit(vehicle.vehicle_type)
        ]

class FirstAvailableStrategy(ParkingStrategy):
    def find_spot(self, vehicle, floors):
        vt = vehicle.vehicle_type
        # min() returns the FIRST minimal element, so floor order is preserved.
        return min(
            self._candidates(vehicle, floors),
            key=lambda s: not s.is_exact_match(vt),     # False(0) sorts first
            default=None,
        )

class NearestSpotStrategy(ParkingStrategy):
    def find_spot(self, vehicle, floors):
        vt = vehicle.vehicle_type
        return min(
            self._candidates(vehicle, floors),
            key=lambda s: (not s.is_exact_match(vt), s.distance),
            default=None,
        )


# ----------------------------------------------------------------------------
# Ticket: now has status, exit time and fee (audit trail)
# ----------------------------------------------------------------------------
class Ticket:
    def __init__(self, vehicle, slot, entry_time=None):
        self.ticket_id = str(uuid.uuid4())
        self.vehicle = vehicle
        self.slot = slot
        self.entry_time = entry_time or datetime.now()
        self.exit_time = None
        self.fee = None
        self.status = TicketStatus.ACTIVE


# ----------------------------------------------------------------------------
# Pricing (Strategy + Decorator). Open/Closed: add rules without editing old code.
# ----------------------------------------------------------------------------
class PricingStrategy(ABC):
    @abstractmethod
    def calculate(self, ticket, exit_time):
        pass

class HourlyPricing(PricingStrategy):
    RATES = {
        VehicleType.BIKE: 10,
        VehicleType.CAR: 20,
        VehicleType.ELECTRIC_CAR: 30,
    }

    def calculate(self, ticket, exit_time):
        if exit_time < ticket.entry_time:
            raise ValueError("Exit time is before entry time")
        vt = ticket.vehicle.vehicle_type
        if vt not in self.RATES:
            raise ValueError(f"Pricing not configured for {vt}")
        seconds = (exit_time - ticket.entry_time).total_seconds()
        hours = max(1, math.ceil(seconds / 3600))      # 1 hour minimum, round up
        return hours * self.RATES[vt]

class PeakHourPricing(PricingStrategy):

    """Decorator: wraps any PricingStrategy and applies a multiplier
    if the vehicle ENTERED during peak hours."""
    def __init__(self, base, multiplier=1.5, peak_hours=((8, 11), (17, 20))):
        self.base = base
        self.multiplier = multiplier
        self.peak_hours = peak_hours

    def calculate(self, ticket, exit_time):
        fee = self.base.calculate(ticket, exit_time)
        h = ticket.entry_time.hour
        if any(start <= h < end for start, end in self.peak_hours):
            fee *= self.multiplier
        return fee

class WeekendPricing(PricingStrategy):
    """Another Decorator: flat discount on weekends."""
    def __init__(self, base, discount=0.8):
        self.base = base
        self.discount = discount

    def calculate(self, ticket, exit_time):
        fee = self.base.calculate(ticket, exit_time)
        if ticket.entry_time.weekday() >= 5:
            fee *= self.discount
        return fee


# ----------------------------------------------------------------------------
# Payment (Strategy). Real gateways would be injected the same way.
# ----------------------------------------------------------------------------
class PaymentMethod(ABC):
    @abstractmethod
    def pay(self, amount):
        """Return True on success, False on failure."""

class CashPayment(PaymentMethod):
    def pay(self, amount):
        return True

class CardPayment(PaymentMethod):
    def __init__(self, card_no):
        self.card_no = card_no
    def pay(self, amount):
        return bool(self.card_no)

class UPIPayment(PaymentMethod):
    def __init__(self, upi_id):
        self.upi_id = upi_id
    def pay(self, amount):
        return bool(self.upi_id) and "@" in self.upi_id


# ----------------------------------------------------------------------------
# Observer: lot notifies observers on every park / exit.
# ----------------------------------------------------------------------------
class ParkingObserver(ABC):
    @abstractmethod
    def update(self, lot):
        pass

class DisplayBoard(ParkingObserver):
    def __init__(self):
        self.snapshot = {}

    def update(self, lot):
        snap = {}
        for floor in lot.floors:
            snap[floor.floor_no] = {
                vt.name: len(floor.available_slots(vt)) for vt in VehicleType
            }
        self.snapshot = snap

    def show(self):
        lines = ["--- FREE SLOTS ---"]
        for fno, counts in sorted(self.snapshot.items()):
            parts = ", ".join(f"{k}: {v}" for k, v in counts.items())
            lines.append(f"Floor {fno}: {parts}")
        return "\n".join(lines)


# ----------------------------------------------------------------------------
# ParkingLot (Facade). Dependencies are injected: strategy, pricing, observers.
# ----------------------------------------------------------------------------
class ParkingLot:
    LOST_TICKET_PENALTY = 200
    _instance = None
    _instance_lock = threading.Lock()

    def __init__(self, floors, parking_strategy, pricing_strategy=None):
        self.floors = floors
        self.parking_strategy = parking_strategy
        self.pricing_strategy = pricing_strategy or HourlyPricing()
        self.active_tickets = {}      # ticket_id -> Ticket
        self.active_vehicles = {}     # vehicle number -> Ticket
        self.history = []             # closed tickets (audit)
        self._observers = []
        # ONE lock for all shared state. RLock so internal calls can re-enter.
        self._lock = threading.RLock()

    # ---- Singleton (optional) ---------------------------------------------
    @classmethod
    def get_instance(cls, floors=None, parking_strategy=None, pricing_strategy=None):
        with cls._instance_lock:
            if cls._instance is None:
                if floors is None or parking_strategy is None:
                    raise ValueError("First call must provide floors and strategy")
                cls._instance = cls(floors, parking_strategy, pricing_strategy)
            return cls._instance

    # ---- Observer plumbing ------------------------------------------------
    def add_observer(self, observer):
        self._observers.append(observer)
        observer.update(self)

    def _notify(self):
        for o in self._observers:
            o.update(self)

    # ---- Park -------------------------------------------------------------
    def park_vehicle(self, vehicle, entry_time=None):
        with self._lock:
            if vehicle.number in self.active_vehicles:
                raise VehicleAlreadyParkedError(f"{vehicle.number} is already parked")

            slot = self.parking_strategy.find_spot(vehicle, self.floors)
            if slot is None or not slot.park():
                raise ParkingFullError(f"No free slot for {vehicle.vehicle_type.name}")

            ticket = Ticket(vehicle, slot, entry_time)
            self.active_tickets[ticket.ticket_id] = ticket
            self.active_vehicles[vehicle.number] = ticket
            self._notify()
            return ticket

    # ---- Exit -------------------------------------------------------------
    def exit_vehicle(self, ticket_id, payment_method, exit_time=None):
        with self._lock:
            ticket = self.active_tickets.get(ticket_id)
            if ticket is None:
                raise InvalidTicketError("Invalid ticket or vehicle already exited")
            fee = self.pricing_strategy.calculate(ticket, exit_time or datetime.now())
            return self._settle(ticket, fee, payment_method, exit_time)

    def exit_lost_ticket(self, vehicle_number, payment_method, exit_time=None):
        """Lost ticket: find the ticket by vehicle number and add a penalty."""
        with self._lock:
            ticket = self.active_vehicles.get(vehicle_number.strip().upper())
            if ticket is None:
                raise InvalidTicketError("No active ticket for this vehicle")
            base = self.pricing_strategy.calculate(ticket, exit_time or datetime.now())
            return self._settle(ticket, base + self.LOST_TICKET_PENALTY,
                                payment_method, exit_time)

    def _settle(self, ticket, fee, payment_method, exit_time):
        # Called with the lock held.
        # NOTE: a real system would NOT hold the lot lock during a slow
        # payment gateway call. It would mark the ticket PAYING and release.
        # Kept simple here so the ticket can never be double-paid.
        if not payment_method.pay(fee):
            raise PaymentFailedError("Payment failed; ticket is still ACTIVE")
        ticket.status = TicketStatus.PAID
        ticket.fee = fee
        ticket.exit_time = exit_time or datetime.now()

        ticket.slot.free()
        del self.active_tickets[ticket.ticket_id]
        del self.active_vehicles[ticket.vehicle.number]
        ticket.status = TicketStatus.CLOSED
        self.history.append(ticket)
        self._notify()
        return fee

    # ---- Queries / admin --------------------------------------------------
    def available_slots(self, vehicle_type=None):
        with self._lock:
            return [s for f in self.floors for s in f.available_slots(vehicle_type)]

    def find_ticket_by_vehicle(self, vehicle_number):
        with self._lock:
            return self.active_vehicles.get(vehicle_number.strip().upper())

    def set_slot_maintenance(self, slot):
        with self._lock:
            ok = slot.set_maintenance()
            self._notify()
            return ok

    def restore_slot(self, slot):
        with self._lock:
            ok = slot.restore()
            self._notify()
            return ok


# ----------------------------------------------------------------------------
# Gate: entry/exit points that talk to the lot (multiple gates supported)
# ----------------------------------------------------------------------------
class Gate:
    def __init__(self, gate_id, lot):
        self.gate_id = gate_id
        self.lot = lot

class EntryGate(Gate):
    def enter(self, vehicle):
        return self.lot.park_vehicle(vehicle)

class ExitGate(Gate):
    def leave(self, ticket_id, payment_method):
        return self.lot.exit_vehicle(ticket_id, payment_method)


# ----------------------------------------------------------------------------
# Factory: build a lot from a simple config dict
# ----------------------------------------------------------------------------
class ParkingLotFactory:
    @staticmethod
    def create(config, parking_strategy=None, pricing_strategy=None):
        """
        config = {floor_no: {"CAR": 3, "BIKE": 2, "ELECTRIC_CAR": 1}, ...}
        Distance = running index on the floor (+ 100 per floor).
        """
        floors = []
        for floor_no, counts in config.items():
            spots, n = [], 0
            for type_name, count in counts.items():
                vt = VehicleType[type_name]
                for _ in range(count):
                    n += 1
                    spots.append(ParkingSlot(f"F{floor_no}-S{n}", vt,
                                             distance=floor_no * 100 + n))
            floors.append(ParkingFloor(floor_no, spots))
        return ParkingLot(floors,
                          parking_strategy or NearestSpotStrategy(),
                          pricing_strategy)


# ----------------------------------------------------------------------------
# DEMO + concurrency check
# ----------------------------------------------------------------------------
if __name__ == "__main__":
    pricing = PeakHourPricing(WeekendPricing(HourlyPricing()))
    lot = ParkingLotFactory.create(
        {0: {"CAR": 2, "BIKE": 1, "ELECTRIC_CAR": 1},
         1: {"CAR": 2, "BIKE": 1}},
        NearestSpotStrategy(), pricing)
    board = DisplayBoard()
    lot.add_observer(board)

    t1 = lot.park_vehicle(Vehicle("KA01AB1234", VehicleType.ELECTRIC_CAR))
    print("EV parked in:", t1.slot.slot_number, t1.slot.slot_type.name)
    t2 = lot.park_vehicle(Vehicle("KA02CD5678", VehicleType.ELECTRIC_CAR))
    print("2nd EV parked in:", t2.slot.slot_number, t2.slot.slot_type.name, "(falls back to CAR slot)")
    print(board.show())

    # duplicate vehicle
    try:
        lot.park_vehicle(Vehicle("ka01ab1234", VehicleType.ELECTRIC_CAR))
    except VehicleAlreadyParkedError as e:
        print("Duplicate blocked:", e)

    # pay by UPI after 2h30m
    later = t1.entry_time + timedelta(hours=2, minutes=30)
    print("Fee:", lot.exit_vehicle(t1.ticket_id, UPIPayment("me@upi"), later))

    # failed payment keeps ticket ACTIVE
    try:
        lot.exit_vehicle(t2.ticket_id, UPIPayment("bad"), later)
    except PaymentFailedError as e:
        print("Payment error:", e, "| status:", t2.status.name)

    # lost ticket
    print("Lost-ticket fee:", lot.exit_lost_ticket("KA02CD5678", CashPayment(), later))

    # double exit
    try:
        lot.exit_vehicle(t1.ticket_id, CashPayment())
    except InvalidTicketError as e:
        print("Double exit blocked:", e)

    # maintenance
    slot = lot.available_slots(VehicleType.BIKE)[0]
    lot.set_slot_maintenance(slot)
    print("Bike slots after maintenance:", len(lot.available_slots(VehicleType.BIKE)))
    print(board.show())

    # Concurrency stress test: 50 threads, 8 CAR slots -> exactly 8 must succeed
    big = ParkingLotFactory.create({0: {"CAR": 5}, 1: {"CAR": 3}})
    results, rlock = [], threading.Lock()
    def worker(i):
        try:
            tk = big.park_vehicle(Vehicle(f"CAR{i}", VehicleType.CAR))
            with rlock: results.append(tk.slot.slot_number)
        except ParkingFullError:
            pass
    threads = [threading.Thread(target=worker, args=(i,)) for i in range(50)]
    [t.start() for t in threads]; [t.join() for t in threads]
    print(f"Concurrency: {len(results)} parked, {len(set(results))} unique slots (expected 8 / 8)")
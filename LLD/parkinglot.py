"""
===============================================================================
PARKING LOT - LOW LEVEL DESIGN (annotated)
===============================================================================
The code below is your original logic, unchanged. Only comments were added.

Tags used in comments:
  [PATTERN]  design pattern used
  [SOLID]    SOLID principle followed or violated
  [GOOD]     something done well
  [BUG]      real bug, fix it
  [ISSUE]    smaller problem or smell
  [FIX]      suggested fix
  [ADD]      new requirement you can add

-------------------------------------------------------------------------------
SUMMARY
-------------------------------------------------------------------------------
PATTERNS FOLLOWED
  1. Strategy            -> ParkingStrategy (+ FirstAvailable, NearestSpot)
  2. Dependency Injection-> strategy passed into ParkingLot constructor
  3. Composition         -> ParkingLot -> ParkingFloor -> ParkingSlot
  4. Enum                -> VehicleType for type safety

PRINCIPLES FOLLOWED
  S - Ticket = data, FeeCalculator = pricing, Strategy = spot selection
  O - new parking strategies can be added without editing ParkingLot
  L - any ParkingStrategy subclass is substitutable
  D - ParkingLot depends on the abstract ParkingStrategy
  Encapsulation - ParkingSlot.__is_free is private
  Thread safety - you considered concurrency (but see BUG 1)

PRINCIPLES VIOLATED / WEAK
  O - FeeCalculator.PRICE is hardcoded (pricing cannot be extended)
  S - business classes call print() (mixes logic with I/O)
  D - ParkingLot creates FeeCalculator itself (should be injected)

TOP PRIORITIES
  1. Fix the locking bug (BUG 1)
  2. Make pricing a Strategy (ISSUE: pricing)
  3. Remove print() from business logic
  4. Add payment, slot status, display board (see [ADD] section at the end)
===============================================================================
"""

from abc import ABC, abstractmethod
from enum import Enum
from datetime import datetime
import threading
import uuid
import math


# [PATTERN] Enum: fixed set of vehicle types, no magic strings/ints.
# [ADD] Extend with TRUCK, HANDICAPPED, etc. and update can_fit() rules.
class VehicleType(Enum):
  CAR = 1
  BIKE = 2
  ELECTRIC_CAR = 3
#----------------------#
# [GOOD] Constructor validation (isinstance check) fails fast on bad input.
# [ISSUE] number is not validated (empty / None / format).
class Vehicle:
  def __init__(self, number, vehicle_type):
    if not isinstance(vehicle_type, VehicleType):
      raise TypeError("vehicle_type must be VehicleType")
    self.number = number
    self.vehicle_type = vehicle_type
#----------------------#
# [PATTERN] Composition: a floor HAS slots.
# [ISSUE] ParkingFloor is defined before ParkingSlot. It works because slots are
#         only passed in, but order ParkingSlot first for readability.
# [ADD] A display board could read available_slots() per floor (Observer).
class ParkingFloor:
    def __init__(self, floor_no, spots):
        self.floor_no = floor_no
        self.spots = spots

    def available_slots(self, vehicle_type=None):
        available = []

        for slot in self.spots:
            if slot.is_free():
                if vehicle_type is None or slot.can_fit(vehicle_type):
                    available.append(slot)

        return available
#----------------------#
class ParkingSlot:
  # [ISSUE] Duplication: slot stores floor_number, and ParkingFloor stores
  #         floor_no. Pick one source of truth.
  # [ADD] Replace the is_free bool with a SlotStatus enum
  #       (FREE, OCCUPIED, RESERVED, MAINTENANCE) or the State pattern.
  def __init__(self, slot_number, slot_type, distance, floor_number):
    if not isinstance(slot_type, VehicleType):
      raise TypeError("slot_type must be VehicleType")
    self.slot_number = slot_number
    self.slot_type = slot_type
    # [GOOD] Encapsulation: state is private, changed only via park()/free().
    self.__is_free = True
    self.distance = distance
    self.floor_number = floor_number

  # [ISSUE] print() inside business logic. Raise an exception (or just return
  #         False) and let the caller decide how to show it.
  # [BUG] The caller (ParkingLot.park_vehicle) ignores this return value.
  def park(self):
    if not self.__is_free:
            print("Slot is already occupied")
            return False
    self.__is_free = False
    return True

  def free(self):
      if self.__is_free:
          print("Slot is already free")
          return False

      self.__is_free = True
      return True

  # Business rule: an electric car may use an EV slot or a normal CAR slot.
  # [BUG-RELATED] This rule is what breaks the per-vehicle-type locks in
  #               ParkingLot: EV and CAR requests can reach the SAME slot.
  # [ISSUE] Hardcoded rule. For more rules, use a compatibility map:
  #         COMPATIBLE = {EV: {EV, CAR}, CAR: {CAR}, BIKE: {BIKE}}
  def can_fit(self,vehicle_type):
    if vehicle_type == VehicleType.ELECTRIC_CAR:
        return self.slot_type in [VehicleType.ELECTRIC_CAR, VehicleType.CAR]
    return vehicle_type == self.slot_type 

  def is_free(self):
        return self.__is_free


#----------------------#
# [PATTERN] STRATEGY
#   Interface: ParkingStrategy
#   Concrete:  FirstAvailableStrategy, NearestSpotStrategy
# [SOLID] O: add a new strategy (e.g. LowestFloorStrategy) with zero edits to
#         ParkingLot.
# [SOLID] L: every subclass honours the same contract: return a slot or None.
# [SOLID] D: ParkingLot depends on this abstraction.
class ParkingStrategy(ABC):
    @abstractmethod
    def find_spot(self, vehicle, floors):
        pass

class FirstAvailableStrategy(ParkingStrategy):
    # [ISSUE] Confusing double handling for EVs: it loops once to prefer EV
    #         slots, then falls back to the first compatible one.
    # [FIX]   Sort so exact-type slots come first, then return the first:
    #           spots.sort(key=lambda s: s.slot_type != vehicle.vehicle_type)
    #         (Python's sort is stable, so floor order is preserved.)
    # [ISSUE] The preference for an exact slot type only applies within ONE
    #         floor. An EV may take a CAR slot on floor 1 even though an EV
    #         slot is free on floor 2.
    def find_spot(self, vehicle, floors):
        for floor in floors:
            available_spots = [
                spot for spot in floor.spots
                if spot.is_free() and spot.can_fit(vehicle.vehicle_type)
            ]

            if vehicle.vehicle_type == VehicleType.ELECTRIC_CAR:
                for spot in available_spots:
                    if spot.slot_type == VehicleType.ELECTRIC_CAR:
                        return spot

            if available_spots:
                return available_spots[0]

        return None

class NearestSpotStrategy(ParkingStrategy):
    # [GOOD] Clean use of min() with key and default=None.
    # [ISSUE] Same EV preference problem: an EV could take a CAR slot that is
    #         nearer than a free EV slot. Use a key of
    #         (slot_type != vehicle_type, distance) to prefer exact matches.
    # [ISSUE] "distance" is a bare number. Document what it measures
    #         (from the gate? multiple gates need a distance per gate).
    def find_spot(self, vehicle, floors):
        compatible = []

        for floor in floors:
            compatible.extend([
                spot for spot in floor.spots
                if spot.is_free()
                and spot.can_fit(vehicle.vehicle_type)
            ])

        return min(
            compatible,
            key=lambda spot: spot.distance,
            default=None
        )
    
#----------------------#
# [GOOD] Ticket is a plain data holder (S in SOLID). uuid gives unique ids.
# [ISSUE] No exit_time, fee, or status. Add them for audit and history:
#           status: ACTIVE -> PAID -> CLOSED (enum)
# [ADD] Lost-ticket flow: look up the ticket by vehicle number, then charge a
#       penalty (ParkingLot already has active_vechicles for this lookup).
class Ticket:
    def __init__(self, vehicle, slot):
        self.ticket_id = str(uuid.uuid4())
        self.vehicle = vehicle
        self.slot = slot
        self.entry_time = datetime.now()

#----------------------#
# [SOLID] O is VIOLATED. Rates are hardcoded, so weekend pricing, peak hours,
#         monthly passes, EV charging fees all mean editing this class.
# [FIX]   Introduce a PricingStrategy (same idea as ParkingStrategy):
#
#   class PricingStrategy(ABC):
#       @abstractmethod
#       def calculate(self, ticket, exit_time): ...
#
#   class HourlyPricing(PricingStrategy): ...        # current logic
#   class PeakHourPricing(PricingStrategy):          # Decorator-style wrapper
#       def __init__(self, base, multiplier=1.5): ...
#
#   Then inject it: ParkingLot(floors, parking_strategy, pricing_strategy)
# [ISSUE] No check that exit_time >= entry_time.
# [GOOD] max(1, ceil(...)) correctly bills any partial hour as a full hour with
#        a 1 hour minimum.
class FeeCalculator:
    PRICE = {
            VehicleType.BIKE: 10,
            VehicleType.CAR: 20,
            VehicleType.ELECTRIC_CAR: 30
        }
    def calculate(self, ticket, exit_time):
        vehicle_type = ticket.vehicle.vehicle_type
        if vehicle_type not in self.PRICE:
            raise ValueError("Pricing not configured for this vehicle type")
        
        total_hours = max(1,math.ceil((exit_time-ticket.entry_time).total_seconds()/3600))
        return total_hours*self.PRICE[vehicle_type]

#----------------------#
# ParkingLot is the FACADE / orchestrator: callers only use park_vehicle,
# exit_vehicle and available_slots.
# [PATTERN] Dependency Injection for parking_strategy (good).
# [SOLID] D is only partly followed: FeeCalculator is created inside __init__.
#         Inject a PricingStrategy instead.
# [ADD] Singleton (or one instance created at startup) if the interviewer
#       wants a single global lot.
# [ADD] Observer: notify a DisplayBoard on every park/exit.
# [ADD] Gate entity: multiple entry/exit gates calling this class.
class ParkingLot:
    def __init__(self, floors, parking_strategy):
        self.floors = floors
        self.active_tickets = {}
        # [ISSUE] Typo: "vechicles" -> "vehicles" (rename everywhere).
        self.active_vechicles = {}
        self.fee_calculator = FeeCalculator()
        self.parking_strategy = parking_strategy
        # [BUG 1] ONE LOCK PER VEHICLE TYPE IS NOT ENOUGH.
        #   can_fit() lets an ELECTRIC_CAR use a CAR slot. So an EV thread
        #   (holding the EV lock) and a CAR thread (holding the CAR lock) can
        #   both run find_spot() at the same time, pick the same slot, and
        #   both "park" there = double booking.
        #   active_tickets / active_vechicles dicts are also shared across
        #   locks.
        # [FIX] Use ONE lock for the lot:  self._lock = threading.RLock()
        #   (Or a lock per slot, with the park() result checked, but a single
        #   lot lock is simplest and correct for interviews.)
        self.locks = {
            vehicle_type: threading.Lock()
            for vehicle_type in VehicleType
        }

    def park_vehicle(self, vehicle):
        lock = self.locks[vehicle.vehicle_type]
        with lock:
            # [GOOD] Duplicate check: the same vehicle cannot park twice.
            # [ISSUE] Returning None for both "already parked" and "lot full"
            #         is ambiguous. Raise VehicleAlreadyParkedException /
            #         ParkingFullException so callers can tell them apart.
            if vehicle.number in self.active_vechicles:
                return None
            slot = self.parking_strategy.find_spot(
                vehicle,
                self.floors
            )

            if slot is None:
                return None

            # [BUG 2] The return value of park() is ignored. If it returns
            #         False the slot was taken, yet a ticket is still issued.
            # [FIX]   if slot is None or not slot.park(): return None
            slot.park()

            ticket = Ticket(vehicle, slot)
            self.active_tickets[ticket.ticket_id] = ticket
            self.active_vechicles[vehicle.number] = ticket

            return ticket

    # [BUG 3] No lock in exit_vehicle. Two threads exiting the same ticket can
    #         both pass the "ticket is None" check, and then the second one
    #         raises KeyError on del. Also races with park_vehicle on the dicts.
    # [FIX]   with self._lock:
    #             ticket = self.active_tickets.pop(ticket_id, None)
    #         pop() removes and checks in one step.
    # [ISSUE] print() inside business logic. Return the fee and let the caller
    #         print it.
    # [ADD]   Payment step: Payment entity + PaymentMethod Strategy
    #         (Cash / Card / UPI). Only free the slot after payment succeeds,
    #         and mark ticket status PAID -> CLOSED.
    # [ISSUE] Fee is computed before the slot is freed, which is good. If
    #         calculate() raises, the state is unchanged. Keep that ordering.
    def exit_vehicle(self, ticket_id, exit_time=None):
        ticket = self.active_tickets.get(ticket_id)

        if ticket is None:
            print("Invalid ticket or vehicle already exited")
            return None

        if exit_time is None:
            exit_time = datetime.now()

        fee = self.fee_calculator.calculate(ticket, exit_time)

        ticket.slot.free()

        del self.active_tickets[ticket_id]
        del self.active_vechicles[ticket.vehicle.number]

        print("Vehicle exited successfully!")
        print(f"Parking Fee: Rs. {fee}")

        return fee

    # [GOOD] Delegates to ParkingFloor, which keeps floor logic in one place.
    # [ISSUE] Reads slot state without a lock, so the result can be slightly
    #         stale. Acceptable for a display, not for allocation.
    def available_slots(self, vehicle_type=None):
        available = []

        for floor in self.floors:
            available.extend(floor.available_slots(vehicle_type))

        return available


"""
===============================================================================
NEW REQUIREMENTS YOU CAN ADD  ->  pattern / concept
===============================================================================
[ADD] Payment (cash, card, UPI)       -> Strategy (PaymentMethod), Payment
                                         entity, ticket status ACTIVE/PAID/CLOSED
[ADD] Pricing rules (peak, weekend)   -> PricingStrategy + Decorator wrapper
[ADD] Multiple entry/exit gates       -> Gate class that calls ParkingLot
[ADD] Display board (free per floor)  -> Observer (lot notifies DisplayBoard)
[ADD] Slot states (maintenance, etc.) -> SlotStatus enum or State pattern
[ADD] Handicapped / truck slots       -> extend VehicleType and can_fit rules
[ADD] Reservation / pre-booking       -> Reservation entity with expiry
[ADD] EV charging fee                 -> extra pricing component (Decorator)
[ADD] Lost ticket penalty             -> lookup by vehicle number + flat fine
[ADD] Create slots/vehicles from cfg  -> Factory (SlotFactory, VehicleFactory)
[ADD] One global lot                  -> Singleton
[ADD] Monthly pass / membership       -> Customer and Pass entities, pricing
                                         strategy that checks them
[ADD] Custom exceptions               -> ParkingFullException,
                                         InvalidTicketException,
                                         VehicleAlreadyParkedException

SUGGESTED ORDER FOR AN INTERVIEW
  1. Fix locking (BUG 1-3) and remove print() calls
  2. PricingStrategy + PaymentMethod
  3. SlotStatus + Observer DisplayBoard
  4. Mention Singleton and Factory as optional extras
===============================================================================
"""
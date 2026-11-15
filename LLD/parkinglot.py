from abc import ABC, abstractmethod
from enum import Enum
from datetime import datetime
import threading
import uuid
import math

class VehicleType(Enum):
  CAR = 1
  BIKE = 2
  ELECTRIC_CAR = 3
#----------------------#
class Vehicle:
  def __init__(self, number, vehicle_type):
    if not isinstance(vehicle_type, VehicleType):
      raise TypeError("vehicle_type must be VehicleType")
    self.number = number
    self.vehicle_type = vehicle_type
#----------------------#
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
  def __init__(self, slot_number, slot_type, distance, floor_number):
    if not isinstance(slot_type, VehicleType):
      raise TypeError("slot_type must be VehicleType")
    self.slot_number = slot_number
    self.slot_type = slot_type
    self.__is_free = True
    self.distance = distance
    self.floor_number = floor_number

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

  def can_fit(self,vehicle_type):
    if vehicle_type == VehicleType.ELECTRIC_CAR:
        return self.slot_type in [VehicleType.ELECTRIC_CAR, VehicleType.CAR]
    return vehicle_type == self.slot_type 

  def is_free(self):
        return self.__is_free


#----------------------#
class ParkingStrategy(ABC):
    @abstractmethod
    def find_spot(self, vehicle, floors):
        pass

class FirstAvailableStrategy(ParkingStrategy):
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
class Ticket:
    def __init__(self, vehicle, slot):
        self.ticket_id = str(uuid.uuid4())
        self.vehicle = vehicle
        self.slot = slot
        self.entry_time = datetime.now()

#----------------------#
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
class ParkingLot:
    def __init__(self, floors, parking_strategy):
        self.floors = floors
        self.active_tickets = {}
        self.active_vechicles = {}
        self.fee_calculator = FeeCalculator()
        self.parking_strategy = parking_strategy
        self.locks = {
            vehicle_type: threading.Lock()
            for vehicle_type in VehicleType
        }

    def park_vehicle(self, vehicle):
        lock = self.locks[vehicle.vehicle_type]
        with lock:
            if vehicle.number in self.active_vechicles:
                return None
            slot = self.parking_strategy.find_spot(
                vehicle,
                self.floors
            )

            if slot is None:
                return None

            slot.park()

            ticket = Ticket(vehicle, slot)
            self.active_tickets[ticket.ticket_id] = ticket
            self.active_vechicles[vehicle.number] = ticket

            return ticket

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

    def available_slots(self, vehicle_type=None):
        available = []

        for floor in self.floors:
            available.extend(floor.available_slots(vehicle_type))

        return available
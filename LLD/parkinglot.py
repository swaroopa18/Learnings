from enum import Enum
from datetime import datetime
import uuid
import math

class VehicleType(Enum):
  CAR = 1
  BIKE = 2
#----------------------#
class Vehicle:
  def __init__(self, number, vehicle_type):
    if not isinstance(vehicle_type, VehicleType):
      raise TypeError("vehicle_type must be VehicleType")
    self.number = number
    self.vehicle_type = vehicle_type
#----------------------#
class ParkingSlot:
  def __init__(self, slot_number, slot_type):
    if not isinstance(slot_type, VehicleType):
      raise TypeError("slot_type must be VehicleType")
    self.slot_number = slot_number
    self.slot_type = slot_type
    self.__is_free = True

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
    return vehicle_type == self.slot_type

  def is_free(self):
        return self.__is_free

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
            VehicleType.CAR: 20
        }
    def calculate(self, ticket, exit_time):
        vehicle_type = ticket.vehicle.vehicle_type
        if vehicle_type not in self.PRICE:
            raise ValueError("Pricing not configured for this vehicle type")
        
        total_hours = max(1,math.ceil((exit_time-ticket.entry_time).total_seconds()/3600))
        return total_hours*self.PRICE[vehicle_type]

#----------------------#
class ParkingLot:
    def __init__(self, slots):
        self.slots = slots
        self.active_tickets = {}
        self.fee_calculator = FeeCalculator()

    def find_available_slot(self, vehicle_type):
        for slot in self.slots:
          if slot.is_free() and slot.can_fit(vehicle_type):
            return slot
        return None

    def park_vehicle(self, vehicle):
        slot = self.find_available_slot(vehicle.vehicle_type)

        if slot is None:
            print("No available parking slot")
            return None

        if slot.park():
            ticket = Ticket(vehicle, slot)
            self.active_tickets[ticket.ticket_id] = ticket

            print(f"Vehicle parked successfully!")
            print(f"Slot Number: {slot.slot_number}")
            print(f"Ticket ID: {ticket.ticket_id}")

            return ticket
        return None

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

        print("Vehicle exited successfully!")
        print(f"Parking Fee: Rs. {fee}")

        return fee

    def available_slots(self, vehicle_type=None):
        available = []

        for slot in self.slots:
            if slot.is_free():
                if vehicle_type is None or slot.can_fit(vehicle_type):
                    available.append(slot)

        return available
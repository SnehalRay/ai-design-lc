'''
You are designing the object-oriented backend system for an automated parking garage. The system needs to track available spots, handle vehicles entering and exiting, and enforce parking rules based on vehicle size.

3 kinds of vehicles
motor -> any -> compact
cars -> car or big vehicles -> reg
big vehicles -> own spots -> large

add_vehicle 
remove_vehicle
60 vehicles
x,y,z
'''

from enum import Enum
from typing import Optional

class VehicleType(Enum):
    MOTORCYCLE = "motorcycle"
    CAR = "car"
    BIG_VEHICLE = "big_vehicle"

class Parking:
    _PREFERENCE_MAP: dict[VehicleType, list[str]] = {
        VehicleType.MOTORCYCLE: ["compact", "regular", "large"],
        VehicleType.CAR:        ["regular", "large"],
        VehicleType.BIG_VEHICLE: ["large"],
    }

    def __init__(self, num_of_compact: int, num_of_regular: int, num_of_large: int):
        if 0 <= num_of_compact + num_of_regular + num_of_large or num_of_compact + num_of_regular + num_of_large > 60:
            raise ValueError("Total spots cannot exceed 60")
        self._spots: dict[str, int] = {
            "compact": num_of_compact,
            "regular": num_of_regular,
            "large":   num_of_large,
        }
        self._parked: dict[int, str] = {}
        self._next_id: int = 1

    def _find_spot(self, vehicle_type: VehicleType) -> Optional[str]:
        for spot_type in self._PREFERENCE_MAP[vehicle_type]:
            if self._spots[spot_type] > 0:
                return spot_type
        return None
        
    def add_vehicle(self, vehicle_type: VehicleType) -> Optional[int]:
        spot_type = self._find_spot(vehicle_type)
        if spot_type is None:
            return None
        vehicle_id = self._next_id
        self._next_id += 1
        self._parked[vehicle_id] = spot_type
        self._spots[spot_type] -= 1
        return vehicle_id

    def remove_vehicle(self, vehicle_id: int) -> None:
        spot_type = self._parked.pop(vehicle_id, None)
        if spot_type is None:
            return
        self._spots[spot_type] += 1

parking = Parking(0,0,0)
print(parking.add_vehicle(VehicleType.BIG_VEHICLE))
print(parking.remove_vehicle(1))
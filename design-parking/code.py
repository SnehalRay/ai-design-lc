'''
Design car park
3 cars: bike, car and bus
3 spots: small, medium and large
bike-> small, medium and large
car-> med and large
bus-> only large

10 small
20 medium
10 large

Features:
1. park a vehicle
2. remove a vehicle
3. find where a specific vehicle is parker
4. what vehicle is in a spot
'''


'''

❯ def parking_vehicle(self,vehicle: Vehicle):
          pass
  
  let us implement this method
  
  here we will go based on the vehicle type
  if bike, it will look to park it in in bike 
  parking first, if not aka full then car, if not 
  aka full then bus
  
  if everything is full 
  
'''
from enum import Enum


class VehicleType(Enum):
    BIKE = "bike"
    CAR = "car"
    BUS = "bus"


class SpotType(Enum):
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"


class Vehicle:
    def __init__(self, vehicle_type: VehicleType):
        self.vehicle_type = vehicle_type



class ParkingSpot:
    _id_counter = 0

    def __init__(self, spot_type: SpotType):
        ParkingSpot._id_counter += 1
        self.spot_id = ParkingSpot._id_counter
        self.spot_type = spot_type
        self.vehicle = None

    def is_empty(self) -> bool:
        return self.vehicle is None

    def find(self) -> Vehicle:
        return self.vehicle

    def add_vehicle(self, vehicle: Vehicle) -> bool:
        if not self.is_empty():
            return False
        self.vehicle = vehicle
        return True
    
    def remove_vehicle(self) -> bool:
        if self.is_empty():
            return False
        self.vehicle = None
        return True


class ParkingLot:
    def __init__(self,small=10, medium=20, large=10):
        self.small_count = small
        self.medium_count = medium
        self.large_count = large

        self.small_spots = [ParkingSpot(SpotType.SMALL) for _ in range(self.small_count)]
        self.medium_spots = [ParkingSpot(SpotType.MEDIUM) for _ in range(self.medium_count)]
        self.large_spots = [ParkingSpot(SpotType.LARGE) for _ in range(self.large_count)]

        self.vehicles = {} #vehicle: parking

    def parking_vehicle(self, vehicle: Vehicle) -> ParkingSpot:
        if vehicle.vehicle_type == VehicleType.BIKE:
            spot_priority = [self.small_spots, self.medium_spots, self.large_spots]
        elif vehicle.vehicle_type == VehicleType.CAR:
            spot_priority = [self.medium_spots, self.large_spots]
        else:  # BUS
            spot_priority = [self.large_spots]

        for spots in spot_priority:
            for i, spot in enumerate(spots):
                if spot.is_empty():
                    spot.add_vehicle(vehicle)
                    self.vehicles[vehicle] = spot
                    return spot
        return -1

    def remove_vehicle(self,vehicle: Vehicle):
        if vehicle not in self.vehicles:
            return False
        spot= self.vehicles[vehicle]
        spot.remove_vehicle()
        del self.vehicles[vehicle]
        return True

    def vehicle_location(self,vehicle: Vehicle):

        return self.vehicles[vehicle]

    def find_vehicle_with_spot(self, parkType: SpotType, idx: int) -> Vehicle:
        if parkType == SpotType.SMALL:
            spots = self.small_spots
        elif parkType == SpotType.MEDIUM:
            spots = self.medium_spots
        else:
            spots = self.large_spots

        if idx < 0 or idx >= len(spots):
            return None
        return spots[idx].find()


def main():
    lot = ParkingLot()

    bike = Vehicle(VehicleType.BIKE)
    car = Vehicle(VehicleType.CAR)
    bus = Vehicle(VehicleType.BUS)

    # park all 3
    spot = lot.parking_vehicle(bike)
    print(f"[BIKE]  parked -> spot_id={spot.spot_id}, type={spot.spot_type}")

    spot = lot.parking_vehicle(car)
    print(f"[CAR]   parked -> spot_id={spot.spot_id}, type={spot.spot_type}")

    spot = lot.parking_vehicle(bus)
    print(f"[BUS]   parked -> spot_id={spot.spot_id}, type={spot.spot_type}")

    # vehicle_location
    loc = lot.vehicle_location(bike)
    print(f"[LOCATION] bike is at spot_id={loc.spot_id}, type={loc.spot_type}")

    # find_vehicle_with_spot
    found = lot.find_vehicle_with_spot(SpotType.SMALL, 0)
    print(f"[FIND]  small[0] -> vehicle_type={found.vehicle_type}")

    # remove bike
    removed = lot.remove_vehicle(bike)
    print(f"[REMOVE] bike removed={removed}, spot empty={lot.small_spots[0].is_empty()}")

    # find after removal
    found = lot.find_vehicle_with_spot(SpotType.SMALL, 0)
    print(f"[FIND after remove] small[0] -> {found}")

    # remove ghost vehicle
    ghost = Vehicle(VehicleType.CAR)
    print(f"[REMOVE ghost] result={lot.remove_vehicle(ghost)}")

    # out of bounds
    print(f"[OOB]   small[999] -> {lot.find_vehicle_with_spot(SpotType.SMALL, 999)}")


if __name__ == "__main__":
    main()
    



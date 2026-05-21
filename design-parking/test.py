import unittest
from code import VehicleType, SpotType, Vehicle, ParkingSpot, ParkingLot


class TestParkingSpot(unittest.TestCase):

    def setUp(self):
        self.spot = ParkingSpot(SpotType.SMALL)

    def test_is_empty_when_created(self):
        self.assertTrue(self.spot.is_empty())

    def test_unique_spot_ids(self):
        other = ParkingSpot(SpotType.MEDIUM)
        self.assertNotEqual(self.spot.spot_id, other.spot_id)

    def test_spot_type_assigned(self):
        self.assertEqual(self.spot.spot_type, SpotType.SMALL)

    def test_add_vehicle(self):
        vehicle = Vehicle(VehicleType.BIKE)
        result = self.spot.add_vehicle(vehicle)
        self.assertTrue(result)
        self.assertFalse(self.spot.is_empty())

    def test_add_vehicle_to_occupied_spot(self):
        v1 = Vehicle(VehicleType.BIKE)
        v2 = Vehicle(VehicleType.BIKE)
        self.spot.add_vehicle(v1)
        result = self.spot.add_vehicle(v2)
        self.assertFalse(result)

    def test_find_returns_vehicle(self):
        vehicle = Vehicle(VehicleType.CAR)
        self.spot.add_vehicle(vehicle)
        self.assertEqual(self.spot.find(), vehicle)

    def test_find_returns_none_when_empty(self):
        self.assertIsNone(self.spot.find())

    def test_remove_vehicle(self):
        vehicle = Vehicle(VehicleType.BUS)
        self.spot.add_vehicle(vehicle)
        result = self.spot.remove_vehicle()
        self.assertTrue(result)
        self.assertTrue(self.spot.is_empty())

    def test_remove_from_empty_spot(self):
        result = self.spot.remove_vehicle()
        self.assertFalse(result)


class TestParkingLot(unittest.TestCase):

    def setUp(self):
        self.lot = ParkingLot(small=2, medium=2, large=2)

    def test_bike_parks_in_small(self):
        bike = Vehicle(VehicleType.BIKE)
        spot = self.lot.parking_vehicle(bike)
        self.assertEqual(spot.spot_type, SpotType.SMALL)

    def test_car_parks_in_medium(self):
        car = Vehicle(VehicleType.CAR)
        spot = self.lot.parking_vehicle(car)
        self.assertEqual(spot.spot_type, SpotType.MEDIUM)

    def test_bus_parks_in_large(self):
        bus = Vehicle(VehicleType.BUS)
        spot = self.lot.parking_vehicle(bus)
        self.assertEqual(spot.spot_type, SpotType.LARGE)

    def test_bike_overflows_to_medium_when_small_full(self):
        b1 = Vehicle(VehicleType.BIKE)
        b2 = Vehicle(VehicleType.BIKE)
        b3 = Vehicle(VehicleType.BIKE)  # small is full (size=2), should go to medium
        self.lot.parking_vehicle(b1)
        self.lot.parking_vehicle(b2)
        spot = self.lot.parking_vehicle(b3)
        self.assertEqual(spot.spot_type, SpotType.MEDIUM)

    def test_car_overflows_to_large_when_medium_full(self):
        c1 = Vehicle(VehicleType.CAR)
        c2 = Vehicle(VehicleType.CAR)
        c3 = Vehicle(VehicleType.CAR)  # medium full, should go to large
        self.lot.parking_vehicle(c1)
        self.lot.parking_vehicle(c2)
        spot = self.lot.parking_vehicle(c3)
        self.assertEqual(spot.spot_type, SpotType.LARGE)

    def test_returns_minus_one_when_full(self):
        for _ in range(2):
            self.lot.parking_vehicle(Vehicle(VehicleType.BUS))
        result = self.lot.parking_vehicle(Vehicle(VehicleType.BUS))
        self.assertEqual(result, -1)

    def test_remove_vehicle(self):
        bike = Vehicle(VehicleType.BIKE)
        self.lot.parking_vehicle(bike)
        result = self.lot.remove_vehicle(bike)
        self.assertTrue(result)

    def test_remove_frees_spot(self):
        bike = Vehicle(VehicleType.BIKE)
        self.lot.parking_vehicle(bike)
        self.lot.remove_vehicle(bike)
        self.assertTrue(self.lot.small_spots[0].is_empty())

    def test_remove_nonexistent_vehicle(self):
        ghost = Vehicle(VehicleType.CAR)
        result = self.lot.remove_vehicle(ghost)
        self.assertFalse(result)

    def test_vehicle_location(self):
        car = Vehicle(VehicleType.CAR)
        parked_spot = self.lot.parking_vehicle(car)
        loc = self.lot.vehicle_location(car)
        self.assertEqual(loc, parked_spot)

    def test_find_vehicle_with_spot(self):
        bike = Vehicle(VehicleType.BIKE)
        self.lot.parking_vehicle(bike)
        found = self.lot.find_vehicle_with_spot(SpotType.SMALL, 0)
        self.assertEqual(found, bike)

    def test_find_vehicle_empty_spot(self):
        found = self.lot.find_vehicle_with_spot(SpotType.SMALL, 0)
        self.assertIsNone(found)

    def test_find_vehicle_out_of_bounds(self):
        found = self.lot.find_vehicle_with_spot(SpotType.SMALL, 999)
        self.assertIsNone(found)


if __name__ == "__main__":
    unittest.main()

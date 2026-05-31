import unittest
from code import Parking, VehicleType


class TestParkingInit(unittest.TestCase):

    def test_valid_init(self):
        p = Parking(10, 10, 10)
        self.assertEqual(p._spots["compact"], 10)
        self.assertEqual(p._spots["regular"], 10)
        self.assertEqual(p._spots["large"], 10)

    def test_init_at_capacity_limit(self):
        p = Parking(20, 20, 20)
        self.assertEqual(sum(p._spots.values()), 60)

    def test_init_exceeds_limit(self):
        with self.assertRaises(ValueError):
            Parking(30, 20, 11)

    def test_init_zeros(self):
        p = Parking(0, 0, 0)
        self.assertEqual(sum(p._spots.values()), 0)


class TestAddVehicle(unittest.TestCase):

    def test_motorcycle_uses_compact_first(self):
        p = Parking(1, 1, 1)
        vid = p.add_vehicle(VehicleType.MOTORCYCLE)
        self.assertIsNotNone(vid)
        self.assertEqual(p._parked[vid], "compact")
        self.assertEqual(p._spots["compact"], 0)

    def test_motorcycle_falls_back_to_regular(self):
        p = Parking(0, 1, 1)
        vid = p.add_vehicle(VehicleType.MOTORCYCLE)
        self.assertEqual(p._parked[vid], "regular")

    def test_motorcycle_falls_back_to_large(self):
        p = Parking(0, 0, 1)
        vid = p.add_vehicle(VehicleType.MOTORCYCLE)
        self.assertEqual(p._parked[vid], "large")

    def test_car_uses_regular_first(self):
        p = Parking(1, 1, 1)
        vid = p.add_vehicle(VehicleType.CAR)
        self.assertEqual(p._parked[vid], "regular")
        self.assertEqual(p._spots["regular"], 0)

    def test_car_falls_back_to_large(self):
        p = Parking(1, 0, 1)
        vid = p.add_vehicle(VehicleType.CAR)
        self.assertEqual(p._parked[vid], "large")

    def test_car_cannot_use_compact(self):
        p = Parking(5, 0, 0)
        vid = p.add_vehicle(VehicleType.CAR)
        self.assertIsNone(vid)

    def test_big_vehicle_uses_large(self):
        p = Parking(1, 1, 1)
        vid = p.add_vehicle(VehicleType.BIG_VEHICLE)
        self.assertEqual(p._parked[vid], "large")
        self.assertEqual(p._spots["large"], 0)

    def test_big_vehicle_cannot_use_compact_or_regular(self):
        p = Parking(5, 5, 0)
        vid = p.add_vehicle(VehicleType.BIG_VEHICLE)
        self.assertIsNone(vid)

    def test_add_returns_incrementing_ids(self):
        p = Parking(5, 5, 5)
        id1 = p.add_vehicle(VehicleType.MOTORCYCLE)
        id2 = p.add_vehicle(VehicleType.MOTORCYCLE)
        id3 = p.add_vehicle(VehicleType.MOTORCYCLE)
        self.assertEqual(id2, id1 + 1)
        self.assertEqual(id3, id2 + 1)

    def test_add_when_full_returns_none(self):
        p = Parking(0, 0, 0)
        self.assertIsNone(p.add_vehicle(VehicleType.MOTORCYCLE))

    def test_spot_count_decrements_on_add(self):
        p = Parking(2, 2, 2)
        p.add_vehicle(VehicleType.MOTORCYCLE)
        self.assertEqual(p._spots["compact"], 1)


class TestRemoveVehicle(unittest.TestCase):

    def test_remove_frees_spot(self):
        p = Parking(1, 1, 1)
        vid = p.add_vehicle(VehicleType.CAR)
        self.assertEqual(p._spots["regular"], 0)
        p.remove_vehicle(vid)
        self.assertEqual(p._spots["regular"], 1)

    def test_remove_clears_parked_entry(self):
        p = Parking(1, 1, 1)
        vid = p.add_vehicle(VehicleType.MOTORCYCLE)
        p.remove_vehicle(vid)
        self.assertNotIn(vid, p._parked)

    def test_remove_unknown_id_is_noop(self):
        p = Parking(1, 1, 1)
        p.remove_vehicle(999)
        self.assertEqual(p._spots["compact"], 1)
        self.assertEqual(p._spots["regular"], 1)
        self.assertEqual(p._spots["large"], 1)

    def test_double_remove_is_noop(self):
        p = Parking(1, 1, 1)
        vid = p.add_vehicle(VehicleType.MOTORCYCLE)
        p.remove_vehicle(vid)
        p.remove_vehicle(vid)
        self.assertEqual(p._spots["compact"], 1)

    def test_remove_then_readd(self):
        p = Parking(1, 0, 0)
        vid = p.add_vehicle(VehicleType.MOTORCYCLE)
        p.remove_vehicle(vid)
        new_vid = p.add_vehicle(VehicleType.MOTORCYCLE)
        self.assertIsNotNone(new_vid)
        self.assertEqual(p._spots["compact"], 0)


class TestParkingRules(unittest.TestCase):

    def test_large_preserved_for_big_vehicles(self):
        p = Parking(0, 0, 1)
        p.add_vehicle(VehicleType.MOTORCYCLE)
        vid = p.add_vehicle(VehicleType.BIG_VEHICLE)
        self.assertIsNone(vid)

    def test_full_cycle_all_vehicle_types(self):
        p = Parking(1, 1, 1)
        mid = p.add_vehicle(VehicleType.MOTORCYCLE)
        cid = p.add_vehicle(VehicleType.CAR)
        bid = p.add_vehicle(VehicleType.BIG_VEHICLE)
        self.assertIsNotNone(mid)
        self.assertIsNotNone(cid)
        self.assertIsNotNone(bid)
        self.assertEqual(sum(p._spots.values()), 0)
        p.remove_vehicle(mid)
        p.remove_vehicle(cid)
        p.remove_vehicle(bid)
        self.assertEqual(sum(p._spots.values()), 3)

    def test_garage_fills_up_then_rejects(self):
        p = Parking(1, 0, 0)
        vid = p.add_vehicle(VehicleType.MOTORCYCLE)
        self.assertIsNotNone(vid)
        self.assertIsNone(p.add_vehicle(VehicleType.MOTORCYCLE))


if __name__ == "__main__":
    unittest.result.TestResult.maxDiff = None
    unittest.main(verbosity=2)

import unittest
from code import UndergroundSystem


class TestUndergroundSystem(unittest.TestCase):

    def setUp(self):
        self.system = UndergroundSystem()

    # --- Happy Path ---

    def test_single_trip(self):
        self.system.checkIn(1, "Leyton", 0)
        self.system.checkOut(1, "Waterloo", 10)
        self.assertEqual(self.system.averageTime("Leyton", "Waterloo"), 10.0)

    def test_average_updates(self):
        self.system.checkIn(1, "Leyton", 0)
        self.system.checkOut(1, "Waterloo", 10)  # duration 10

        self.system.checkIn(2, "Leyton", 5)
        self.system.checkOut(2, "Waterloo", 25)  # duration 20

        self.assertAlmostEqual(self.system.averageTime("Leyton", "Waterloo"), 15.0)

    def test_direction_asymmetry(self):
        self.system.checkIn(1, "A", 0)
        self.system.checkOut(1, "B", 10)  # A->B: 10

        self.system.checkIn(2, "B", 0)
        self.system.checkOut(2, "A", 30)  # B->A: 30

        self.assertEqual(self.system.averageTime("A", "B"), 10.0)
        self.assertEqual(self.system.averageTime("B", "A"), 30.0)

    # --- Edge Cases ---

    def test_same_station(self):
        self.system.checkIn(1, "Central", 5)
        self.system.checkOut(1, "Central", 15)  # duration 10
        self.assertEqual(self.system.averageTime("Central", "Central"), 10.0)

    def test_concurrent_users(self):
        self.system.checkIn(1, "Leyton", 0)
        self.system.checkIn(2, "Waterloo", 0)
        self.system.checkOut(1, "Waterloo", 10)   # Leyton->Waterloo: 10
        self.system.checkOut(2, "Leyton", 20)     # Waterloo->Leyton: 20

        self.assertEqual(self.system.averageTime("Leyton", "Waterloo"), 10.0)
        self.assertEqual(self.system.averageTime("Waterloo", "Leyton"), 20.0)

    def test_user_makes_multiple_trips(self):
        self.system.checkIn(1, "Leyton", 0)
        self.system.checkOut(1, "Waterloo", 10)   # trip 1: duration 10

        self.system.checkIn(1, "Leyton", 20)
        self.system.checkOut(1, "Waterloo", 50)   # trip 2: duration 30

        self.assertAlmostEqual(self.system.averageTime("Leyton", "Waterloo"), 20.0)

    def test_unseen_route_returns_inf(self):
        self.assertEqual(self.system.averageTime("Nowhere", "Anywhere"), float('inf'))

    def test_checkout_without_checkin_raises(self):
        with self.assertRaises(KeyError):
            self.system.checkOut(99, "Waterloo", 10)

    def test_average_is_float(self):
        self.system.checkIn(1, "A", 0)
        self.system.checkOut(1, "B", 7)
        result = self.system.averageTime("A", "B")
        self.assertIsInstance(result, float)


if __name__ == "__main__":
    unittest.main()

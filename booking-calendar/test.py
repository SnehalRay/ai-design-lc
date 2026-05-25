import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from code import MyCalendar


class TestMyCalendarNormalCases(unittest.TestCase):

    def test_n1_single_booking(self):
        cal = MyCalendar()
        self.assertTrue(cal.book(10, 20))

    def test_n2_two_non_overlapping_with_gap(self):
        cal = MyCalendar()
        self.assertTrue(cal.book(10, 20))
        self.assertTrue(cal.book(30, 40))

    def test_n3_two_overlapping(self):
        cal = MyCalendar()
        self.assertTrue(cal.book(10, 20))
        self.assertFalse(cal.book(15, 25))

    def test_n4_rejected_booking_does_not_block_future_valid_booking(self):
        cal = MyCalendar()
        self.assertTrue(cal.book(10, 20))
        self.assertFalse(cal.book(15, 25))
        self.assertTrue(cal.book(25, 35))

    def test_n5_sequential_adjacent_bookings(self):
        cal = MyCalendar()
        self.assertTrue(cal.book(0, 10))
        self.assertTrue(cal.book(10, 20))
        self.assertTrue(cal.book(20, 30))


class TestMyCalendarEdgeCases(unittest.TestCase):

    def test_e1_adjacent_new_starts_where_old_ends(self):
        cal = MyCalendar()
        self.assertTrue(cal.book(10, 20))
        self.assertTrue(cal.book(20, 30))

    def test_e2_adjacent_reversed_insertion_order(self):
        cal = MyCalendar()
        self.assertTrue(cal.book(20, 30))
        self.assertTrue(cal.book(10, 20))

    def test_e3_exact_duplicate(self):
        cal = MyCalendar()
        self.assertTrue(cal.book(10, 20))
        self.assertFalse(cal.book(10, 20))

    def test_e4_new_event_fully_contains_existing(self):
        cal = MyCalendar()
        self.assertTrue(cal.book(15, 25))
        self.assertFalse(cal.book(10, 30))

    def test_e5_new_event_fully_inside_existing(self):
        cal = MyCalendar()
        self.assertTrue(cal.book(10, 30))
        self.assertFalse(cal.book(15, 25))

    def test_e6_same_start_boundary(self):
        cal = MyCalendar()
        self.assertTrue(cal.book(10, 20))
        self.assertFalse(cal.book(10, 15))

    def test_e7_same_end_boundary(self):
        cal = MyCalendar()
        self.assertTrue(cal.book(10, 20))
        self.assertFalse(cal.book(15, 20))

    def test_e8_overlap_by_one_unit(self):
        cal = MyCalendar()
        self.assertTrue(cal.book(10, 20))
        self.assertFalse(cal.book(19, 25))

    def test_e9_booking_at_time_zero(self):
        cal = MyCalendar()
        self.assertTrue(cal.book(0, 5))

    def test_e10_minimal_one_unit_adjacent_intervals(self):
        cal = MyCalendar()
        self.assertTrue(cal.book(5, 6))
        self.assertTrue(cal.book(6, 7))

    def test_e11_new_event_ends_where_existing_starts(self):
        cal = MyCalendar()
        self.assertTrue(cal.book(20, 30))
        self.assertTrue(cal.book(10, 20))

    def test_e12_fresh_instance_per_test(self):
        cal1 = MyCalendar()
        self.assertTrue(cal1.book(10, 20))

        cal2 = MyCalendar()
        self.assertTrue(cal2.book(10, 20))


if __name__ == "__main__":
    unittest.main(verbosity=2)

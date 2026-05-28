import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from code import MKAverage


class TestWindowNotFull(unittest.TestCase):

    def test_no_elements(self):
        obj = MKAverage(3, 1)
        self.assertEqual(obj.calculateMKAverage(), -1)

    def test_partial_window(self):
        obj = MKAverage(3, 1)
        obj.addElement(5)
        self.assertEqual(obj.calculateMKAverage(), -1)
        obj.addElement(10)
        self.assertEqual(obj.calculateMKAverage(), -1)

    def test_one_before_full(self):
        obj = MKAverage(4, 1)
        for v in [1, 2, 3]:
            obj.addElement(v)
        self.assertEqual(obj.calculateMKAverage(), -1)

    def test_exactly_at_m(self):
        obj = MKAverage(3, 1)
        obj.addElement(3)
        obj.addElement(1)
        obj.addElement(12)
        self.assertEqual(obj.calculateMKAverage(), 3)


class TestSlidingWindow(unittest.TestCase):

    def test_lc_example(self):
        obj = MKAverage(3, 1)
        obj.addElement(3)
        self.assertEqual(obj.calculateMKAverage(), -1)
        obj.addElement(1)
        self.assertEqual(obj.calculateMKAverage(), -1)
        obj.addElement(12)
        self.assertEqual(obj.calculateMKAverage(), 3)   # window=[3,1,12] → mid=3
        obj.addElement(5)
        self.assertEqual(obj.calculateMKAverage(), 5)   # window=[1,12,5] → mid=5
        obj.addElement(3)
        self.assertEqual(obj.calculateMKAverage(), 5)   # window=[12,5,3] → mid=5
        obj.addElement(4)
        self.assertEqual(obj.calculateMKAverage(), 4)   # window=[5,3,4] → mid=4

    def test_window_slides_correctly(self):
        obj = MKAverage(3, 1)
        for v in [10, 20, 30]:
            obj.addElement(v)
        self.assertEqual(obj.calculateMKAverage(), 20)  # mid of [10,20,30]
        obj.addElement(40)
        self.assertEqual(obj.calculateMKAverage(), 30)  # window=[20,30,40], mid=30
        obj.addElement(50)
        self.assertEqual(obj.calculateMKAverage(), 40)  # window=[30,40,50], mid=40


class TestFloorDivision(unittest.TestCase):

    def test_floor_not_round(self):
        obj = MKAverage(4, 1)          # mid has 2 elements
        for v in [1, 10, 3, 4]:
            obj.addElement(v)
        # sorted=[1,3,4,10], mid=[3,4], sum=7, 7//2=3
        self.assertEqual(obj.calculateMKAverage(), 3)

    def test_odd_sum_truncates_down(self):
        obj = MKAverage(4, 1)
        for v in [1, 100, 2, 4]:
            obj.addElement(v)
        # sorted=[1,2,4,100], mid=[2,4], sum=6, 6//2=3
        self.assertEqual(obj.calculateMKAverage(), 3)


class TestDuplicateValues(unittest.TestCase):

    def test_all_same(self):
        obj = MKAverage(3, 1)
        for _ in range(6):
            obj.addElement(5)
            if obj.calculateMKAverage() != -1:
                self.assertEqual(obj.calculateMKAverage(), 5)

    def test_duplicate_at_boundary_eviction(self):
        obj = MKAverage(3, 1)
        for v in [3, 3, 3]:
            obj.addElement(v)
        self.assertEqual(obj.calculateMKAverage(), 3)
        obj.addElement(6)
        # window=[3,3,6], sorted=[3,3,6], mid=[3], avg=3
        self.assertEqual(obj.calculateMKAverage(), 3)

    def test_evict_one_of_duplicates(self):
        obj = MKAverage(3, 1)
        for v in [2, 2, 8]:
            obj.addElement(v)
        self.assertEqual(obj.calculateMKAverage(), 2)   # window=[2,2,8], mid=[2]
        obj.addElement(5)
        # evicts first 2, window=[2,8,5], sorted=[2,5,8], mid=[5]
        self.assertEqual(obj.calculateMKAverage(), 5)


class TestEvictionFromEachPartition(unittest.TestCase):

    def test_evict_from_low(self):
        obj = MKAverage(3, 1)
        for v in [1, 5, 8]:
            obj.addElement(v)
        self.assertEqual(obj.calculateMKAverage(), 5)
        obj.addElement(6)
        # evicts 1 (oldest, in low), window=[5,8,6], sorted=[5,6,8], mid=[6]
        self.assertEqual(obj.calculateMKAverage(), 6)

    def test_evict_from_mid(self):
        obj = MKAverage(3, 1)
        for v in [5, 1, 8]:        # 5 is oldest
            obj.addElement(v)
        # sorted=[1,5,8], low=[1], mid=[5], high=[8]
        self.assertEqual(obj.calculateMKAverage(), 5)
        obj.addElement(6)
        # evicts 5 (oldest, was in mid), window=[1,8,6], sorted=[1,6,8], mid=[6]
        self.assertEqual(obj.calculateMKAverage(), 6)

    def test_evict_from_high(self):
        obj = MKAverage(3, 1)
        for v in [8, 1, 5]:        # 8 is oldest
            obj.addElement(v)
        # sorted=[1,5,8], low=[1], mid=[5], high=[8]
        self.assertEqual(obj.calculateMKAverage(), 5)
        obj.addElement(3)
        # evicts 8 (oldest, in high), window=[1,5,3], sorted=[1,3,5], mid=[3]
        self.assertEqual(obj.calculateMKAverage(), 3)


class TestBoundaryShapes(unittest.TestCase):

    def test_single_mid_element(self):
        obj = MKAverage(5, 2)      # mid = 5-4 = 1 element
        for v in [1, 2, 3, 4, 5]:
            obj.addElement(v)
        # sorted=[1,2,3,4,5], low=[1,2], mid=[3], high=[4,5]
        self.assertEqual(obj.calculateMKAverage(), 3)
        obj.addElement(6)
        # evicts 1, window=[2,3,4,5,6], sorted=[2,3,4,5,6], mid=[4]
        self.assertEqual(obj.calculateMKAverage(), 4)

    def test_partition_sizes_maintained(self):
        obj = MKAverage(5, 2)
        for v in [10, 1, 8, 3, 6]:
            obj.addElement(v)
        # sorted=[1,3,6,8,10], low=[1,3], mid=[6], high=[8,10]
        self.assertEqual(obj.calculateMKAverage(), 6)
        obj.addElement(5)
        # evicts 10, window=[1,8,3,6,5], sorted=[1,3,5,6,8], mid=[5]
        self.assertEqual(obj.calculateMKAverage(), 5)


class TestMonotonicSequences(unittest.TestCase):

    def test_increasing(self):
        obj = MKAverage(3, 1)
        for v in [1, 2, 3]:
            obj.addElement(v)
        self.assertEqual(obj.calculateMKAverage(), 2)
        obj.addElement(4)
        self.assertEqual(obj.calculateMKAverage(), 3)   # window=[2,3,4]
        obj.addElement(5)
        self.assertEqual(obj.calculateMKAverage(), 4)   # window=[3,4,5]
        obj.addElement(100)
        # window=[4,5,100], sorted=[4,5,100], mid=[5]
        self.assertEqual(obj.calculateMKAverage(), 5)

    def test_decreasing(self):
        obj = MKAverage(3, 1)
        for v in [10, 9, 8]:
            obj.addElement(v)
        self.assertEqual(obj.calculateMKAverage(), 9)
        obj.addElement(7)
        self.assertEqual(obj.calculateMKAverage(), 8)   # window=[9,8,7]
        obj.addElement(6)
        self.assertEqual(obj.calculateMKAverage(), 7)   # window=[8,7,6]


if __name__ == "__main__":
    unittest.main()

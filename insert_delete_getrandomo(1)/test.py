import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(__file__))
from code import RandomizedCollection


class TestRandomizedCollection(unittest.TestCase):

    def setUp(self):
        self.rc = RandomizedCollection()

    def _assert_consistent(self, rc):
        for val, indices in rc.hashmap.items():
            for idx in indices:
                self.assertEqual(rc.lst[idx], val, f"hashmap[{val}] contains index {idx} but lst[{idx}]={rc.lst[idx]}")
        covered = set()
        for indices in rc.hashmap.values():
            covered |= indices
        self.assertEqual(covered, set(range(len(rc.lst))), "hashmap indices don't cover all lst positions")

    # --- insert ---

    def test_insert_new_value(self):
        self.assertTrue(self.rc.insert(5))
        self.assertIn(5, self.rc.lst)
        self.assertEqual(self.rc.hashmap[5], {0})
        self._assert_consistent(self.rc)

    def test_insert_duplicate(self):
        self.rc.insert(5)
        self.assertFalse(self.rc.insert(5))
        self.assertEqual(self.rc.lst.count(5), 2)
        self.assertEqual(len(self.rc.hashmap[5]), 2)
        self._assert_consistent(self.rc)

    def test_insert_after_full_removal(self):
        self.rc.insert(5)
        self.rc.remove(5)
        self.assertTrue(self.rc.insert(5))
        self._assert_consistent(self.rc)

    # --- remove ---

    def test_remove_nonexistent(self):
        self.assertFalse(self.rc.remove(99))
        self.assertEqual(self.rc.lst, [])
        self.assertEqual(len(self.rc.hashmap), 0)

    def test_remove_only_occurrence_is_last(self):
        self.rc.insert(5)
        self.assertTrue(self.rc.remove(5))
        self.assertEqual(self.rc.lst, [])
        self.assertNotIn(5, self.rc.hashmap)

    def test_remove_only_occurrence_triggers_swap(self):
        # lst=[5, 3], remove 5 — 3 swaps into index 0
        self.rc.insert(5)
        self.rc.insert(3)
        self.assertTrue(self.rc.remove(5))
        self.assertEqual(len(self.rc.lst), 1)
        self.assertEqual(self.rc.lst[0], 3)
        self.assertNotIn(5, self.rc.hashmap)
        self._assert_consistent(self.rc)

    def test_remove_one_of_two_occurrences(self):
        self.rc.insert(5)
        self.rc.insert(5)
        self.assertTrue(self.rc.remove(5))
        self.assertEqual(self.rc.lst.count(5), 1)
        self.assertEqual(len(self.rc.hashmap[5]), 1)
        self._assert_consistent(self.rc)

    def test_remove_all_occurrences(self):
        self.rc.insert(5)
        self.rc.insert(5)
        self.rc.remove(5)
        self._assert_consistent(self.rc)
        self.rc.remove(5)
        self.assertEqual(self.rc.lst, [])
        self.assertNotIn(5, self.rc.hashmap)

    def test_remove_single_element_collection(self):
        self.rc.insert(7)
        self.rc.remove(7)
        self.assertEqual(self.rc.lst, [])
        self.assertEqual(len(self.rc.hashmap), 0)

    def test_remove_same_value_swap(self):
        # lst=[5, 3, 5]: removing a 5 when last element is also 5
        self.rc.insert(5)
        self.rc.insert(3)
        self.rc.insert(5)
        self.assertEqual(self.rc.lst, [5, 3, 5])
        self.assertTrue(self.rc.remove(5))
        self.assertEqual(len(self.rc.lst), 2)
        self.assertEqual(self.rc.lst.count(5), 1)
        self.assertEqual(len(self.rc.hashmap[5]), 1)
        self._assert_consistent(self.rc)
        self.assertTrue(self.rc.remove(5))
        self.assertNotIn(5, self.rc.hashmap)
        self._assert_consistent(self.rc)

    # --- getRandom ---

    def test_get_random_empty(self):
        self.assertIsNone(self.rc.getRandom())

    def test_get_random_single_element(self):
        self.rc.insert(42)
        for _ in range(10):
            self.assertEqual(self.rc.getRandom(), 42)

    def test_get_random_distribution(self):
        # 5 inserted twice, 3 inserted once — expect ~2:1 ratio
        self.rc.insert(5)
        self.rc.insert(5)
        self.rc.insert(3)
        counts = {3: 0, 5: 0}
        for _ in range(9000):
            counts[self.rc.getRandom()] += 1
        self.assertAlmostEqual(counts[5] / 9000, 2/3, delta=0.05)
        self.assertAlmostEqual(counts[3] / 9000, 1/3, delta=0.05)


if __name__ == "__main__":
    unittest.main(verbosity=2)

import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(__file__))
from code import TaskManager, Priority


class TestAddTask(unittest.TestCase):

    def setUp(self):
        self.tm = TaskManager()

    def test_single_add(self):
        self.tm.add_task(1, 1, Priority.HIGH)
        self.assertIn(1, self.tm.map)

    def test_duplicate_raises_value_error(self):
        self.tm.add_task(1, 1, Priority.HIGH)
        with self.assertRaises(ValueError):
            self.tm.add_task(1, 1, Priority.LOW)

    def test_multiple_adds_all_present(self):
        self.tm.add_task(1, 1, Priority.HIGH)
        self.tm.add_task(2, 1, Priority.MEDIUM)
        self.tm.add_task(3, 1, Priority.LOW)
        self.assertEqual(self.tm.exec(), 1)
        self.assertEqual(self.tm.exec(), 2)
        self.assertEqual(self.tm.exec(), 3)


class TestEditTask(unittest.TestCase):

    def setUp(self):
        self.tm = TaskManager()

    def test_edit_changes_priority(self):
        self.tm.add_task(1, 1, Priority.LOW)
        self.tm.add_task(2, 1, Priority.MEDIUM)
        self.tm.edit_task(1, Priority.HIGH)
        self.assertEqual(self.tm.exec(), 1)

    def test_edit_unknown_raises_key_error(self):
        with self.assertRaises(KeyError):
            self.tm.edit_task(99, Priority.HIGH)

    def test_edit_preserves_insertion_order(self):
        # task 1 added before task 2; editing 1 to HIGH should not push it behind task 2
        self.tm.add_task(1, 1, Priority.LOW)
        self.tm.add_task(2, 1, Priority.HIGH)
        self.tm.edit_task(1, Priority.HIGH)
        self.assertEqual(self.tm.exec(), 1)
        self.assertEqual(self.tm.exec(), 2)
        self.assertIsNone(self.tm.exec())


class TestRemoveTask(unittest.TestCase):

    def setUp(self):
        self.tm = TaskManager()

    def test_remove_task_gone_from_exec(self):
        self.tm.add_task(1, 1, Priority.HIGH)
        self.tm.remove_task(1)
        self.assertIsNone(self.tm.exec())

    def test_remove_unknown_raises_key_error(self):
        with self.assertRaises(KeyError):
            self.tm.remove_task(99)

    def test_remove_middle_task_skipped(self):
        self.tm.add_task(1, 1, Priority.HIGH)
        self.tm.add_task(2, 1, Priority.MEDIUM)
        self.tm.add_task(3, 1, Priority.LOW)
        self.tm.remove_task(2)
        self.assertEqual(self.tm.exec(), 1)
        self.assertEqual(self.tm.exec(), 3)
        self.assertIsNone(self.tm.exec())


class TestExec(unittest.TestCase):

    def setUp(self):
        self.tm = TaskManager()

    def test_empty_returns_none(self):
        self.assertIsNone(self.tm.exec())

    def test_priority_ordering(self):
        self.tm.add_task(1, 1, Priority.LOW)
        self.tm.add_task(2, 1, Priority.MEDIUM)
        self.tm.add_task(3, 1, Priority.HIGH)
        self.assertEqual(self.tm.exec(), 3)
        self.assertEqual(self.tm.exec(), 2)
        self.assertEqual(self.tm.exec(), 1)

    def test_fifo_tie_breaking(self):
        self.tm.add_task(1, 1, Priority.HIGH)
        self.tm.add_task(2, 1, Priority.HIGH)
        self.assertEqual(self.tm.exec(), 1)
        self.assertEqual(self.tm.exec(), 2)

    def test_lazy_delete_skip(self):
        self.tm.add_task(1, 1, Priority.HIGH)
        self.tm.remove_task(1)
        self.tm.add_task(2, 1, Priority.LOW)
        self.assertEqual(self.tm.exec(), 2)
        self.assertIsNone(self.tm.exec())

    def test_stale_edit_entry_not_double_returned(self):
        self.tm.add_task(1, 1, Priority.LOW)
        self.tm.edit_task(1, Priority.HIGH)
        self.assertEqual(self.tm.exec(), 1)
        self.assertIsNone(self.tm.exec())

    def test_user_scenario(self):
        # add 1,2,3 as LOW; edit 3 to HIGH; add 4 as HIGH
        # expected exec order: 3, 4, 1, 2, None
        self.tm.add_task(1, 1, Priority.LOW)
        self.tm.add_task(2, 1, Priority.LOW)
        self.tm.add_task(3, 1, Priority.LOW)
        self.tm.edit_task(3, Priority.HIGH)
        self.tm.add_task(4, 1, Priority.HIGH)
        self.assertEqual(self.tm.exec(), 3)
        self.assertEqual(self.tm.exec(), 4)
        self.assertEqual(self.tm.exec(), 1)
        self.assertEqual(self.tm.exec(), 2)
        self.assertIsNone(self.tm.exec())


if __name__ == "__main__":
    unittest.main()

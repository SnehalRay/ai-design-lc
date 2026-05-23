import unittest
from code import CircularDeque


class TestIsEmpty(unittest.TestCase):
    def setUp(self): self.dq = CircularDeque(3)

    def test_empty_on_init(self):
        self.assertTrue(self.dq.isEmpty())

    def test_not_empty_after_insert(self):
        self.dq.insertFront(1)
        self.assertFalse(self.dq.isEmpty())

    def test_empty_after_full_drain(self):
        self.dq.insertFront(1); self.dq.insertFront(2); self.dq.insertFront(3)
        self.dq.removeFront(); self.dq.removeFront(); self.dq.removeFront()
        self.assertTrue(self.dq.isEmpty())


class TestIsFull(unittest.TestCase):
    def setUp(self): self.dq = CircularDeque(3)

    def test_not_full_on_init(self):
        self.assertFalse(self.dq.isFull())

    def test_full_after_capacity_inserts(self):
        self.dq.insertFront(1); self.dq.insertFront(2); self.dq.insertFront(3)
        self.assertTrue(self.dq.isFull())

    def test_not_full_after_remove(self):
        self.dq.insertFront(1); self.dq.insertFront(2); self.dq.insertFront(3)
        self.dq.removeFront()
        self.assertFalse(self.dq.isFull())


class TestInsertFront(unittest.TestCase):
    def setUp(self): self.dq = CircularDeque(3)

    def test_returns_true_on_success(self):
        self.assertTrue(self.dq.insertFront(1))

    def test_value_at_front(self):
        self.dq.insertFront(5)
        self.assertEqual(self.dq.getFront(), 5)

    def test_multiple_inserts_order(self):
        self.dq.insertFront(1); self.dq.insertFront(2)
        self.assertEqual(self.dq.getFront(), 2)
        self.assertEqual(self.dq.getBack(), 1)

    def test_returns_false_when_full(self):
        self.dq.insertFront(1); self.dq.insertFront(2); self.dq.insertFront(3)
        self.assertFalse(self.dq.insertFront(9))

    def test_size_increments(self):
        self.dq.insertFront(1)
        self.assertEqual(self.dq.size, 1)


class TestInsertBack(unittest.TestCase):
    def setUp(self): self.dq = CircularDeque(3)

    def test_returns_true_on_success(self):
        self.assertTrue(self.dq.insertBack(1))

    def test_value_at_back(self):
        self.dq.insertBack(5)
        self.assertEqual(self.dq.getBack(), 5)

    def test_multiple_inserts_order(self):
        self.dq.insertBack(1); self.dq.insertBack(2)
        self.assertEqual(self.dq.getBack(), 2)
        self.assertEqual(self.dq.getFront(), 1)

    def test_returns_false_when_full(self):
        self.dq.insertBack(1); self.dq.insertBack(2); self.dq.insertBack(3)
        self.assertFalse(self.dq.insertBack(9))

    def test_size_increments(self):
        self.dq.insertBack(1)
        self.assertEqual(self.dq.size, 1)


class TestRemoveFront(unittest.TestCase):
    def setUp(self): self.dq = CircularDeque(3)

    def test_returns_false_when_empty(self):
        self.assertFalse(self.dq.removeFront())

    def test_returns_true_on_success(self):
        self.dq.insertFront(1)
        self.assertTrue(self.dq.removeFront())

    def test_front_updates_after_remove(self):
        self.dq.insertFront(1); self.dq.insertFront(2)
        self.dq.removeFront()
        self.assertEqual(self.dq.getFront(), 1)

    def test_size_decrements(self):
        self.dq.insertFront(1)
        self.dq.removeFront()
        self.assertEqual(self.dq.size, 0)

    def test_single_element_both_ends_clear(self):
        self.dq.insertFront(1)
        self.dq.removeFront()
        self.assertEqual(self.dq.getFront(), -1)
        self.assertEqual(self.dq.getBack(), -1)


class TestRemoveBack(unittest.TestCase):
    def setUp(self): self.dq = CircularDeque(3)

    def test_returns_false_when_empty(self):
        self.assertFalse(self.dq.removeBack())

    def test_returns_true_on_success(self):
        self.dq.insertBack(1)
        self.assertTrue(self.dq.removeBack())

    def test_back_updates_after_remove(self):
        self.dq.insertBack(1); self.dq.insertBack(2)
        self.dq.removeBack()
        self.assertEqual(self.dq.getBack(), 1)

    def test_size_decrements(self):
        self.dq.insertBack(1)
        self.dq.removeBack()
        self.assertEqual(self.dq.size, 0)

    def test_single_element_both_ends_clear(self):
        self.dq.insertBack(1)
        self.dq.removeBack()
        self.assertEqual(self.dq.getFront(), -1)
        self.assertEqual(self.dq.getBack(), -1)


class TestGetFront(unittest.TestCase):
    def setUp(self): self.dq = CircularDeque(3)

    def test_returns_minus_one_when_empty(self):
        self.assertEqual(self.dq.getFront(), -1)

    def test_returns_front_value(self):
        self.dq.insertFront(7)
        self.assertEqual(self.dq.getFront(), 7)

    def test_not_affected_by_insertBack(self):
        self.dq.insertFront(1); self.dq.insertBack(2)
        self.assertEqual(self.dq.getFront(), 1)


class TestGetBack(unittest.TestCase):
    def setUp(self): self.dq = CircularDeque(3)

    def test_returns_minus_one_when_empty(self):
        self.assertEqual(self.dq.getBack(), -1)

    def test_returns_back_value(self):
        self.dq.insertBack(7)
        self.assertEqual(self.dq.getBack(), 7)

    def test_not_affected_by_insertFront(self):
        self.dq.insertBack(1); self.dq.insertFront(2)
        self.assertEqual(self.dq.getBack(), 1)


class TestCapacityOne(unittest.TestCase):
    def setUp(self): self.dq = CircularDeque(1)

    def test_insert_front_then_full(self):
        self.dq.insertFront(7)
        self.assertTrue(self.dq.isFull())

    def test_insert_back_fails_when_full(self):
        self.dq.insertFront(7)
        self.assertFalse(self.dq.insertBack(8))

    def test_remove_and_reinsert(self):
        self.dq.insertFront(7)
        self.dq.removeFront()
        self.assertTrue(self.dq.insertBack(8))

    def test_front_equals_back(self):
        self.dq.insertFront(7)
        self.assertEqual(self.dq.getFront(), self.dq.getBack())


if __name__ == "__main__":
    unittest.main()

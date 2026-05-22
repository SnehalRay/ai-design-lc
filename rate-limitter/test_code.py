import unittest
from collections import deque
from code import RateLimiter


class TestQueuePop(unittest.TestCase):
    def setUp(self):
        self.rl = RateLimiter(window_size=10, max_length=5)

    def test_empty_queue(self):
        q = deque()
        self.rl._queue_pop(q, 10)
        self.assertEqual(len(q), 0)

    def test_none_expired(self):
        q = deque([1, 2, 3])
        self.rl._queue_pop(q, 5)
        self.assertEqual(list(q), [1, 2, 3])

    def test_all_expired(self):
        q = deque([1, 2, 3])
        self.rl._queue_pop(q, 15)
        self.assertEqual(len(q), 0)

    def test_partial_expire(self):
        q = deque([1, 5, 9])
        self.rl._queue_pop(q, 11)
        self.assertEqual(list(q), [5, 9])

    def test_exact_boundary(self):
        # diff == window_size → expired
        q = deque([1])
        self.rl._queue_pop(q, 11)
        self.assertEqual(len(q), 0)

    def test_just_inside_boundary(self):
        # diff == window_size - 1 → not expired
        q = deque([2])
        self.rl._queue_pop(q, 11)
        self.assertEqual(list(q), [2])


class TestAddingData(unittest.TestCase):
    def setUp(self):
        self.rl = RateLimiter(window_size=10, max_length=5)

    def test_new_user_allowed(self):
        self.assertTrue(self.rl.adding_data("alice", 1))

    def test_fill_to_limit(self):
        results = [self.rl.adding_data("alice", 1) for _ in range(5)]
        self.assertEqual(results, [True] * 5)

    def test_over_limit_rejected(self):
        for _ in range(5):
            self.rl.adding_data("alice", 1)
        self.assertFalse(self.rl.adding_data("alice", 1))

    def test_window_expiry_allows_new_request(self):
        for _ in range(5):
            self.rl.adding_data("alice", 1)
        # t=11: diff from t=1 is 10 >= window_size, so all old entries expire
        self.assertTrue(self.rl.adding_data("alice", 11))

    def test_users_tracked_independently(self):
        for _ in range(5):
            self.rl.adding_data("alice", 1)
        # alice is at limit, bob is fresh
        self.assertFalse(self.rl.adding_data("alice", 1))
        self.assertTrue(self.rl.adding_data("bob", 1))

    def test_max_length_zero(self):
        rl = RateLimiter(window_size=10, max_length=0)
        self.assertFalse(rl.adding_data("alice", 1))

    def test_max_length_one(self):
        rl = RateLimiter(window_size=10, max_length=1)
        self.assertTrue(rl.adding_data("alice", 1))
        self.assertFalse(rl.adding_data("alice", 5))   # within window
        self.assertTrue(rl.adding_data("alice", 11))   # window expired

    def test_exact_boundary_expires(self):
        for _ in range(5):
            self.rl.adding_data("alice", 1)
        # diff == window_size exactly → entries at t=1 expire
        self.assertTrue(self.rl.adding_data("alice", 11))

    def test_same_timestamp_burst(self):
        for _ in range(5):
            self.rl.adding_data("alice", 1)
        self.assertFalse(self.rl.adding_data("alice", 1))


if __name__ == "__main__":
    unittest.main()

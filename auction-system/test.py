import unittest
from code import AuctionSystem


class TestAddBid(unittest.TestCase):

    def setUp(self):
        self.a = AuctionSystem()

    def test_add_first_bid(self):
        self.a.addBid(1, 101, 100)
        self.assertEqual(self.a.getHighestBidder(101), 1)

    def test_add_multiple_users_highest_wins(self):
        self.a.addBid(1, 101, 100)
        self.a.addBid(2, 101, 200)
        self.assertEqual(self.a.getHighestBidder(101), 2)

    def test_add_same_user_replaces_and_wins(self):
        self.a.addBid(1, 101, 100)
        self.a.addBid(1, 101, 300)
        self.assertEqual(self.a.getHighestBidder(101), 1)
        self.assertEqual(self.a.bids[101][1], 300)

    def test_add_first_bid_any_amount_ok(self):
        self.a.addBid(1, 101, 1)
        self.assertEqual(self.a.getHighestBidder(101), 1)

    def test_add_bid_equal_to_highest_raises(self):
        self.a.addBid(1, 101, 100)
        with self.assertRaises(ValueError):
            self.a.addBid(2, 101, 100)

    def test_add_bid_below_highest_raises(self):
        self.a.addBid(1, 101, 100)
        with self.assertRaises(ValueError):
            self.a.addBid(2, 101, 50)


class TestUpdateBid(unittest.TestCase):

    def setUp(self):
        self.a = AuctionSystem()

    def test_update_transfers_lead(self):
        self.a.addBid(1, 101, 100)
        self.a.addBid(2, 101, 150)
        self.a.updateBid(1, 101, 200)
        self.assertEqual(self.a.getHighestBidder(101), 1)

    def test_full_sequence(self):
        # user1 bids 10, user2 bids 15, user1 updates 20, user2 updates 21, user2 removes
        self.a.addBid(1, 1, 10)
        self.a.addBid(2, 1, 15)
        self.a.updateBid(1, 1, 20)
        self.a.updateBid(2, 1, 21)
        self.a.removeBid(2, 1)
        self.assertEqual(self.a.getHighestBidder(1), 1)

    def test_update_nonexistent_user_raises(self):
        self.a.addBid(1, 101, 100)
        with self.assertRaises(KeyError):
            self.a.updateBid(99, 101, 200)

    def test_update_nonexistent_item_raises(self):
        with self.assertRaises(KeyError):
            self.a.updateBid(1, 999, 200)

    def test_update_equal_to_highest_raises(self):
        self.a.addBid(1, 101, 100)
        with self.assertRaises(ValueError):
            self.a.updateBid(1, 101, 100)

    def test_update_below_highest_raises(self):
        self.a.addBid(1, 101, 100)
        with self.assertRaises(ValueError):
            self.a.updateBid(1, 101, 50)


class TestRemoveBid(unittest.TestCase):

    def setUp(self):
        self.a = AuctionSystem()

    def test_remove_non_highest_winner_unchanged(self):
        self.a.addBid(1, 101, 100)
        self.a.addBid(2, 101, 200)
        self.a.removeBid(1, 101)
        self.assertEqual(self.a.getHighestBidder(101), 2)

    def test_remove_highest_falls_back_to_next(self):
        self.a.addBid(1, 101, 100)
        self.a.addBid(2, 101, 200)
        self.a.removeBid(2, 101)
        self.assertEqual(self.a.getHighestBidder(101), 1)

    def test_remove_all_bids_returns_minus1(self):
        self.a.addBid(1, 101, 100)
        self.a.removeBid(1, 101)
        self.assertEqual(self.a.getHighestBidder(101), -1)

    def test_remove_then_readd_no_hard_condition(self):
        # After all bids removed, heap is exhausted; next addBid faces no minimum
        self.a.addBid(1, 101, 100)
        self.a.removeBid(1, 101)
        self.a.addBid(2, 101, 50)
        self.assertEqual(self.a.getHighestBidder(101), 2)


class TestGetHighestBidder(unittest.TestCase):

    def setUp(self):
        self.a = AuctionSystem()

    def test_unknown_item_returns_minus1(self):
        self.assertEqual(self.a.getHighestBidder(999), -1)

    def test_empty_after_all_removed_returns_minus1(self):
        self.a.addBid(1, 101, 100)
        self.a.addBid(2, 101, 200)
        self.a.removeBid(2, 101)
        self.a.removeBid(1, 101)
        self.assertEqual(self.a.getHighestBidder(101), -1)


class TestMultiItemIsolation(unittest.TestCase):

    def test_items_do_not_interfere(self):
        a = AuctionSystem()
        a.addBid(1, 101, 100)
        a.addBid(2, 202, 200)
        self.assertEqual(a.getHighestBidder(101), 1)
        self.assertEqual(a.getHighestBidder(202), 2)

    def test_remove_from_one_item_leaves_other_intact(self):
        a = AuctionSystem()
        a.addBid(1, 101, 100)
        a.addBid(2, 202, 200)
        a.removeBid(1, 101)
        self.assertEqual(a.getHighestBidder(101), -1)
        self.assertEqual(a.getHighestBidder(202), 2)


class TestLazyDeletionStress(unittest.TestCase):

    def test_many_stale_entries_cleared_correctly(self):
        a = AuctionSystem()
        a.addBid(1, 101, 100)
        # Five updates leave five stale heap entries for user1
        a.updateBid(1, 101, 200)
        a.updateBid(1, 101, 300)
        a.updateBid(1, 101, 400)
        a.updateBid(1, 101, 500)
        a.updateBid(1, 101, 600)
        # Remove user1 entirely; heap still holds all six entries as stale
        a.removeBid(1, 101)
        # New low bid should succeed (no valid highest bid exists)
        a.addBid(2, 101, 50)
        self.assertEqual(a.getHighestBidder(101), 2)


if __name__ == "__main__":
    unittest.main()

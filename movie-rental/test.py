import unittest
from code import MovieRentingCompany

BASE_ENTRIES = [
    [0, 1, 5],
    [0, 2, 8],
    [1, 1, 3],
    [1, 2, 6],
    [2, 1, 10],
    [2, 2, 4],
]

SIX_SHOP_ENTRIES = BASE_ENTRIES + [
    [3, 1, 7],
    [4, 1, 2],
    [5, 1, 9],
    [6, 1, 1],
]

PRICE_TIE_ENTRIES = [
    [0, 1, 5],
    [1, 1, 5],
    [2, 1, 5],
]


class TestSearch(unittest.TestCase):

    def setUp(self):
        self.system = MovieRentingCompany(BASE_ENTRIES)

    def test_basic_sorted_by_price(self):
        self.assertEqual(self.system.search(1), [1, 0, 2])

    def test_returns_at_most_5(self):
        system = MovieRentingCompany(SIX_SHOP_ENTRIES)
        result = system.search(1)
        self.assertEqual(len(result), 5)
        self.assertEqual(result, [6, 4, 1, 0, 3])

    def test_price_tie_smaller_shop_first(self):
        system = MovieRentingCompany(PRICE_TIE_ENTRIES)
        self.assertEqual(system.search(1), [0, 1, 2])

    def test_all_copies_rented_returns_empty(self):
        self.system.rent(0, 1)
        self.system.rent(1, 1)
        self.system.rent(2, 1)
        self.assertEqual(self.system.search(1), [])

    def test_nonexistent_movie_returns_empty(self):
        self.assertEqual(self.system.search(999), [])

    def test_single_shop(self):
        system = MovieRentingCompany([[0, 5, 20]])
        self.assertEqual(system.search(5), [0])


class TestRent(unittest.TestCase):

    def setUp(self):
        self.system = MovieRentingCompany(BASE_ENTRIES)

    def test_valid_rent_added_to_rented(self):
        self.system.rent(1, 1)
        self.assertIn((3, 1, 1), self.system.rented)

    def test_rent_hides_shop_from_search(self):
        self.system.rent(1, 1)
        self.assertNotIn(1, self.system.search(1))

    def test_rent_idempotent(self):
        self.system.rent(1, 1)
        self.system.rent(1, 1)
        count = sum(1 for t in self.system.rented if t == (3, 1, 1))
        self.assertEqual(count, 1)

    def test_rent_nonexistent_movie_no_crash(self):
        self.system.rent(0, 999)
        self.assertEqual(len(self.system.rented), 0)

    def test_rent_nonexistent_shop_no_crash(self):
        self.system.rent(99, 1)
        self.assertEqual(len(self.system.rented), 0)


class TestDrop(unittest.TestCase):

    def setUp(self):
        self.system = MovieRentingCompany(BASE_ENTRIES)

    def test_valid_drop_removed_from_rented(self):
        self.system.rent(1, 1)
        self.system.drop(1, 1)
        self.assertNotIn((3, 1, 1), self.system.rented)

    def test_drop_restores_shop_to_search(self):
        self.system.rent(1, 1)
        self.system.drop(1, 1)
        self.assertIn(1, self.system.search(1))

    def test_drop_non_rented_no_crash(self):
        self.system.drop(1, 1)
        self.assertEqual(len(self.system.rented), 0)

    def test_drop_nonexistent_movie_no_crash(self):
        self.system.drop(0, 999)

    def test_drop_nonexistent_shop_no_crash(self):
        self.system.drop(99, 1)


class TestReport(unittest.TestCase):

    def setUp(self):
        self.system = MovieRentingCompany(BASE_ENTRIES)

    def test_nothing_rented_returns_empty(self):
        self.assertEqual(self.system.report(), [])

    def test_fewer_than_5_returns_all(self):
        self.system.rent(1, 1)
        self.system.rent(2, 2)
        self.assertEqual(self.system.report(), [[1, 1], [2, 2]])

    def test_more_than_5_returns_cheapest_5(self):
        system = MovieRentingCompany(SIX_SHOP_ENTRIES)
        for shop in [6, 4, 1, 0, 3, 5]:
            system.rent(shop, 1)
        result = system.report()
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0], [6, 1])

    def test_price_tie_smaller_shop_first(self):
        system = MovieRentingCompany(PRICE_TIE_ENTRIES + [[0, 2, 5], [1, 2, 5]])
        system.rent(0, 1)
        system.rent(1, 1)
        result = system.report()
        self.assertEqual(result[0], [0, 1])
        self.assertEqual(result[1], [1, 1])

    def test_price_shop_tie_smaller_movie_first(self):
        system = MovieRentingCompany([[0, 1, 5], [0, 2, 5]])
        system.rent(0, 1)
        system.rent(0, 2)
        result = system.report()
        self.assertEqual(result[0], [0, 1])
        self.assertEqual(result[1], [0, 2])

    def test_format_is_shop_then_movie(self):
        self.system.rent(1, 1)
        result = self.system.report()
        self.assertEqual(result, [[1, 1]])


class TestIntegration(unittest.TestCase):

    def setUp(self):
        self.system = MovieRentingCompany(BASE_ENTRIES)

    def test_rent_drop_cycle(self):
        self.assertIn(1, self.system.search(1))
        self.system.rent(1, 1)
        self.assertNotIn(1, self.system.search(1))
        self.system.drop(1, 1)
        self.assertIn(1, self.system.search(1))

    def test_report_reflects_live_state(self):
        self.system.rent(1, 1)
        self.assertEqual(self.system.report(), [[1, 1]])
        self.system.rent(2, 2)
        self.assertEqual(self.system.report(), [[1, 1], [2, 2]])
        self.system.drop(1, 1)
        self.assertEqual(self.system.report(), [[2, 2]])


if __name__ == "__main__":
    unittest.main()

import unittest
from code import Movie, MovieRentalSystem


class TestMovie(unittest.TestCase):

    def test_getters(self):
        m = Movie("Inception", 2.99, 1, 5)
        self.assertEqual(m.name, "Inception")
        self.assertEqual(m.price, 2.99)
        self.assertEqual(m.store_id, 1)
        self.assertEqual(m.qty, 5)

    def test_setters(self):
        m = Movie("Inception", 2.99, 1, 5)
        m.name = "Dunkirk"
        m.price = 3.99
        m.store_id = 2
        m.qty = 10
        self.assertEqual(m.name, "Dunkirk")
        self.assertEqual(m.price, 3.99)
        self.assertEqual(m.store_id, 2)
        self.assertEqual(m.qty, 10)

    def test_negative_price_raises(self):
        with self.assertRaises(ValueError):
            Movie("Inception", -1.0, 1, 5)

    def test_negative_qty_raises(self):
        m = Movie("Inception", 2.99, 1, 5)
        with self.assertRaises(ValueError):
            m.qty = -1

    def test_zero_price_allowed(self):
        m = Movie("Free Movie", 0.0, 1, 1)
        self.assertEqual(m.price, 0.0)

    def test_zero_qty_allowed(self):
        m = Movie("Inception", 2.99, 1, 0)
        self.assertEqual(m.qty, 0)


class TestAddStores(unittest.TestCase):

    def setUp(self):
        self.rs = MovieRentalSystem()

    def test_add_new_store(self):
        self.assertTrue(self.rs.add_stores(1))
        self.assertIn(1, self.rs._stores)

    def test_add_duplicate_store(self):
        self.rs.add_stores(1)
        self.assertFalse(self.rs.add_stores(1))

    def test_add_multiple_stores(self):
        self.rs.add_stores(1)
        self.rs.add_stores(2)
        self.rs.add_stores(3)
        self.assertEqual(len(self.rs._stores), 3)


class TestAddMovie(unittest.TestCase):

    def setUp(self):
        self.rs = MovieRentalSystem()
        self.rs.add_stores(1)
        self.rs.add_stores(2)

    def test_add_movie_valid_store(self):
        self.assertTrue(self.rs.add_movie("Inception", 1, 2.99, 3))
        self.assertIn("Inception", self.rs._movies)
        self.assertEqual(self.rs._movies["Inception"][1].qty, 3)

    def test_add_movie_invalid_store(self):
        self.assertFalse(self.rs.add_movie("Inception", 99, 2.99, 3))
        self.assertNotIn("Inception", self.rs._movies)

    def test_add_same_movie_same_store_increments_qty(self):
        self.rs.add_movie("Inception", 1, 2.99, 3)
        self.rs.add_movie("Inception", 1, 2.99, 2)
        self.assertEqual(self.rs._movies["Inception"][1].qty, 5)

    def test_add_same_movie_different_stores(self):
        self.rs.add_movie("Inception", 1, 2.99, 3)
        self.rs.add_movie("Inception", 2, 4.50, 1)
        self.assertIn(1, self.rs._movies["Inception"])
        self.assertIn(2, self.rs._movies["Inception"])

    def test_add_different_movies_same_store(self):
        self.rs.add_movie("Inception", 1, 2.99, 3)
        self.rs.add_movie("Dunkirk", 1, 3.49, 2)
        self.assertIn("Inception", self.rs._movies)
        self.assertIn("Dunkirk", self.rs._movies)


class TestSearchMovies(unittest.TestCase):

    def setUp(self):
        self.rs = MovieRentalSystem()
        self.rs.add_stores(1)
        self.rs.add_stores(2)
        self.rs.add_stores(3)
        self.rs.add_stores(4)
        self.rs.add_stores(5)
        self.rs.add_stores(6)

    def test_search_nonexistent_movie(self):
        self.assertEqual(self.rs.search_movies("Ghost"), [])

    def test_search_returns_sorted_by_price(self):
        self.rs.add_movie("Inception", 1, 4.99, 2)
        self.rs.add_movie("Inception", 2, 2.99, 2)
        self.rs.add_movie("Inception", 3, 3.49, 2)
        results = self.rs.search_movies("Inception")
        prices = [m.price for m in results]
        self.assertEqual(prices, sorted(prices))

    def test_search_returns_at_most_5(self):
        for i in range(1, 7):
            self.rs.add_movie("Inception", i, float(i), 1)
        results = self.rs.search_movies("Inception")
        self.assertEqual(len(results), 5)
        self.assertEqual(results[0].price, 1.0)

    def test_search_returns_all_when_fewer_than_5(self):
        self.rs.add_movie("Inception", 1, 2.99, 2)
        self.rs.add_movie("Inception", 2, 4.50, 1)
        results = self.rs.search_movies("Inception")
        self.assertEqual(len(results), 2)

    def test_search_single_store(self):
        self.rs.add_movie("Dunkirk", 1, 3.49, 2)
        results = self.rs.search_movies("Dunkirk")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].store_id, 1)


class TestRentMovie(unittest.TestCase):

    def setUp(self):
        self.rs = MovieRentalSystem()
        self.rs.add_stores(1)
        self.rs.add_movie("Inception", 1, 2.99, 3)

    def test_rent_decrements_qty(self):
        self.rs.rent_movie("Inception", 1, userId=1)
        self.assertEqual(self.rs._movies["Inception"][1].qty, 2)

    def test_rent_adds_to_user_rented(self):
        self.rs.rent_movie("Inception", 1, userId=1)
        self.assertIn("Inception", self.rs._user_rented[1])

    def test_rent_same_movie_twice_same_user_is_noop(self):
        self.rs.rent_movie("Inception", 1, userId=1)
        self.rs.rent_movie("Inception", 1, userId=1)
        self.assertEqual(self.rs._movies["Inception"][1].qty, 2)

    def test_rent_out_of_stock(self):
        self.rs.add_movie("Dunkirk", 1, 3.49, 0)
        self.rs.rent_movie("Dunkirk", 1, userId=1)
        self.assertNotIn("Dunkirk", self.rs._user_rented.get(1, {}))

    def test_rent_nonexistent_movie(self):
        self.rs.rent_movie("Ghost", 1, userId=1)
        self.assertNotIn("Ghost", self.rs._user_rented.get(1, {}))

    def test_rent_nonexistent_store(self):
        self.rs.rent_movie("Inception", 99, userId=1)
        self.assertNotIn("Inception", self.rs._user_rented.get(1, {}))

    def test_two_users_can_rent_same_movie(self):
        self.rs.rent_movie("Inception", 1, userId=1)
        self.rs.rent_movie("Inception", 1, userId=2)
        self.assertIn("Inception", self.rs._user_rented[1])
        self.assertIn("Inception", self.rs._user_rented[2])
        self.assertEqual(self.rs._movies["Inception"][1].qty, 1)

    def test_rent_exhausts_stock_for_third_user(self):
        self.rs.rent_movie("Inception", 1, userId=1)
        self.rs.rent_movie("Inception", 1, userId=2)
        self.rs.rent_movie("Inception", 1, userId=3)
        self.rs.rent_movie("Inception", 1, userId=4)  # qty now 0, should fail
        self.assertNotIn("Inception", self.rs._user_rented.get(4, {}))
        self.assertEqual(self.rs._movies["Inception"][1].qty, 0)


class TestReturnMovie(unittest.TestCase):

    def setUp(self):
        self.rs = MovieRentalSystem()
        self.rs.add_stores(1)
        self.rs.add_movie("Inception", 1, 2.99, 3)

    def test_return_increments_qty(self):
        self.rs.rent_movie("Inception", 1, userId=1)
        self.rs.return_movie("Inception", 1, userId=1)
        self.assertEqual(self.rs._movies["Inception"][1].qty, 3)

    def test_return_removes_from_user_rented(self):
        self.rs.rent_movie("Inception", 1, userId=1)
        self.rs.return_movie("Inception", 1, userId=1)
        self.assertNotIn("Inception", self.rs._user_rented.get(1, {}))

    def test_return_movie_never_rented_is_noop(self):
        self.rs.return_movie("Inception", 1, userId=1)
        self.assertEqual(self.rs._movies["Inception"][1].qty, 3)

    def test_return_for_unknown_user_is_noop(self):
        self.rs.return_movie("Inception", 1, userId=999)
        self.assertEqual(self.rs._movies["Inception"][1].qty, 3)

    def test_return_twice_is_noop_on_second(self):
        self.rs.rent_movie("Inception", 1, userId=1)
        self.rs.return_movie("Inception", 1, userId=1)
        self.rs.return_movie("Inception", 1, userId=1)
        self.assertEqual(self.rs._movies["Inception"][1].qty, 3)


class TestReport(unittest.TestCase):

    def setUp(self):
        self.rs = MovieRentalSystem()
        self.rs.add_stores(1)
        self.rs.add_stores(2)

    def test_report_empty_system(self):
        result = self.rs.report()
        self.assertEqual(result, "Top 5 Cheapest Movies:")

    def test_report_shows_at_most_5(self):
        self.rs.add_stores(3)
        self.rs.add_stores(4)
        self.rs.add_stores(5)
        self.rs.add_stores(6)
        for i, (name, price) in enumerate([
            ("A", 1.0), ("B", 2.0), ("C", 3.0),
            ("D", 4.0), ("E", 5.0), ("F", 6.0)
        ], 1):
            self.rs.add_movie(name, i, price, 1)
        lines = self.rs.report().split("\n")
        self.assertEqual(len(lines), 6)  # header + 5 movies

    def test_report_sorted_cheapest_first(self):
        self.rs.add_movie("Inception", 1, 4.99, 1)
        self.rs.add_movie("Dunkirk", 2, 1.99, 1)
        report = self.rs.report()
        lines = report.split("\n")
        self.assertIn("Dunkirk", lines[1])
        self.assertIn("Inception", lines[2])

    def test_report_format(self):
        self.rs.add_movie("Inception", 1, 2.99, 3)
        report = self.rs.report()
        self.assertIn("Inception", report)
        self.assertIn("Store 1", report)
        self.assertIn("$2.99", report)

    def test_report_fewer_than_5(self):
        self.rs.add_movie("Inception", 1, 2.99, 3)
        self.rs.add_movie("Dunkirk", 2, 3.49, 2)
        lines = self.rs.report().split("\n")
        self.assertEqual(len(lines), 3)  # header + 2 movies


if __name__ == "__main__":
    unittest.main()

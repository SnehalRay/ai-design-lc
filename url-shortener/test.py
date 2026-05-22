import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from code import URLShortener

class TestURLShortener(unittest.TestCase):

    def setUp(self):
        self.shortener = URLShortener()

    # --- add_URL ---

    def test_add_url_returns_valid_short_url(self):
        short = self.shortener.add_URL("https://example.com")
        self.assertTrue(short.startswith("https://www.tinyURL/"))
        suffix = short[len("https://www.tinyURL/"):]
        self.assertEqual(len(suffix), 6)
        self.assertTrue(suffix.isalnum())

    def test_add_url_idempotent(self):
        short1 = self.shortener.add_URL("https://example.com")
        short2 = self.shortener.add_URL("https://example.com")
        self.assertEqual(short1, short2)

    def test_add_url_different_urls_get_different_short_urls(self):
        short1 = self.shortener.add_URL("https://example.com")
        short2 = self.shortener.add_URL("https://other.com")
        self.assertNotEqual(short1, short2)

    # --- get_long_url ---

    def test_get_long_url_valid(self):
        short = self.shortener.add_URL("https://example.com")
        self.assertEqual(self.shortener.get_long_url(short), "https://example.com")

    def test_get_long_url_unknown_returns_none(self):
        self.assertIsNone(self.shortener.get_long_url("https://www.tinyURL/xxxxxx"))

    # --- get_short_url ---

    def test_get_short_url_known(self):
        short = self.shortener.add_URL("https://example.com")
        self.assertEqual(self.shortener.get_short_url("https://example.com"), short)

    def test_get_short_url_unknown_returns_none(self):
        self.assertIsNone(self.shortener.get_short_url("https://never-added.com"))

    # --- existence checks ---

    def test_long_url_exists_before_and_after(self):
        self.assertFalse(self.shortener.long_url_exists("https://example.com"))
        self.shortener.add_URL("https://example.com")
        self.assertTrue(self.shortener.long_url_exists("https://example.com"))

    def test_short_url_exists(self):
        self.assertFalse(self.shortener.short_url_exists("https://www.tinyURL/abcdef"))
        short = self.shortener.add_URL("https://example.com")
        self.assertTrue(self.shortener.short_url_exists(short))

    def test_url_exists_for_both_long_and_short(self):
        short = self.shortener.add_URL("https://example.com")
        self.assertTrue(self.shortener.url_exists("https://example.com"))
        self.assertTrue(self.shortener.url_exists(short))

    # --- bidirectional consistency ---

    def test_bidirectional_consistency(self):
        long = "https://example.com"
        short = self.shortener.add_URL(long)
        self.assertEqual(self.shortener.long_to_short[long], short)
        self.assertEqual(self.shortener.short_to_long[short], long)

    # --- edge cases ---

    def test_get_long_url_empty_string(self):
        self.assertIsNone(self.shortener.get_long_url(""))

    def test_get_short_url_empty_string(self):
        self.assertIsNone(self.shortener.get_short_url(""))

    def test_bulk_uniqueness(self):
        urls = [f"https://example.com/page{i}" for i in range(100)]
        short_urls = [self.shortener.add_URL(url) for url in urls]
        self.assertEqual(len(short_urls), len(set(short_urls)))


if __name__ == "__main__":
    unittest.main()

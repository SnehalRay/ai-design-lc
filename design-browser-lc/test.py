import unittest
from code import BrowserHistory


class TestBrowserHistory(unittest.TestCase):

    def setUp(self):
        self.bh = BrowserHistory()

    def test_init(self):
        self.assertEqual(self.bh.current.url, "home")

    def test_visit(self):
        self.bh.visit("google.com")
        self.assertEqual(self.bh.current.url, "google.com")

    def test_visit_clears_forward(self):
        self.bh.visit("google.com")
        self.bh.visit("youtube.com")
        self.bh.back(1)
        self.bh.visit("reddit.com")
        self.assertEqual(self.bh.forward(1), "reddit.com")  # no forward exists

    def test_back_normal(self):
        self.bh.visit("google.com")
        self.bh.visit("youtube.com")
        self.bh.visit("facebook.com")
        self.assertEqual(self.bh.back(1), "youtube.com")

    def test_back_clamped(self):
        self.bh.visit("google.com")
        self.bh.visit("youtube.com")
        self.assertEqual(self.bh.back(100), "home")

    def test_back_at_homepage(self):
        self.assertEqual(self.bh.back(1), "home")

    def test_forward_normal(self):
        self.bh.visit("google.com")
        self.bh.visit("youtube.com")
        self.bh.back(2)
        self.assertEqual(self.bh.forward(1), "google.com")

    def test_forward_clamped(self):
        self.bh.visit("google.com")
        self.bh.visit("youtube.com")
        self.assertEqual(self.bh.forward(100), "youtube.com")

    def test_forward_no_history(self):
        self.assertEqual(self.bh.forward(1), "home")

    def test_back_then_forward_roundtrip(self):
        self.bh.visit("google.com")
        self.bh.visit("youtube.com")
        self.bh.visit("facebook.com")
        self.bh.back(2)
        self.assertEqual(self.bh.forward(2), "facebook.com")


if __name__ == "__main__":
    unittest.main()
import unittest
from code import AuthenticationManager


class TestGenerate(unittest.TestCase):

    def test_basic_generate(self):
        auth = AuthenticationManager(5)
        auth.generate("aaa", 1)
        self.assertEqual(auth.tokens["aaa"], 6)

    def test_generate_overwrites_existing(self):
        auth = AuthenticationManager(5)
        auth.generate("aaa", 1)   # expiry = 6
        auth.generate("aaa", 10)  # overwrite → expiry = 15
        self.assertEqual(auth.tokens["aaa"], 15)

    def test_generate_overwrites_expired_token(self):
        auth = AuthenticationManager(5)
        auth.generate("aaa", 1)   # expiry = 6
        auth.generate("aaa", 20)  # re-generate after expiry → expiry = 25
        self.assertEqual(auth.tokens["aaa"], 25)


class TestRenew(unittest.TestCase):

    def test_renew_valid_token(self):
        auth = AuthenticationManager(5)
        auth.generate("aaa", 1)   # expiry = 6
        auth.renew("aaa", 3)      # 6 > 3, valid → expiry = 8
        self.assertEqual(auth.tokens["aaa"], 8)

    def test_renew_nonexistent_token_is_noop(self):
        auth = AuthenticationManager(5)
        auth.renew("ghost", 1)    # never generated, no-op
        self.assertNotIn("ghost", auth.tokens)

    def test_renew_expired_token_is_noop(self):
        auth = AuthenticationManager(5)
        auth.generate("aaa", 1)   # expiry = 6
        auth.renew("aaa", 7)      # 6 <= 7, expired → no-op
        self.assertEqual(auth.tokens["aaa"], 6)

    def test_renew_at_exact_expiry_is_noop(self):
        # token expiring at t=6, renew called at t=6 → already expired
        auth = AuthenticationManager(5)
        auth.generate("aaa", 1)   # expiry = 6
        auth.renew("aaa", 6)      # 6 <= 6 → no-op
        self.assertEqual(auth.tokens["aaa"], 6)


class TestCountUnexpiredTokens(unittest.TestCase):

    def test_count_all_unexpired(self):
        auth = AuthenticationManager(5)
        auth.generate("aaa", 1)   # expiry = 6
        auth.generate("bbb", 1)   # expiry = 6
        self.assertEqual(auth.countUnexpiredTokens(3), 2)

    def test_count_some_expired(self):
        auth = AuthenticationManager(5)
        auth.generate("aaa", 1)   # expiry = 6
        auth.generate("bbb", 5)   # expiry = 10
        self.assertEqual(auth.countUnexpiredTokens(7), 1)  # only bbb alive

    def test_count_all_expired(self):
        auth = AuthenticationManager(5)
        auth.generate("aaa", 1)   # expiry = 6
        auth.generate("bbb", 1)   # expiry = 6
        self.assertEqual(auth.countUnexpiredTokens(10), 0)

    def test_count_at_exact_expiry_is_zero(self):
        # token at expiry time is considered expired
        auth = AuthenticationManager(5)
        auth.generate("aaa", 1)   # expiry = 6
        self.assertEqual(auth.countUnexpiredTokens(6), 0)

    def test_count_empty(self):
        auth = AuthenticationManager(5)
        self.assertEqual(auth.countUnexpiredTokens(1), 0)


class TestLeetCodeExample(unittest.TestCase):
    # Mirrors the official example from the problem statement

    def test_full_sequence(self):
        auth = AuthenticationManager(5)
        auth.generate("aaa", 1)
        auth.renew("aaa", 2)
        self.assertEqual(auth.countUnexpiredTokens(6), 1)
        auth.generate("bbb", 7)
        auth.renew("aaa", 8)   # aaa expired at 7 (renewed to 7) → no-op
        self.assertEqual(auth.countUnexpiredTokens(8), 1)  # only bbb alive


if __name__ == "__main__":
    unittest.main(verbosity=2)

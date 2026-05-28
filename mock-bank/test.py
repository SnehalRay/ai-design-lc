import unittest
from code import (
    BankSystem, TransactionType,
    AccountAlreadyExistsError, AccountNotFoundError,
    NegativeAmountError, InsufficientFundsError,
)


class TestCreateAccount(unittest.TestCase):

    def setUp(self):
        self.bank = BankSystem()

    def test_returns_string_id(self):
        aid = self.bank.create_account(1234567890, "Alice")
        self.assertIsInstance(aid, str)
        self.assertTrue(len(aid) > 0)

    def test_unique_ids(self):
        a1 = self.bank.create_account(1111111111, "Alice")
        a2 = self.bank.create_account(2222222222, "Bob")
        self.assertNotEqual(a1, a2)

    def test_duplicate_raises(self):
        self.bank.create_account(1234567890, "Alice")
        with self.assertRaises(AccountAlreadyExistsError):
            self.bank.create_account(1234567890, "Alice")

    def test_same_phone_different_name_allowed(self):
        self.bank.create_account(1234567890, "Alice")
        aid = self.bank.create_account(1234567890, "Bob")
        self.assertIsNotNone(aid)

    def test_same_name_different_phone_allowed(self):
        self.bank.create_account(1111111111, "Alice")
        aid = self.bank.create_account(2222222222, "Alice")
        self.assertIsNotNone(aid)


class TestDeposit(unittest.TestCase):

    def setUp(self):
        self.bank = BankSystem()
        self.aid = self.bank.create_account(1234567890, "Alice")

    def test_basic_deposit(self):
        self.bank.deposit(self.aid, 100)
        self.assertEqual(self.bank.get_balance(self.aid), 100)

    def test_multiple_deposits(self):
        self.bank.deposit(self.aid, 100)
        self.bank.deposit(self.aid, 50)
        self.assertEqual(self.bank.get_balance(self.aid), 150)

    def test_deposit_zero(self):
        self.bank.deposit(self.aid, 0)
        self.assertEqual(self.bank.get_balance(self.aid), 0)

    def test_returns_true(self):
        self.assertTrue(self.bank.deposit(self.aid, 100))

    def test_records_transaction(self):
        self.bank.deposit(self.aid, 100)
        t = self.bank.transactions[-1]
        self.assertEqual(t.transaction_type, TransactionType.DEPOSIT)
        self.assertEqual(t.from_account, self.aid)
        self.assertEqual(t.to_account, self.aid)
        self.assertEqual(t.amount, 100)

    def test_invalid_account_raises(self):
        with self.assertRaises(AccountNotFoundError):
            self.bank.deposit("bad-id", 100)

    def test_negative_amount_raises(self):
        with self.assertRaises(NegativeAmountError):
            self.bank.deposit(self.aid, -50)


class TestWithdraw(unittest.TestCase):

    def setUp(self):
        self.bank = BankSystem()
        self.aid = self.bank.create_account(1234567890, "Alice")
        self.bank.deposit(self.aid, 500)

    def test_basic_withdraw(self):
        self.bank.withdraw(self.aid, 200)
        self.assertEqual(self.bank.get_balance(self.aid), 300)

    def test_withdraw_exact_balance(self):
        self.bank.withdraw(self.aid, 500)
        self.assertEqual(self.bank.get_balance(self.aid), 0)

    def test_returns_true(self):
        self.assertTrue(self.bank.withdraw(self.aid, 100))

    def test_records_transaction(self):
        self.bank.withdraw(self.aid, 200)
        t = self.bank.transactions[-1]
        self.assertEqual(t.transaction_type, TransactionType.WITHDRAW)
        self.assertEqual(t.from_account, self.aid)
        self.assertEqual(t.to_account, self.aid)
        self.assertEqual(t.amount, 200)

    def test_invalid_account_raises(self):
        with self.assertRaises(AccountNotFoundError):
            self.bank.withdraw("bad-id", 100)

    def test_negative_amount_raises(self):
        with self.assertRaises(NegativeAmountError):
            self.bank.withdraw(self.aid, -50)

    def test_insufficient_funds_raises(self):
        with self.assertRaises(InsufficientFundsError):
            self.bank.withdraw(self.aid, 501)

    def test_balance_unchanged_on_failed_withdraw(self):
        try:
            self.bank.withdraw(self.aid, 9999)
        except InsufficientFundsError:
            pass
        self.assertEqual(self.bank.get_balance(self.aid), 500)


class TestTransfer(unittest.TestCase):

    def setUp(self):
        self.bank = BankSystem()
        self.sender = self.bank.create_account(1111111111, "Alice")
        self.receiver = self.bank.create_account(2222222222, "Bob")
        self.bank.deposit(self.sender, 1000)

    def test_basic_transfer(self):
        self.bank.transaction(self.sender, self.receiver, 400)
        self.assertEqual(self.bank.get_balance(self.sender), 600)
        self.assertEqual(self.bank.get_balance(self.receiver), 400)

    def test_transfer_full_balance(self):
        self.bank.transaction(self.sender, self.receiver, 1000)
        self.assertEqual(self.bank.get_balance(self.sender), 0)
        self.assertEqual(self.bank.get_balance(self.receiver), 1000)

    def test_returns_true(self):
        self.assertTrue(self.bank.transaction(self.sender, self.receiver, 100))

    def test_records_transaction(self):
        self.bank.transaction(self.sender, self.receiver, 300)
        t = self.bank.transactions[-1]
        self.assertEqual(t.transaction_type, TransactionType.TRANSFER)
        self.assertEqual(t.from_account, self.sender)
        self.assertEqual(t.to_account, self.receiver)
        self.assertEqual(t.amount, 300)

    def test_invalid_sender_raises(self):
        with self.assertRaises(AccountNotFoundError):
            self.bank.transaction("bad-id", self.receiver, 100)

    def test_invalid_receiver_raises(self):
        with self.assertRaises(AccountNotFoundError):
            self.bank.transaction(self.sender, "bad-id", 100)

    def test_negative_amount_raises(self):
        with self.assertRaises(NegativeAmountError):
            self.bank.transaction(self.sender, self.receiver, -100)

    def test_insufficient_funds_raises(self):
        with self.assertRaises(InsufficientFundsError):
            self.bank.transaction(self.sender, self.receiver, 1001)

    def test_balances_unchanged_on_failed_transfer(self):
        try:
            self.bank.transaction(self.sender, self.receiver, 9999)
        except InsufficientFundsError:
            pass
        self.assertEqual(self.bank.get_balance(self.sender), 1000)
        self.assertEqual(self.bank.get_balance(self.receiver), 0)


class TestGetBalance(unittest.TestCase):

    def setUp(self):
        self.bank = BankSystem()
        self.aid = self.bank.create_account(1234567890, "Alice")

    def test_initial_balance_is_zero(self):
        self.assertEqual(self.bank.get_balance(self.aid), 0)

    def test_reflects_deposits(self):
        self.bank.deposit(self.aid, 250)
        self.assertEqual(self.bank.get_balance(self.aid), 250)

    def test_invalid_account_raises(self):
        with self.assertRaises(AccountNotFoundError):
            self.bank.get_balance("bad-id")


if __name__ == "__main__":
    unittest.main()

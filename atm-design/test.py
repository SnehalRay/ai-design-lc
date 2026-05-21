import unittest
from datetime import date
from second_code import Account, Bank, Card, ATM, TransactionType


def make_setup():
    bank = Bank("Chase")
    account = Account(bank)
    bank.add_account(account)
    card = account.generate_credit_card(
        cardId=1001,
        expiryDate=date(2027, 12, 31),
        pin=4242,
        cardHolderName="Snehal Ray"
    )
    atm = ATM(bank)
    return bank, account, card, atm


class TestAccount(unittest.TestCase):
    def setUp(self):
        self.bank, self.account, self.card, self.atm = make_setup()

    def test_initial_balance_is_zero(self):
        fresh_account = Account(self.bank)
        self.assertEqual(fresh_account.balance, 0)

    def test_set_balance(self):
        self.account.set_balance(250)
        self.assertEqual(self.account.balance, 250)

    def test_deposit_positive(self):
        self.account.deposit(100)
        self.assertEqual(self.account.balance, 100)

    def test_deposit_zero_raises(self):
        with self.assertRaises(ValueError):
            self.account.deposit(0)

    def test_deposit_negative_raises(self):
        with self.assertRaises(ValueError):
            self.account.deposit(-50)

    def test_withdraw_within_balance(self):
        self.account.set_balance(500)
        self.account.withdraw(200)
        self.assertEqual(self.account.balance, 300)

    def test_withdraw_exact_balance(self):
        self.account.set_balance(100)
        self.account.withdraw(100)
        self.assertEqual(self.account.balance, 0)

    def test_withdraw_more_than_balance_raises(self):
        self.account.set_balance(100)
        with self.assertRaises(ValueError):
            self.account.withdraw(101)


class TestCard(unittest.TestCase):
    def setUp(self):
        self.bank, self.account, self.card, self.atm = make_setup()

    def test_generate_credit_card_stores_in_account(self):
        self.assertIn(1001, self.account.creditCards)

    def test_has_credit_card_true(self):
        self.assertTrue(self.account.has_credit_card(1001))

    def test_has_credit_card_false(self):
        self.assertFalse(self.account.has_credit_card(9999))

    def test_getters(self):
        self.assertEqual(self.card.get_card_id(), 1001)
        self.assertEqual(self.card.get_expiry_date(), date(2027, 12, 31))
        self.assertEqual(self.card.get_pin(), 4242)
        self.assertEqual(self.card.get_card_holder_name(), "Snehal Ray")
        self.assertIs(self.card.get_bank(), self.bank)
        self.assertIs(self.card.get_account(), self.account)


class TestBank(unittest.TestCase):
    def setUp(self):
        self.bank, self.account, self.card, self.atm = make_setup()

    def test_registered_account_is_valid(self):
        self.assertTrue(self.bank.isAccountValid(self.account))

    def test_unregistered_account_is_invalid(self):
        other = Account(self.bank)
        self.assertFalse(self.bank.isAccountValid(other))

    def test_get_account_returns_account(self):
        self.assertIs(self.bank.get_account(self.account), self.account)

    def test_get_account_unregistered_raises(self):
        other = Account(self.bank)
        with self.assertRaises(ValueError):
            self.bank.get_account(other)


class TestATM(unittest.TestCase):
    def setUp(self):
        self.bank, self.account, self.card, self.atm = make_setup()
        self.account.set_balance(500)

    def test_atm_deposit(self):
        self.atm.process_transaction(self.card, TransactionType.DEPOSIT, 200)
        self.assertEqual(self.account.balance, 700)

    def test_atm_withdraw(self):
        self.atm.process_transaction(self.card, TransactionType.WITHDRAW, 100)
        self.assertEqual(self.account.balance, 400)

    def test_atm_card_from_different_bank_raises(self):
        other_bank = Bank("Wells Fargo")
        other_account = Account(other_bank)
        other_bank.add_account(other_account)
        other_card = other_account.generate_credit_card(
            cardId=2002,
            expiryDate=date(2026, 6, 30),
            pin=1234,
            cardHolderName="Other Person"
        )
        with self.assertRaises(ValueError):
            self.atm.process_transaction(other_card, TransactionType.DEPOSIT, 100)

    def test_atm_withdraw_overdraft_raises(self):
        with self.assertRaises(ValueError):
            self.atm.process_transaction(self.card, TransactionType.WITHDRAW, 10000)

    def test_atm_deposit_negative_raises(self):
        with self.assertRaises(ValueError):
            self.atm.process_transaction(self.card, TransactionType.DEPOSIT, -50)


if __name__ == "__main__":
    unittest.main(verbosity=2)

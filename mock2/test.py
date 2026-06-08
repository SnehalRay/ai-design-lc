import unittest
from code import Account, Bank, Transaction, TransactionType


class TestAccount(unittest.TestCase):

    def setUp(self):
        self.bank = Bank()
        self.id = self.bank.add_account("alice", "secret")

    def test_initial_balance(self):
        self.assertEqual(self.bank.check_balance(self.id), 0)

    def test_initial_overdraft(self):
        self.assertEqual(self.bank.account[self.id].overdraft_limit, 0)

    def test_initial_transaction_history_empty(self):
        self.assertEqual(self.bank.account[self.id].transaction_history, [])

    def test_id_is_readonly(self):
        with self.assertRaises(AttributeError):
            self.bank.account[self.id].id = "new-id"

    def test_name_is_readonly(self):
        with self.assertRaises(AttributeError):
            self.bank.account[self.id].name = "bob"

    def test_balance_rounds_to_two_decimals(self):
        self.bank.account[self.id].balance = 1.005
        self.assertEqual(self.bank.account[self.id].balance, 1.0)  # round half to even

    def test_overdraft_setter_rejects_negative(self):
        with self.assertRaises(ValueError):
            self.bank.account[self.id].overdraft_limit = -10

    def test_transaction_history_setter_rejects_non_list(self):
        with self.assertRaises(TypeError):
            self.bank.account[self.id].transaction_history = "bad"


class TestTransactionRepr(unittest.TestCase):

    def test_deposit_repr(self):
        t = Transaction(None, "acc-1", TransactionType.DEPOSIT, 100)
        self.assertIn("DEPOSIT", repr(t))
        self.assertIn("acc-1", repr(t))
        self.assertIn("100", repr(t))

    def test_withdraw_repr(self):
        t = Transaction("acc-1", None, TransactionType.WITHDRAW, 50)
        self.assertIn("WITHDRAW", repr(t))
        self.assertIn("acc-1", repr(t))
        self.assertIn("50", repr(t))

    def test_transfer_repr(self):
        t = Transaction("acc-1", "acc-2", TransactionType.TRANSFER, 75)
        self.assertIn("TRANSFER", repr(t))
        self.assertIn("acc-1", repr(t))
        self.assertIn("acc-2", repr(t))
        self.assertIn("75", repr(t))


class TestAuthentication(unittest.TestCase):

    def setUp(self):
        self.bank = Bank()
        self.id = self.bank.add_account("alice", "secret")

    def test_valid_credentials(self):
        self.assertEqual(self.bank.authenticate("alice", "secret"), self.id)

    def test_wrong_password(self):
        self.assertIsNone(self.bank.authenticate("alice", "wrong"))

    def test_unknown_user(self):
        self.assertIsNone(self.bank.authenticate("nobody", "secret"))


class TestDeposit(unittest.TestCase):

    def setUp(self):
        self.bank = Bank()
        self.id = self.bank.add_account("alice", "secret")

    def test_valid_deposit(self):
        self.assertTrue(self.bank.deposit(100, self.id))
        self.assertEqual(self.bank.check_balance(self.id), 100)

    def test_deposit_zero(self):
        self.assertFalse(self.bank.deposit(0, self.id))

    def test_deposit_negative(self):
        self.assertFalse(self.bank.deposit(-50, self.id))

    def test_deposit_unknown_account(self):
        self.assertIsNone(self.bank.deposit(100, "bad-id"))

    def test_floating_point_precision(self):
        self.bank.deposit(3.10, self.id)
        self.bank.deposit(3.20, self.id)
        self.assertEqual(self.bank.check_balance(self.id), 6.30)

    def test_deposit_records_transaction(self):
        self.bank.deposit(100, self.id)
        history = self.bank.account[self.id].transaction_history
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0].type, TransactionType.DEPOSIT)
        self.assertEqual(history[0].amount, 100)


class TestWithdraw(unittest.TestCase):

    def setUp(self):
        self.bank = Bank()
        self.id = self.bank.add_account("alice", "secret")
        self.bank.deposit(500, self.id)

    def test_valid_withdrawal(self):
        self.assertTrue(self.bank.withdraw(200, self.id))
        self.assertEqual(self.bank.check_balance(self.id), 300)

    def test_withdraw_zero(self):
        self.assertFalse(self.bank.withdraw(0, self.id))

    def test_withdraw_negative(self):
        self.assertFalse(self.bank.withdraw(-50, self.id))

    def test_withdraw_exceeds_balance(self):
        self.assertFalse(self.bank.withdraw(600, self.id))

    def test_withdraw_exact_balance(self):
        self.assertTrue(self.bank.withdraw(500, self.id))
        self.assertEqual(self.bank.check_balance(self.id), 0)

    def test_withdraw_unknown_account(self):
        self.assertIsNone(self.bank.withdraw(100, "bad-id"))

    def test_withdraw_records_transaction(self):
        self.bank.withdraw(100, self.id)
        history = self.bank.account[self.id].transaction_history
        withdraw_txns = [t for t in history if t.type == TransactionType.WITHDRAW]
        self.assertEqual(len(withdraw_txns), 1)
        self.assertEqual(withdraw_txns[0].amount, 100)


class TestTransfer(unittest.TestCase):

    def setUp(self):
        self.bank = Bank()
        self.sender = self.bank.add_account("alice", "secret")
        self.receiver = self.bank.add_account("bob", "pass")
        self.bank.deposit(500, self.sender)

    def test_valid_transfer(self):
        self.assertTrue(self.bank.transfer(self.sender, self.receiver, 200))
        self.assertEqual(self.bank.check_balance(self.sender), 300)
        self.assertEqual(self.bank.check_balance(self.receiver), 200)

    def test_transfer_zero(self):
        self.assertFalse(self.bank.transfer(self.sender, self.receiver, 0))

    def test_transfer_negative(self):
        self.assertFalse(self.bank.transfer(self.sender, self.receiver, -100))

    def test_transfer_insufficient_funds(self):
        self.assertFalse(self.bank.transfer(self.sender, self.receiver, 600))

    def test_transfer_unknown_sender(self):
        self.assertIsNone(self.bank.transfer("bad-id", self.receiver, 100))

    def test_transfer_unknown_receiver(self):
        self.assertIsNone(self.bank.transfer(self.sender, "bad-id", 100))

    def test_transfer_records_in_both_histories(self):
        self.bank.transfer(self.sender, self.receiver, 100)
        sender_txns = [t for t in self.bank.account[self.sender].transaction_history
                       if t.type == TransactionType.TRANSFER]
        receiver_txns = [t for t in self.bank.account[self.receiver].transaction_history
                         if t.type == TransactionType.TRANSFER]
        self.assertEqual(len(sender_txns), 1)
        self.assertEqual(len(receiver_txns), 1)


class TestOverdraft(unittest.TestCase):

    def setUp(self):
        self.bank = Bank()
        self.id = self.bank.add_account("alice", "secret")
        self.bank.deposit(100, self.id)

    def test_set_overdraft(self):
        self.assertTrue(self.bank.set_overdraft(self.id, 50))
        self.assertEqual(self.bank.account[self.id].overdraft_limit, 50)

    def test_set_overdraft_negative(self):
        self.assertFalse(self.bank.set_overdraft(self.id, -10))

    def test_set_overdraft_unknown_account(self):
        self.assertIsNone(self.bank.set_overdraft("bad-id", 50))

    def test_withdraw_within_overdraft(self):
        self.bank.set_overdraft(self.id, 50)
        self.assertTrue(self.bank.withdraw(130, self.id))
        self.assertEqual(self.bank.check_balance(self.id), -30)

    def test_withdraw_exceeds_overdraft(self):
        self.bank.set_overdraft(self.id, 50)
        self.assertFalse(self.bank.withdraw(160, self.id))

    def test_transfer_within_overdraft(self):
        receiver = self.bank.add_account("bob", "pass")
        self.bank.set_overdraft(self.id, 50)
        self.assertTrue(self.bank.transfer(self.id, receiver, 130))
        self.assertEqual(self.bank.check_balance(self.id), -30)

    def test_no_overdraft_cannot_go_negative(self):
        self.assertFalse(self.bank.withdraw(101, self.id))


class TestSession(unittest.TestCase):

    def setUp(self):
        self.bank = Bank()
        self.account_id = self.bank.add_account("alice", "secret")

    def test_create_session_returns_id(self):
        session_id = self.bank.create_session(self.account_id)
        self.assertIsNotNone(session_id)

    def test_validate_session_returns_account_id(self):
        session_id = self.bank.create_session(self.account_id)
        self.assertEqual(self.bank.validate_session(session_id), self.account_id)

    def test_validate_unknown_session(self):
        self.assertIsNone(self.bank.validate_session("bad-session"))

    def test_end_session_invalidates(self):
        session_id = self.bank.create_session(self.account_id)
        self.bank.end_session(session_id)
        self.assertIsNone(self.bank.validate_session(session_id))

    def test_session_id_differs_from_account_id(self):
        session_id = self.bank.create_session(self.account_id)
        self.assertNotEqual(session_id, self.account_id)


class TestInterest(unittest.TestCase):

    def setUp(self):
        self.bank = Bank()
        self.id = self.bank.add_account("alice", "secret")

    def test_apply_interest(self):
        self.bank.deposit(1000, self.id)
        self.bank.apply_interest(self.id)
        self.assertEqual(self.bank.check_balance(self.id), 1050.0)

    def test_apply_interest_unknown_account(self):
        self.assertFalse(self.bank.apply_interest("bad-id"))

    def test_apply_interest_zero_balance(self):
        self.bank.apply_interest(self.id)
        self.assertEqual(self.bank.check_balance(self.id), 0)


if __name__ == "__main__":
    unittest.main()

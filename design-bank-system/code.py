'''
You are building a simplified money transfer platform.
The system should support creating accounts, transferring money, and tracking transactions.

We can create accounts,
Transfer money from one account to another account?

Account should have a
unique id
owner name
current balance (while starting and creating an account, let the balance be 0)

Support:
creating an account
depositing money
withdrawing money
viewing balance
'''

import uuid
from datetime import datetime


class Account:
    def __init__(self, owner_name: str, phone_number:int):
        self._id = str(uuid.uuid4())
        self._owner_name = owner_name
        self._balance = 0.0
        self._phone_number = phone_number
        self._history = []

    @property
    def id(self):
        return self._id

    @property
    def owner_name(self):
        return self._owner_name

    @owner_name.setter
    def owner_name(self, name: str):
        if not name or not name.strip():
            raise ValueError("Owner name cannot be empty")
        self._owner_name = name.strip()

    @property
    def balance(self):
        return self._balance

    @property
    def min_balance(self) -> float:
        return 0.0

    @balance.setter
    def balance(self, amount: float):
        if amount < self.min_balance:
            raise ValueError(f"Balance cannot go below {self.min_balance}")
        self._balance = amount

    @property
    def history(self):
        return list(self._history)

    def _add_record(self, tx_id: str, timestamp: datetime, tx_type: str, amount: float) -> None:
        self._history.append((tx_id, timestamp, tx_type, amount))

    def __repr__(self):
        return f"Account(id={self._id}, owner={self._owner_name}, balance={self._balance})"
    

    
class SavingsAccount(Account):
    pass


class CheckingAccount(Account):
    @property
    def min_balance(self) -> float:
        return -500.0


class BankSystem:

    def __init__(self):
        self.accounts = {} #(owner_name, phone_number): Account object
        self.history = []  # list of (transaction_id, timestamp, transaction_type, amount)

    def create_account(self, name: str, phone_number: int, account_type: str) -> bool:
        key = (name, phone_number, account_type)
        if key in self.accounts:
            return False
        if account_type == "checking":
            self.accounts[key] = CheckingAccount(name, phone_number)
        elif account_type == "savings":
            self.accounts[key] = SavingsAccount(name, phone_number)
        else:
            raise ValueError("account_type must be 'checking' or 'savings'")
        return True

    def deposit_money(self, sender_name: str, sender_ph: int, account_type: str, amount: float) -> None:
        key = (sender_name, sender_ph, account_type)
        if key not in self.accounts:
            raise ValueError("Account not found")
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        account = self.accounts[key]
        account.balance = account.balance + amount
        tx_id, ts = str(uuid.uuid4()), datetime.now()
        account._add_record(tx_id, ts, "deposit", amount)
        self.history.append((tx_id, ts, "deposit", amount))


    def withdraw_money(self, sender_name: str, sender_ph: int, account_type: str, amount: float) -> None:
        key = (sender_name, sender_ph, account_type)
        if key not in self.accounts:
            raise ValueError("Account not found")
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        account = self.accounts[key]
        if account.balance - amount < account.min_balance:
            raise ValueError("Insufficient funds")
        account.balance = account.balance - amount
        tx_id, ts = str(uuid.uuid4()), datetime.now()
        account._add_record(tx_id, ts, "withdraw", amount)
        self.history.append((tx_id, ts, "withdraw", amount))


    def view_balance(self, sender_name: str, sender_ph: int, account_type: str) -> float:
        key = (sender_name, sender_ph, account_type)
        if key not in self.accounts:
            raise ValueError("Account not found")
        return self.accounts[key].balance
    
    def transaction(self, sender_name: str, sender_ph: int, sender_account_type: str,
                    receiver_name: str, receiver_ph: int, receiver_account_type: str,
                    amount: float) -> bool:
        
        if amount <= 0:
            raise ValueError("Transaction amount must be positive")
        sender_key = (sender_name, sender_ph, sender_account_type)
        if sender_key not in self.accounts:
            raise ValueError("Sender account not found")
        receiver_key = (receiver_name, receiver_ph, receiver_account_type)
        if receiver_key not in self.accounts:
            raise ValueError("Receiver account not found")
        if sender_key == receiver_key:
            raise ValueError("Cannot transfer to the same account")
        sender = self.accounts[sender_key]
        receiver = self.accounts[receiver_key]
        if sender.balance - amount < sender.min_balance:
            raise ValueError("Insufficient funds")
        
        sender.balance = sender.balance - amount
        receiver.balance = receiver.balance + amount
        tx_id, ts = str(uuid.uuid4()), datetime.now()
        sender._add_record(tx_id, ts, "transfer_out", amount)
        receiver._add_record(tx_id, ts, "transfer_in", amount)
        self.history.append((tx_id, ts, "transfer", amount))
        return True


def main():
    bank = BankSystem()

    print("=== Creating Accounts ===")
    print(bank.create_account("Alice", 1111, "savings"))   # True
    print(bank.create_account("Alice", 1111, "checking"))  # True — same person, different type
    print(bank.create_account("Bob",   2222, "savings"))   # True
    print(bank.create_account("Alice", 1111, "savings"))   # False — duplicate

    print("\n=== Deposits ===")
    bank.deposit_money("Alice", 1111, "savings",  1000)
    bank.deposit_money("Alice", 1111, "checking",  200)
    bank.deposit_money("Bob",   2222, "savings",   500)
    print(f"Alice savings:  ${bank.view_balance('Alice', 1111, 'savings')}")
    print(f"Alice checking: ${bank.view_balance('Alice', 1111, 'checking')}")
    print(f"Bob   savings:  ${bank.view_balance('Bob',   2222, 'savings')}")

    print("\n=== Withdrawals ===")
    bank.withdraw_money("Alice", 1111, "savings", 300)
    print(f"Alice savings after $300 withdrawal: ${bank.view_balance('Alice', 1111, 'savings')}")

    bank.withdraw_money("Alice", 1111, "checking", 600)   # goes to -400, allowed for checking
    print(f"Alice checking after $600 withdrawal (overdraft): ${bank.view_balance('Alice', 1111, 'checking')}")

    try:
        bank.withdraw_money("Alice", 1111, "checking", 200)   # would be -600, blocked
    except ValueError as e:
        print(f"Blocked overdraft: {e}")

    try:
        bank.withdraw_money("Bob", 2222, "savings", 600)      # savings can't go negative
    except ValueError as e:
        print(f"Blocked savings overdraft: {e}")

    print("\n=== Transfer ===")
    bank.transaction("Alice", 1111, "savings", "Bob", 2222, "savings", 200)
    print(f"Alice savings after transfer: ${bank.view_balance('Alice', 1111, 'savings')}")
    print(f"Bob   savings after transfer: ${bank.view_balance('Bob',   2222, 'savings')}")

    print("\n=== Transaction History ===")
    alice_savings = bank.accounts[("Alice", 1111, "savings")]
    for tx_id, ts, tx_type, amt in alice_savings.history:
        print(f"  [{tx_type:>12}]  ${amt:<8}  {ts.strftime('%H:%M:%S')}")


if __name__ == "__main__":
    main()
    
    


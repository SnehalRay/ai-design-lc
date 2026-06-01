'''
Banking System

Summary
Create a simple application that simulates a basic banking system. 
The system should allow users to perform the following actions with a single account: 
    Check the current balance, 
    deposit money into the account, 
    and withdraw money from the account.


Requirements
Implement an Account class with an initial balance of zero.
Provide methods to deposit money, withdraw money, and check the current balance.
Make sure the application can handle floating-point numbers for deposits. (e.g. When the balance is $3.10 and the user deposits $3.20, 
the new balance should be $6.30 not $6.300000000000001).
Ensure that withdrawals cannot exceed the available balance.


#part 2:
Multiple Accounts
Expand the system to handle multiple accounts, each with a unique identifier. Implement a method to transfer funds between accounts.

Transaction History:
Add functionality to maintain a transaction history for each account, detailing deposits, withdrawals, and transfers. Implement a method to display the transaction history.

Interest Calculation
Introduce a simple interest calculation that applies to accounts on a monthly basis.

User Authentication
Implement a basic system for account authentication, requiring a username and password combination for access.

Overdraft Protection
Add a feature to allow accounts to have overdraft protection up to a specified limit.

Command-line Interface
Create a simple command-line interface allowing users to interact with the banking system efficiently.

'''

import uuid
import hashlib
import os
import getpass
from enum import Enum

class TransactionType(Enum):
    DEPOSIT = "deposit"
    WITHDRAW = "withdraw"
    TRANSFER = "transfer"

class Transaction:
    def __init__(self, from_account: str, to_account: str, type: TransactionType, amount: float):
        self.from_account = from_account
        self.to_account = to_account
        self.type = type
        self.amount = amount

    def __repr__(self):
        if self.type == TransactionType.DEPOSIT:
            return f"[{self.type.value.upper()}] ${self.amount} -> {self.to_account}"
        elif self.type == TransactionType.WITHDRAW:
            return f"[{self.type.value.upper()}] ${self.amount} <- {self.from_account}"
        else:
            return f"[{self.type.value.upper()}] ${self.amount} from {self.from_account} -> {self.to_account}"

class Account:

    def __init__(self, id: str, name: str, password_hash: bytes, salt: bytes):
        self._id = id
        self._name = name
        self._password_hash = password_hash
        self._salt = salt
        self._balance: float = 0
        self._overdraft_limit: float = 0
        self._transaction_history = []

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def salt(self):
        return self._salt

    @property
    def password_hash(self):
        return self._password_hash

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, value:float):
        self._balance = round(value, 2)

    @property
    def overdraft_limit(self):
        return self._overdraft_limit

    @overdraft_limit.setter
    def overdraft_limit(self, value: float):
        if value < 0:
            raise ValueError("Overdraft limit cannot be negative")
        self._overdraft_limit = round(value, 2)

    @property
    def transaction_history(self):
        return self._transaction_history

    @transaction_history.setter
    def transaction_history(self, value: list):
        if not isinstance(value, list):
            raise TypeError("Transaction history must be a list")
        self._transaction_history = value


class Bank:
    def __init__(self):
        self.account = {} #id: account object
        self.interest = 0.05
        self._sessions = {}  # session_id: account_id

    def create_session(self, account_id: str) -> str:
        session_id = str(uuid.uuid4())
        self._sessions[session_id] = account_id
        return session_id

    def validate_session(self, session_id: str) -> str | None:
        return self._sessions.get(session_id)

    def end_session(self, session_id: str) -> None:
        self._sessions.pop(session_id, None)

    def add_account(self, name: str, password: str) -> str:
        salt = os.urandom(16)
        password_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
        account_id = str(uuid.uuid4())
        self.account[account_id] = Account(account_id, name, password_hash, salt)
        return account_id

    def authenticate(self, name: str, password: str) -> str | None:
        for account in self.account.values():
            if account.name == name:
                attempt = hashlib.pbkdf2_hmac('sha256', password.encode(), account.salt, 100000)
                if attempt == account.password_hash:
                    return account.id
        return None

    def set_overdraft(self, account_id: str, limit: float) -> bool:
        if account_id not in self.account:
            return None
        if limit < 0:
            return False
        self.account[account_id].overdraft_limit = limit
        return True

    def check_balance(self,account_id:str)->float:
        if account_id not in self.account:
            return None
        return self.account[account_id].balance

    def deposit(self, amount: float, account_id:str) -> bool:
        if account_id not in self.account:
            return None
        if amount <= 0:
            return False
        self.account[account_id].balance = round(self.account[account_id].balance + amount, 2)
        self.account[account_id].transaction_history.append(
            Transaction(from_account=None, to_account=account_id, type=TransactionType.DEPOSIT, amount=amount)
        )
        return True

    def withdraw(self, amount: float, account_id:str) -> bool:
        if account_id not in self.account:
            return None
        if amount <= 0 or amount > self.account[account_id].balance + self.account[account_id].overdraft_limit:
            return False
        self.account[account_id].balance = round(self.account[account_id].balance - amount, 2)
        self.account[account_id].transaction_history.append(
            Transaction(from_account=account_id, to_account=None, type=TransactionType.WITHDRAW, amount=amount)
        )
        return True
    
    def transfer(self, from_account: str, to_account: str, amount: float) -> bool:
        if from_account not in self.account or to_account not in self.account:
            return None
        if amount <= 0:
            return False
        if amount > self.account[from_account].balance + self.account[from_account].overdraft_limit:
            return False
        self.account[from_account].balance = round(self.account[from_account].balance - amount, 2)
        self.account[to_account].balance = round(self.account[to_account].balance + amount, 2)
        t = Transaction(from_account=from_account, to_account=to_account, type=TransactionType.TRANSFER, amount=amount)
        self.account[from_account].transaction_history.append(t)
        self.account[to_account].transaction_history.append(t)
        return True

    def display_transaction_history(self, account_id: str) -> None:
        if account_id not in self.account:
            return None
        if not self.account[account_id].transaction_history:
            print('No transaction yet')
        for transaction in self.account[account_id].transaction_history:
            print(repr(transaction))

    def apply_interest(self,account_id:str)->bool:
        if account_id not in self.account:
            return False
        self.account[account_id].balance = self.account[account_id].balance + (self.account[account_id].balance * self.interest)
        return True
    
def main():
    bank = Bank()

    while True:
        print("\n=== Welcome to the Bank ===")
        print("1. Login")
        print("2. Create Account")
        print("3. Exit")
        choice = input("Select: ").strip()

        if choice == "1":
            name = input("Username: ").strip()
            password = getpass.getpass("Password: ")
            account_id = bank.authenticate(name, password)
            if not account_id:
                print("Invalid credentials.")
                continue
            session_id = bank.create_session(account_id)
            print(f"Login successful. Session ID: {session_id}")
            _session_menu(bank, session_id)

        elif choice == "2":
            name = input("Username: ").strip()
            password = getpass.getpass("Password: ")
            confirm = getpass.getpass("Confirm password: ")
            if password != confirm:
                print("Passwords do not match.")
                continue
            account_id = bank.add_account(name, password)
            session_id = bank.create_session(account_id)
            print(f"Account created. Session ID: {session_id}")
            _session_menu(bank, session_id)

        elif choice == "3":
            print("Goodbye.")
            break
        else:
            print("Invalid option.")


def _session_menu(bank: Bank, session_id: str):
    while True:
        account_id = bank.validate_session(session_id)
        if not account_id:
            print("Session expired.")
            return

        print("\n=== Account Menu ===")
        print("1. Check Balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Transfer")
        print("5. Transaction History")
        print("6. Logout")
        choice = input("Select: ").strip()

        if choice == "1":
            print(f"Balance: ${bank.check_balance(account_id)}")

        elif choice == "2":
            try:
                amount = float(input("Amount: "))
            except ValueError:
                print("Invalid amount.")
                continue
            if bank.deposit(amount, account_id):
                print(f"Deposited ${amount}. New balance: ${bank.check_balance(account_id)}")
            else:
                print("Deposit failed. Amount must be positive.")

        elif choice == "3":
            try:
                amount = float(input("Amount: "))
            except ValueError:
                print("Invalid amount.")
                continue
            if bank.withdraw(amount, account_id):
                print(f"Withdrew ${amount}. New balance: ${bank.check_balance(account_id)}")
            else:
                print("Withdrawal failed. Insufficient funds or invalid amount.")

        elif choice == "4":
            to_id = input("Recipient account ID: ").strip()
            try:
                amount = float(input("Amount: "))
            except ValueError:
                print("Invalid amount.")
                continue
            result = bank.transfer(account_id, to_id, amount)
            if result is None:
                print("Recipient account not found.")
            elif result:
                print(f"Transferred ${amount}. New balance: ${bank.check_balance(account_id)}")
            else:
                print("Transfer failed. Insufficient funds or invalid amount.")

        elif choice == "5":
            bank.display_transaction_history(account_id)

        elif choice == "6":
            bank.end_session(session_id)
            print("Logged out.")
            return
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()

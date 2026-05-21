'''
Design an ATM Service

Authentication needed for a bank account

Objects:
Card
Bank
Bank Account
ATM

Flow is a customer inserts their card and enters a pin
ATM authenticates with the bank
customer can withdraw or deposit
atm accepts and gives money (while reducing the balance) or upgrade the money
'''

import hashlib
import secrets
from datetime import date


# ---------------------------------------------------------------------------
# Custom exceptions
# ---------------------------------------------------------------------------

class CardNotFoundError(Exception):
    pass

class InvalidPINError(Exception):
    pass

class InsufficientFundsError(Exception):
    pass


# ---------------------------------------------------------------------------
# Card
# ---------------------------------------------------------------------------

class Card:
    def __init__(
        self,
        card_number: str,
        account_number: str,
        bank_name: str,
        expiry: date,
        pin: str,
    ):
        self.card_number = card_number
        self.account_number = account_number
        self.bank_name = bank_name
        self.expiry = expiry
        self._salt = secrets.token_hex(16)
        self._pin_hash = hashlib.sha256((self._salt + pin).encode()).hexdigest()

    def checkPin(self, pin: str) -> bool:
        return hashlib.sha256((self._salt + pin).encode()).hexdigest() == self._pin_hash

    def isExpired(self) -> bool:
        return date.today() > self.expiry

    def __repr__(self) -> str:
        masked = "**** **** **** " + self.card_number[-4:]
        return f"Card({masked}, bank={self.bank_name}, account={self.account_number})"


# ---------------------------------------------------------------------------
# BankAccount
# ---------------------------------------------------------------------------

class BankAccount:
    def __init__(self, account_number: str, owner_name: str, initial_balance: float = 0.0):
        self.account_number = account_number
        self.owner_name = owner_name
        self._balance = initial_balance
        self._transactions = []

    def deposit(self, amount: float) -> float:
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self._balance += amount
        self._transactions.append({"type": "deposit", "amount": amount, "balance": self._balance})
        return self._balance

    def withdraw(self, amount: float) -> float:
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self._balance:
            raise InsufficientFundsError(f"Cannot withdraw {amount}, balance is {self._balance}")
        self._balance -= amount
        self._transactions.append({"type": "withdrawal", "amount": amount, "balance": self._balance})
        return self._balance

    def getBalance(self) -> float:
        return self._balance

    def getTransactionHistory(self) -> list:
        return list(self._transactions)

    def __repr__(self) -> str:
        return f"BankAccount(account={self.account_number}, owner={self.owner_name}, balance={self._balance})"


# ---------------------------------------------------------------------------
# Bank
# ---------------------------------------------------------------------------

class Bank:
    def __init__(self, name: str):
        self.name = name
        self.__accounts: dict = {}

    def addAccount(self, account: BankAccount) -> None:
        if account.account_number in self.__accounts:
            raise ValueError(f"Account {account.account_number} already exists")
        self.__accounts[account.account_number] = account

    def getAccount(self, account_number: str) -> BankAccount:
        if account_number not in self.__accounts:
            raise CardNotFoundError(f"No account found for account number {account_number}")
        return self.__accounts[account_number]

    def authenticate(self, card: Card, pin: str) -> BankAccount:
        if card.isExpired():
            raise ValueError("Card is expired")
        account = self.getAccount(card.account_number)
        if not card.checkPin(pin):
            raise InvalidPINError("Invalid PIN")
        return account

    def __repr__(self) -> str:
        return f"Bank(name={self.name}, accounts={len(self.__accounts)})"


# ---------------------------------------------------------------------------
# ATM
# ---------------------------------------------------------------------------

class ATM:
    def __init__(self, bank: Bank, cash: float = 0.0):
        self.bank = bank
        self.cash = cash
        self._card: Card = None
        self._session: BankAccount = None

    def insertCard(self, card: Card) -> None:
        if self._card is not None:
            raise ValueError("A card is already inserted. Eject it first.")
        self._card = card

    def authenticate(self, pin: str) -> None:
        if self._card is None:
            raise ValueError("No card inserted.")
        self._session = self.bank.authenticate(self._card, pin)

    def withdraw(self, amount: float) -> float:
        self._requireSession()
        if amount > self.cash:
            raise ValueError(f"ATM only has {self.cash} cash available")
        balance = self._session.withdraw(amount)
        self.cash -= amount
        return balance

    def deposit(self, amount: float) -> float:
        self._requireSession()
        balance = self._session.deposit(amount)
        self.cash += amount
        return balance

    def getBalance(self) -> float:
        self._requireSession()
        return self._session.getBalance()

    def ejectCard(self) -> None:
        self._card = None
        self._session = None

    def _requireSession(self) -> None:
        if self._session is None:
            raise ValueError("Not authenticated. Insert card and enter PIN first.")

    def __repr__(self) -> str:
        return f"ATM(bank={self.bank.name}, cash={self.cash}, active_session={self._session is not None})"


# ---------------------------------------------------------------------------
# Quick smoke test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    bank = Bank("Chase")
    account = BankAccount("ACC001", "Alice", initial_balance=500.0)
    bank.addAccount(account)
    card = Card("4111111111111234", "ACC001", "Chase", date(2028, 12, 31), "1234")

    atm = ATM(bank, cash=1000.0)

    atm.insertCard(card)
    atm.authenticate("1234")

    print("Balance:", atm.getBalance())
    atm.deposit(200)
    print("After deposit:", atm.getBalance())
    atm.withdraw(100)
    print("After withdrawal:", atm.getBalance())

    atm.ejectCard()

    # No session after eject
    try:
        atm.getBalance()
    except ValueError as e:
        print("Caught:", e)

    # Wrong PIN
    atm.insertCard(card)
    try:
        atm.authenticate("0000")
    except InvalidPINError as e:
        print("Caught:", e)
    atm.ejectCard()

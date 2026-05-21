from __future__ import annotations
from enum import Enum
from datetime import date

class TransactionType(Enum):
    DEPOSIT = "deposit"
    WITHDRAW = "withdraw"

class Account:
    def __init__(self, bank: Bank):
        self.balance = 0
        self.creditCards = {}
        self.transactions = []
        self.bank = bank

    def set_balance(self, amount: float):
        self.balance = amount

    def generate_credit_card(self, cardId: int, expiryDate: date, pin: int, cardHolderName: str) -> Card:
        card = Card(self.bank, cardId, expiryDate, pin, cardHolderName, self)
        self.creditCards[cardId] = card
        return card

    def has_credit_card(self, cardId: int) -> bool:
        return cardId in self.creditCards

    def withdraw(self, amount: float):
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount

    def deposit(self, amount: float):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.balance += amount



    
    

class Bank:
    def __init__(self, name: str):
        self.__accounts = set()
        self.name = name
    
    def add_account(self,account: Account):
        self.__accounts.add(account)
    
    def isAccountValid(self, account: Account):
        return True if account in self.__accounts else False
    
    def get_account(self, account: Account) -> Account:
        if account in self.__accounts:
            return account
        raise ValueError('Account does not exist')


class Card:
    def __init__(self, bank: Bank, cardId: int, expiryDate: date, pin: int, cardHolderName: str, account: Account):
        self._bank = bank
        self._cardId = cardId
        self._expiryDate = expiryDate
        self._pin = pin
        self._cardHolderName = cardHolderName
        self._account = account

    def get_bank(self) -> Bank:
        return self._bank

    def get_card_id(self) -> int:
        return self._cardId

    def get_expiry_date(self) -> date:
        return self._expiryDate

    def get_pin(self) -> int:
        return self._pin

    def get_card_holder_name(self) -> str:
        return self._cardHolderName

    def get_account(self) -> Account:
        return self._account


class ATM:
    def __init__(self, bank: Bank):
        self._bank = bank

    def process_transaction(self, card: Card, transaction_type: TransactionType, amount: float):
        account = card.get_account()
        if not self._bank.isAccountValid(account):
            raise ValueError("Account not valid for this bank")
        if transaction_type == TransactionType.DEPOSIT:
            account.deposit(amount)
        elif transaction_type == TransactionType.WITHDRAW:
            account.withdraw(amount)


if __name__ == "__main__":
    # Setup
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

    print(f"Initial balance: ${account.balance}")

    # Deposit
    atm.process_transaction(card, TransactionType.DEPOSIT, 500)
    print(f"After depositing $500: ${account.balance}")

    # Withdraw
    atm.process_transaction(card, TransactionType.WITHDRAW, 200)
    print(f"After withdrawing $200: ${account.balance}")

    # Overdraft attempt
    try:
        atm.process_transaction(card, TransactionType.WITHDRAW, 10000)
    except ValueError as e:
        print(f"Withdraw $10000 failed: {e}")

    # Invalid deposit attempt
    try:
        atm.process_transaction(card, TransactionType.DEPOSIT, -50)
    except ValueError as e:
        print(f"Deposit -$50 failed: {e}")



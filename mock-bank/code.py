'''
create account -> return id
deposit
withdraw
transfer
get balance
'''

import uuid
from enum import Enum


class TransactionType(Enum):
    DEPOSIT = "deposit"
    WITHDRAW = "withdraw"
    TRANSFER = "transfer"


class Transaction:
    def __init__(self, from_account: str, to_account: str,
                 transaction_type: TransactionType, amount: float):
        self.__from_account = from_account
        self.__to_account = to_account
        self.__transaction_type = transaction_type
        self.__amount = amount

    @property
    def from_account(self):
        return self.__from_account

    @property
    def to_account(self):
        return self.__to_account

    @property
    def transaction_type(self):
        return self.__transaction_type

    @property
    def amount(self):
        return self.__amount


class AccountAlreadyExistsError(Exception):
    def __init__(self, phone, name):
        super().__init__(f"Account for '{name}' with phone '{phone}' already exists.")

class AccountNotFoundError(Exception):
    def __init__(self, account_id):
        super().__init__(f"No account found with id '{account_id}'.")

class NegativeAmountError(Exception):
    def __init__(self, amount):
        super().__init__(f"Amount '{amount}' must be non-negative.")

class InsufficientFundsError(Exception):
    def __init__(self, balance, amount):
        super().__init__(f"Insufficient funds: balance is {balance}, cannot withdraw {amount}.")


class Account:

    def __init__(self, name: str, phone: int, balance: float = 0):
        self.__id = str(uuid.uuid4())
        self.__name = name
        self.__phone = phone
        self.__balance = balance

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value

    @property
    def phone(self):
        return self.__phone

    @phone.setter
    def phone(self, value: int):
        self.__phone = value

    @property
    def balance(self):
        return self.__balance

    @balance.setter
    def balance(self, value: float):
        self.__balance = value




class BankSystem:

    def __init__(self):
        self.accounts = {} #(phone number, name, account type)
        self.transactions = [] #(from account, to account, type transaction, amount)
        self.account_id = {} #id: Account

    def create_account(self,phoneNumber:int, name:str)->str:
        if (phoneNumber,name) in self.accounts:
            raise AccountAlreadyExistsError(phoneNumber, name)
        account = Account(name=name, phone=phoneNumber)
        self.accounts[(phoneNumber,name)] = account
        self.account_id[account.id] = account
        return account.id
    
    def deposit(self, accountid: str, balance: float) -> bool:
        if accountid not in self.account_id:
            raise AccountNotFoundError(accountid)
        if balance < 0:
            raise NegativeAmountError(balance)
        self.account_id[accountid].balance += balance
        self.transactions.append(Transaction(accountid, accountid, TransactionType.DEPOSIT, balance))
        return True

    def withdraw(self, accountid: str, balance: float) -> bool:
        if accountid not in self.account_id:
            raise AccountNotFoundError(accountid)
        if balance < 0:
            raise NegativeAmountError(balance)
        account = self.account_id[accountid]
        if account.balance - balance < 0:
            raise InsufficientFundsError(account.balance, balance)
        account.balance -= balance
        self.transactions.append(Transaction(accountid, accountid, TransactionType.WITHDRAW, balance))
        return True

    def transaction(self, transaction_out: str, transaction_in: str, balance: float) -> bool:
        if transaction_out not in self.account_id:
            raise AccountNotFoundError(transaction_out)
        if transaction_in not in self.account_id:
            raise AccountNotFoundError(transaction_in)
        if balance < 0:
            raise NegativeAmountError(balance)
        sender = self.account_id[transaction_out]
        if sender.balance - balance < 0:
            raise InsufficientFundsError(sender.balance, balance)
        sender.balance -= balance
        self.account_id[transaction_in].balance += balance
        self.transactions.append(Transaction(transaction_out, transaction_in, TransactionType.TRANSFER, balance))
        return True

    def get_balance(self, accountid: str) -> float:
        if accountid not in self.account_id:
            raise AccountNotFoundError(accountid)
        return self.account_id[accountid].balance


    
    
bank = BankSystem()
account1 = bank.create_account(1234567899, "abc")
# print(bank.create_account(1234567899, "abc"))
bank.deposit(account1,1000)
print(bank.get_balance(account1))
bank.withdraw(account1,1000)
print(bank.get_balance(account1))
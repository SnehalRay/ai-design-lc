'''
Design a vending machine that supports:
Adding products into the machine
Inserting money
Purchasing products
Returning change
Tracking inventory
Assume:
products have:
name
price
quantity
users insert money before purchasing
machine should reject purchases with insufficient balance
machine should reject out-of-stock items
You can start simple and extend later.

Each product has a maximum capacity
'''

from enum import Enum
from typing import List


class CoinDenomination(Enum):
    ONE = 1
    FIVE = 5
    TEN = 10


class Product:
    def __init__(self, name: str, price: float):
        self._name = name
        self._price = price
        self._qty = 0

    def get_name(self) -> str:
        return self._name
    
    def get_price(self) -> float:
        return self._price
    
    def get_quantity(self):
        return self._qty
    
    def set_quantity(self, qty: int):
        self._qty = qty


class VendingMachine:
    def __init__(self,capacity: int):
        self.current_deposit = 0.0
        self.product_items = {} #product name: Product object
        self.capacity = capacity
        self.current_count = 0

    def adding_product(self, product: Product, qty: int) -> bool:
        if self.current_count + qty > self.capacity:
            return False
        if product.get_name() in self.product_items:
            existing = self.product_items[product.get_name()]
            existing.set_quantity(existing.get_quantity() + qty)
        else:
            product.set_quantity(qty)
            self.product_items[product.get_name()] = product
        self.current_count += qty
        return True


    def insert_money(self, coins: List[CoinDenomination]) -> None:
        for coin in coins:
            self.current_deposit += coin.value

    def purchase_product(self, productname: str, qty: int) -> Product | None:
        if productname not in self.product_items:
            print("Product does not exist")
            return None
        
        product = self.product_items.get(productname)
        if qty> product.get_quantity():
            print("Not sufficient stock")
            return None
        if qty * product.get_price() > self.current_deposit:
            print("less funds")
            return None
        
        self.current_deposit -= qty * product.get_price()
        new_qty = product.get_quantity() - qty
        product.set_quantity(new_qty)
        if new_qty <= 0:
            del self.product_items[productname]
        self.current_count -= qty
        return product

    def get_inventory(self) -> None:
        for product in self.product_items.values():
            print(f"{product.get_name()} | price: ${product.get_price()} | qty: {product.get_quantity()}")

    def return_change(self):
        change = self.current_deposit
        self.current_deposit = 0
        return change


if __name__ == "__main__":
    vm = VendingMachine(capacity=10)

    cola = Product("Cola", 3.0)
    chips = Product("Chips", 5.0)
    vm.adding_product(cola, 3)
    vm.adding_product(chips, 2)

    print("--- Initial Inventory ---")
    vm.get_inventory()

    # exceed capacity
    water = Product("Water", 1.0)
    added = vm.adding_product(water, 10)
    print(f"\nAdd 10 Water (capacity=10, used=5): {added}")  # False

    # insufficient funds
    print("\n--- Insert $1, try to buy Cola ($3) ---")
    vm.insert_money([CoinDenomination.ONE])
    vm.purchase_product("Cola", 1)  # less funds

    # successful purchase
    print("\n--- Insert $10, buy 2 Cola ($6 total) ---")
    vm.insert_money([CoinDenomination.TEN])
    result = vm.purchase_product("Cola", 2)
    print(f"Purchased: {result.get_name() if result else None}")
    print(f"Change returned: ${vm.return_change()}")  # $5 (1 + 10 - 6)

    print("\n--- Inventory after purchase ---")
    vm.get_inventory()  # Cola qty should be 1

    # buy remaining Cola to trigger removal from inventory
    print("\n--- Insert $5, buy last Cola ---")
    vm.insert_money([CoinDenomination.FIVE])
    vm.purchase_product("Cola", 1)
    print("\n--- Inventory after Cola sold out ---")
    vm.get_inventory()  # only Chips remains

    # out of stock
    print("\n--- Try to buy Cola again (out of stock) ---")
    vm.insert_money([CoinDenomination.FIVE])
    vm.purchase_product("Cola", 1)  # Product does not exist
    vm.return_change()
    






'''
Requirements:
Add item with name, price, and quantity
If item already exists, increase quantity
Remove a certain quantity of an item
If quantity becomes 0, remove item fully
Get total cart price
Get current cart contents
Clear the cart


Assume:
item name is unique
price is fixed once item is added
quantity must be positive
no discounts yet
no taxes yet
no inventory checking yet
'''
import json


class Product:
    def __init__(self, name: str, price: float):
        self._name = name
        self.price = price  # uses setter for validation
        self.qty = 0

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float):
        if value < 0:
            raise ValueError("Price cannot be negative")
        self._price = float(value)

    @property
    def qty(self) -> float:
        return self._qty

    @qty.setter
    def qty(self, value: int):
        if value < 0:
            raise ValueError("Quantity cannot be negative")
        self._qty = value

    




class ShoppingCart:
    def __init__(self):
        self.cart = {} #name: Product
        self.total_price = 0.0


    def add_item(self, product: Product, qty: int):
        if product.name in self.cart:
            self.cart[product.name].qty += qty
        else:
            product.qty = qty
            self.cart[product.name] = product
        self.total_price += product.price * qty

    def remove_item(self, product: str, qty: int) -> bool:
        if product not in self.cart:
            return False
        existing = self.cart[product]
        if qty > existing.qty:
            return False
        self.total_price -= self.cart[product].price * qty
        if existing.qty == qty:
            del self.cart[product]
        else:
            existing.qty -= qty
        return True
        

    def get_total_price(self)->float:
        return self.total_price
    
    def get_total_card_content(self) -> str:
        items = [{"product": name, "quantity": p.qty, "price": p.price} for name, p in self.cart.items()]
        return json.dumps(items, indent=2)

    def clear_cart(self) -> None:
        self.cart = {}
        self.total_price = 0.0


if __name__ == "__main__":
    cart = ShoppingCart()

    apple = Product("Apple", 1.50)
    milk = Product("Milk", 2.00)

    cart.add_item(apple, 3)
    cart.add_item(milk, 1)

    print(cart.get_total_card_content())
    print("Total:", cart.get_total_price())

    cart.remove_item("Apple", 2)
    print("\nAfter removing 2 Apples:")
    print(cart.get_total_card_content())
    print("Total:", cart.get_total_price())

    cart.clear_cart()
    print("\nAfter clearing cart:")
    print(cart.get_total_card_content())
    print("Total:", cart.get_total_price())



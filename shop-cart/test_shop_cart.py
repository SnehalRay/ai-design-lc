import json
import unittest
from code import Product, ShoppingCart


class TestProduct(unittest.TestCase):
    def test_valid_creation(self):
        p = Product("Apple", 1.50)
        self.assertEqual(p.name, "Apple")
        self.assertEqual(p.price, 1.50)

    def test_negative_price(self):
        with self.assertRaises(ValueError):
            Product("Apple", -1.0)

    def test_negative_qty(self):
        p = Product("Apple", 1.50)
        with self.assertRaises(ValueError):
            p.qty = -1


class TestShoppingCartAddItem(unittest.TestCase):
    def setUp(self):
        self.cart = ShoppingCart()
        self.apple = Product("Apple", 1.50)

    def test_add_new_product(self):
        self.cart.add_item(self.apple, 3)
        self.assertIn("Apple", self.cart.cart)
        self.assertEqual(self.cart.cart["Apple"].qty, 3)
        self.assertAlmostEqual(self.cart.total_price, 4.50)

    def test_add_existing_product(self):
        self.cart.add_item(self.apple, 2)
        self.cart.add_item(self.apple, 3)
        self.assertEqual(self.cart.cart["Apple"].qty, 5)
        self.assertAlmostEqual(self.cart.total_price, 7.50)

    def test_add_multiple_products(self):
        milk = Product("Milk", 2.00)
        self.cart.add_item(self.apple, 2)
        self.cart.add_item(milk, 1)
        self.assertIn("Apple", self.cart.cart)
        self.assertIn("Milk", self.cart.cart)
        self.assertAlmostEqual(self.cart.total_price, 5.00)


class TestShoppingCartRemoveItem(unittest.TestCase):
    def setUp(self):
        self.cart = ShoppingCart()
        self.apple = Product("Apple", 1.50)
        self.cart.add_item(self.apple, 5)

    def test_remove_nonexistent(self):
        result = self.cart.remove_item("Banana", 1)
        self.assertFalse(result)

    def test_remove_more_than_available(self):
        result = self.cart.remove_item("Apple", 10)
        self.assertFalse(result)
        self.assertEqual(self.cart.cart["Apple"].qty, 5)

    def test_remove_partial(self):
        result = self.cart.remove_item("Apple", 3)
        self.assertTrue(result)
        self.assertEqual(self.cart.cart["Apple"].qty, 2)
        self.assertAlmostEqual(self.cart.total_price, 3.00)

    def test_remove_all(self):
        result = self.cart.remove_item("Apple", 5)
        self.assertTrue(result)
        self.assertNotIn("Apple", self.cart.cart)
        self.assertAlmostEqual(self.cart.total_price, 0.0)


class TestShoppingCartGetTotalPrice(unittest.TestCase):
    def setUp(self):
        self.cart = ShoppingCart()

    def test_empty_cart(self):
        self.assertEqual(self.cart.get_total_price(), 0.0)

    def test_after_add(self):
        apple = Product("Apple", 1.50)
        milk = Product("Milk", 2.00)
        self.cart.add_item(apple, 3)
        self.cart.add_item(milk, 2)
        self.assertAlmostEqual(self.cart.get_total_price(), 8.50)

    def test_after_remove(self):
        apple = Product("Apple", 1.50)
        self.cart.add_item(apple, 4)
        self.cart.remove_item("Apple", 2)
        self.assertAlmostEqual(self.cart.get_total_price(), 3.00)


class TestShoppingCartGetContents(unittest.TestCase):
    def setUp(self):
        self.cart = ShoppingCart()

    def test_empty_cart_json(self):
        result = json.loads(self.cart.get_total_card_content())
        self.assertEqual(result, [])

    def test_contents_fields(self):
        apple = Product("Apple", 1.50)
        self.cart.add_item(apple, 2)
        result = json.loads(self.cart.get_total_card_content())
        self.assertEqual(len(result), 1)
        self.assertIn("product", result[0])
        self.assertIn("quantity", result[0])
        self.assertIn("price", result[0])
        self.assertEqual(result[0]["product"], "Apple")
        self.assertEqual(result[0]["quantity"], 2)
        self.assertAlmostEqual(result[0]["price"], 1.50)


class TestShoppingCartClearCart(unittest.TestCase):
    def setUp(self):
        self.cart = ShoppingCart()
        apple = Product("Apple", 1.50)
        self.cart.add_item(apple, 3)

    def test_clear_empties_cart(self):
        self.cart.clear_cart()
        self.assertEqual(len(self.cart.cart), 0)

    def test_clear_resets_total(self):
        self.cart.clear_cart()
        self.assertEqual(self.cart.total_price, 0.0)


if __name__ == "__main__":
    unittest.main()

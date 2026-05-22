import unittest
from code import CoinDenomination, Product, VendingMachine


class TestProduct(unittest.TestCase):
    def setUp(self):
        self.product = Product("Cola", 3.0)

    def test_initial_quantity_is_zero(self):
        self.assertEqual(self.product.get_quantity(), 0)

    def test_get_name(self):
        self.assertEqual(self.product.get_name(), "Cola")

    def test_get_price(self):
        self.assertEqual(self.product.get_price(), 3.0)

    def test_set_quantity(self):
        self.product.set_quantity(5)
        self.assertEqual(self.product.get_quantity(), 5)


class TestVendingMachineInventory(unittest.TestCase):
    def setUp(self):
        self.vm = VendingMachine(capacity=10)
        self.cola = Product("Cola", 3.0)
        self.chips = Product("Chips", 5.0)

    def test_add_new_product(self):
        result = self.vm.adding_product(self.cola, 3)
        self.assertTrue(result)
        self.assertEqual(self.cola.get_quantity(), 3)

    def test_add_existing_product_increments_quantity(self):
        self.vm.adding_product(self.cola, 2)
        cola2 = Product("Cola", 3.0)
        self.vm.adding_product(cola2, 3)
        self.assertEqual(self.vm.product_items["Cola"].get_quantity(), 5)

    def test_add_product_exceeds_capacity_returns_false(self):
        result = self.vm.adding_product(self.cola, 11)
        self.assertFalse(result)

    def test_add_products_up_to_capacity(self):
        self.vm.adding_product(self.cola, 5)
        result = self.vm.adding_product(self.chips, 5)
        self.assertTrue(result)
        self.assertEqual(self.vm.current_count, 10)

    def test_add_beyond_remaining_capacity_returns_false(self):
        self.vm.adding_product(self.cola, 5)
        result = self.vm.adding_product(self.chips, 6)
        self.assertFalse(result)

    def test_current_count_updates_on_add(self):
        self.vm.adding_product(self.cola, 4)
        self.assertEqual(self.vm.current_count, 4)


class TestVendingMachineInsertMoney(unittest.TestCase):
    def setUp(self):
        self.vm = VendingMachine(capacity=10)

    def test_insert_single_coin(self):
        self.vm.insert_money([CoinDenomination.TEN])
        self.assertEqual(self.vm.current_deposit, 10)

    def test_insert_multiple_coins(self):
        self.vm.insert_money([CoinDenomination.ONE, CoinDenomination.FIVE, CoinDenomination.TEN])
        self.assertEqual(self.vm.current_deposit, 16)

    def test_insert_money_accumulates(self):
        self.vm.insert_money([CoinDenomination.FIVE])
        self.vm.insert_money([CoinDenomination.FIVE])
        self.assertEqual(self.vm.current_deposit, 10)

    def test_insert_empty_list(self):
        self.vm.insert_money([])
        self.assertEqual(self.vm.current_deposit, 0)


class TestVendingMachinePurchase(unittest.TestCase):
    def setUp(self):
        self.vm = VendingMachine(capacity=10)
        cola = Product("Cola", 3.0)
        chips = Product("Chips", 5.0)
        self.vm.adding_product(cola, 3)
        self.vm.adding_product(chips, 2)

    def test_successful_purchase(self):
        self.vm.insert_money([CoinDenomination.FIVE])
        result = self.vm.purchase_product("Cola", 1)
        self.assertIsNotNone(result)
        self.assertEqual(result.get_name(), "Cola")

    def test_purchase_deducts_deposit(self):
        self.vm.insert_money([CoinDenomination.TEN])
        self.vm.purchase_product("Cola", 1)
        self.assertAlmostEqual(self.vm.current_deposit, 7.0)

    def test_purchase_reduces_inventory_count(self):
        self.vm.insert_money([CoinDenomination.TEN])
        self.vm.purchase_product("Cola", 2)
        self.assertEqual(self.vm.current_count, 3)

    def test_purchase_reduces_product_quantity(self):
        self.vm.insert_money([CoinDenomination.TEN])
        self.vm.purchase_product("Cola", 2)
        self.assertEqual(self.vm.product_items["Cola"].get_quantity(), 1)

    def test_purchase_nonexistent_product_returns_none(self):
        self.vm.insert_money([CoinDenomination.TEN])
        result = self.vm.purchase_product("Water", 1)
        self.assertIsNone(result)

    def test_purchase_insufficient_funds_returns_none(self):
        self.vm.insert_money([CoinDenomination.ONE])
        result = self.vm.purchase_product("Cola", 1)
        self.assertIsNone(result)

    def test_purchase_insufficient_funds_does_not_deduct_deposit(self):
        self.vm.insert_money([CoinDenomination.ONE])
        self.vm.purchase_product("Cola", 1)
        self.assertEqual(self.vm.current_deposit, 1)

    def test_purchase_more_than_stock_returns_none(self):
        self.vm.insert_money([CoinDenomination.TEN])
        result = self.vm.purchase_product("Cola", 10)
        self.assertIsNone(result)

    def test_purchase_removes_product_when_sold_out(self):
        self.vm.insert_money([CoinDenomination.TEN])
        self.vm.purchase_product("Cola", 3)
        self.assertNotIn("Cola", self.vm.product_items)

    def test_purchase_multiple_qty(self):
        self.vm.insert_money([CoinDenomination.TEN])
        result = self.vm.purchase_product("Cola", 2)
        self.assertIsNotNone(result)
        self.assertAlmostEqual(self.vm.current_deposit, 4.0)


class TestVendingMachineReturnChange(unittest.TestCase):
    def setUp(self):
        self.vm = VendingMachine(capacity=10)

    def test_return_change_gives_back_full_deposit(self):
        self.vm.insert_money([CoinDenomination.TEN])
        change = self.vm.return_change()
        self.assertEqual(change, 10)

    def test_return_change_resets_deposit_to_zero(self):
        self.vm.insert_money([CoinDenomination.FIVE])
        self.vm.return_change()
        self.assertEqual(self.vm.current_deposit, 0)

    def test_return_change_after_purchase(self):
        cola = Product("Cola", 3.0)
        self.vm.adding_product(cola, 1)
        self.vm.insert_money([CoinDenomination.FIVE])
        self.vm.purchase_product("Cola", 1)
        change = self.vm.return_change()
        self.assertAlmostEqual(change, 2.0)

    def test_return_change_with_no_deposit(self):
        change = self.vm.return_change()
        self.assertEqual(change, 0)


if __name__ == "__main__":
    unittest.main()

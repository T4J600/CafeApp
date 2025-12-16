# CafeTests.py
# Unit tests for CaféSmart
import unittest
from CafeSystem import MenuItem, FoodItem, DrinkItem, MenuFactory, Order, TaxCalculator, MenuManager

# Test Factory Pattern
class TestMenuFactory(unittest.TestCase):
    def test_factory_creates_food_item(self):
        item = MenuFactory.create_item("food", "Croissant", 2.50, "Pastry")
        self.assertIsInstance(item, FoodItem)

    def test_factory_creates_drink_item(self):
        item = MenuFactory.create_item("drink", "Latte", 3.20, "Large")
        self.assertIsInstance(item, DrinkItem)

    def test_factory_invalid_type(self):
        with self.assertRaises(ValueError):
            MenuFactory.create_item("dessert", "Cake", 3.00, "Sweet")

# Test Order Functionality
class TestOrder(unittest.TestCase):
    def setUp(self):
        self.order = Order()
        self.item1 = MenuItem("Tea", 2.00)
        self.item2 = MenuItem("Coffee", 3.00)

    def test_add_item(self):
        self.order.add_item(self.item1)
        self.assertEqual(len(self.order.items), 1)

    def test_remove_item(self):
        self.order.add_item(self.item1)
        removed = self.order.remove_item_by_index(0)
        self.assertEqual(removed, self.item1)

    def test_subtotal_calculation(self):
        self.order.add_item(self.item1)
        self.order.add_item(self.item2)
        self.assertEqual(self.order.calculate_subtotal(), 5.00)

# Test Tax Calculation
class TestTaxCalculator(unittest.TestCase):
    def test_tax_calculation(self):
        tax = TaxCalculator(0.10)
        self.assertAlmostEqual(tax.calculate_tax(100), 10.0)

    def test_negative_tax_error(self):
        tax = TaxCalculator()
        with self.assertRaises(ValueError):
            tax.calculate_tax(-20)

# Test Menu Manager
class TestMenuManager(unittest.TestCase):
    def test_add_and_get_item(self):
        menu = MenuManager()
        item = MenuItem("Latte", 3.20)
        menu.add_item(item)
        self.assertEqual(menu.get_item(1), item)

    def test_show_menu(self):
        menu = MenuManager()
        item1 = MenuItem("Tea", 2.00)
        item2 = MenuItem("Coffee", 3.00)
        menu.add_item(item1)
        menu.add_item(item2)
        menu_list = menu.show_menu()
        self.assertEqual(menu_list[0], "Tea - £2.00")
        self.assertEqual(menu_list[1], "Coffee - £3.00")

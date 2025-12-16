from datetime import datetime

# Base Class: MenuItem
class MenuItem:
    def __init__(self, name, price):
        self.name = name        # Name of the menu item
        self.price = price      # Price of the menu item

    def get_price(self):
        return self.price

    def __str__(self):
        #Readable representation for menu display"
        return f"{self.name} - £{self.price:.2f}"


# Subclass: FoodItem (Inheritance)
class FoodItem(MenuItem):
    def __init__(self, name, price, category):
        super().__init__(name, price)
        self.category = category   # e.g., Pastry, Bakery


# Subclass: DrinkItem (Inheritance)
class DrinkItem(MenuItem):
    def __init__(self, name, price, size):
        super().__init__(name, price)
        self.size = size           # e.g., Regular, Large


# Factory Pattern: MenuFactory
class MenuFactory:
    @staticmethod
    def create_item(item_type, name, price, attribute):
        #Creates FoodItem or DrinkItem based on type
        if item_type == "food":
            return FoodItem(name, price, attribute)
        elif item_type == "drink":
            return DrinkItem(name, price, attribute)
        else:
            raise ValueError("Unsupported menu item type.")

# Observer Pattern: OrderObserver
# Observers are notified when the order changes
class OrderObserver:
    def update(self, order):
        #Notify user that order has changed
        print(f"(Order updated: {len(order.items)} item(s) in current order)")


# Class: Order
# Manages a customer's order
class Order:
    def __init__(self):
        self.items = []        # List of MenuItem objects
        self.observers = []    # Attached observers

    def attach(self, observer):
        #attach an observer to the order
        self.observers.append(observer)

    def notify(self):
        """Notify all observers of changes"""
        for obs in self.observers:
            obs.update(self)

    def add_item(self, item):
        #Add a menu item to the order and notify observers
        self.items.append(item)
        self.notify()

    def remove_item_by_index(self, index):
        if 0 <= index < len(self.items):
            removed = self.items.pop(index)
            self.notify()
            return removed
        return None

    def is_empty(self):
        #heck if order is empty
        return len(self.items) == 0

    def calculate_subtotal(self):
        #calculate subtotal of all items
        return sum(item.get_price() for item in self.items)

    def display_order(self):
        #Display current order item
        print("\nCurrent Order:")
        for i, item in enumerate(self.items, start=1):
            print(f"{i}. {item}")
        print()

# Class: TaxCalculator
class TaxCalculator:
    def __init__(self, rate=0.10):
        self.rate = rate   # Default tax rate (10%)

    def calculate_tax(self, amount):
       # calculate tax on a given amount
        if amount < 0:
            raise ValueError("Invalid amount for tax calculation.")
        return amount * self.rate

# Class: Bill
# Generates a receipt from an order
class Bill:
    def __init__(self, order, tax_calculator):
        self.order = order
        self.tax_calculator = tax_calculator

    def generate_bill(self):
    #generate receipt data and calculate totals
        subtotal = self.order.calculate_subtotal()
        tax = self.tax_calculator.calculate_tax(subtotal)
        total = subtotal + tax

        # Return values as dictionary for GUI or text display
        return {
            "subtotal": subtotal,
            "tax": tax,
            "total": total,
            "items": [(item.name, item.price) for item in self.order.items]
        }


# Class: MenuManager
# Manages the café menu items
class MenuManager:
    def __init__(self):
        self.menu = []

    def add_item(self, item):
        #add menu item (manager-only)
        self.menu.append(item)

    def show_menu(self):
        return [str(item) for item in self.menu]

    def get_item(self, number):
        if 1 <= number <= len(self.menu):
            return self.menu[number - 1]
        return None

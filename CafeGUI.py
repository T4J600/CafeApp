# CafeGUI.py
import tkinter as tk
from tkinter import messagebox
from CafeSystem import MenuFactory, MenuManager, Order, Bill, TaxCalculator, OrderObserver

# GUI Class for CaféSmart
class CafeAppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CaféSmart Ordering System")
        self.root.geometry("500x500")

        # Initialize core components
        self.factory = MenuFactory()  # Factory for creating menu items
        self.menu = MenuManager()     # Menu manager
        self.tax_calculator = TaxCalculator()  # Tax calculator
        self.order = None             # Current order

        # Manager-only menu setup
        self.setup_menu()

        # GUI Widgets
        self.create_widgets()

    # Prepopulate the menu with drinks and food
    def setup_menu(self):
        self.menu.add_item(self.factory.create_item("drink", "Americano", 2.80, "Regular"))
        self.menu.add_item(self.factory.create_item("drink", "Latte", 3.20, "Large"))
        self.menu.add_item(self.factory.create_item("drink", "Hot Chocolate", 3.00, "Regular"))
        self.menu.add_item(self.factory.create_item("food", "Butter Croissant", 2.10, "Pastry"))
        self.menu.add_item(self.factory.create_item("food", "Banana Bread", 2.60, "Bakery"))

    # Create all GUI components
    def create_widgets(self):
        # Title
        self.title_label = tk.Label(self.root, text="Welcome to CaféSmart", font=("Helvetica", 16))
        self.title_label.pack(pady=10)

        # Menu Listbox
        self.menu_label = tk.Label(self.root, text="Menu")
        self.menu_label.pack()
        self.menu_listbox = tk.Listbox(self.root, width=50)
        self.menu_listbox.pack()
        self.update_menu_display()

        # Buttons Frame
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=10)

        self.start_button = tk.Button(self.button_frame, text="Start New Order", command=self.start_order)
        self.start_button.grid(row=0, column=0, padx=5)

        self.add_button = tk.Button(self.button_frame, text="Add Item", command=self.add_item_to_order)
        self.add_button.grid(row=0, column=1, padx=5)

        self.remove_button = tk.Button(self.button_frame, text="Remove Item", command=self.remove_item_from_order)
        self.remove_button.grid(row=0, column=2, padx=5)

        self.finish_button = tk.Button(self.button_frame, text="Finish Order", command=self.finish_order)
        self.finish_button.grid(row=0, column=3, padx=5)

        # Current Order Display
        self.order_label = tk.Label(self.root, text="Current Order:")
        self.order_label.pack()
        self.order_listbox = tk.Listbox(self.root, width=50)
        self.order_listbox.pack()

    # Update the menu Listbox
    def update_menu_display(self):
        self.menu_listbox.delete(0, tk.END)
        for item in self.menu.menu:
            self.menu_listbox.insert(tk.END, str(item))

    # Start a new order
    def start_order(self):
        self.order = Order()
        self.order.attach(OrderObserver())  # Observer to track updates
        self.update_order_display()
        messagebox.showinfo("Order Started", "New order has been started!")

    # Add selected item to the current order
    def add_item_to_order(self):
        if self.order is None:
            messagebox.showwarning("No Order", "Start a new order first!")
            return
        selection = self.menu_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Select a menu item to add!")
            return
        item = self.menu.get_item(selection[0] + 1)
        self.order.add_item(item)
        self.update_order_display()
        messagebox.showinfo("Item Added", f"Added: {item.name}")

    # Remove selected item from the current order
    def remove_item_from_order(self):
        if self.order is None or self.order.is_empty():
            messagebox.showwarning("Empty Order", "No items to remove!")
            return
        selection = self.order_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Select an item to remove!")
            return
        index = selection[0]
        removed = self.order.remove_item_by_index(index)
        self.update_order_display()
        messagebox.showinfo("Item Removed", f"Removed: {removed.name}")

    # Finish order and generate the bill
    def finish_order(self):
        if self.order is None or self.order.is_empty():
            messagebox.showwarning("Empty Order", "Cannot finish an empty order!")
            return

        # Calculate subtotal and tax
        subtotal = self.order.calculate_subtotal()
        tax = self.tax_calculator.calculate_tax(subtotal)
        total = subtotal + tax

        # Generate bill text for GUI display
        bill_text = "------ CaféSmart Receipt ------\n"
        for item in self.order.items:
            bill_text += f"{item.name:<18} £{item.price:.2f}\n"
        bill_text += "-------------------------------\n"
        bill_text += f"Subtotal:           £{subtotal:.2f}\n"
        bill_text += f"Tax (10%):          £{tax:.2f}\n"
        bill_text += f"Total Due:          £{total:.2f}\n"
        bill_text += "-------------------------------\n"
        bill_text += "Thank you. Please come again!\n"
        bill_text += "-------------------------------"

        # Show the bill in a popup
        messagebox.showinfo("Bill", bill_text)

        # Reset the order
        self.order = None
        self.update_order_display()

    # Update the order Listbox
    def update_order_display(self):
        self.order_listbox.delete(0, tk.END)
        if self.order is not None:
            for item in self.order.items:
                self.order_listbox.insert(tk.END, str(item))


# Run GUI if this file is executed
if __name__ == "__main__":
    root = tk.Tk()
    app = CafeAppGUI(root)
    root.mainloop()

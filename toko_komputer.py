import tkinter as tk
from tkinter import simpledialog, messagebox
import locale
from tkinter import ttk

locale.setlocale(locale.LC_ALL, 'id_ID')


class Product:
    def __init__(self, name, price, stock, category):
        self.name = name
        self.price = price
        self.stock = stock
        self.category = category

class Customer:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.shopping_cart = []

    def add_to_cart(self, product, quantity):
        self.shopping_cart.append({"product": product, "quantity": quantity})

    def clear_cart(self):
        self.shopping_cart = []



class ComputerStore:
    def __init__(self, name):
        self.name = name
        self.products = []

        default_products = [
            Product("ASUS ROG Strix Scar", 60000000, 10, "Laptop"),
            Product("PC Desktop I5 Gen 10 GTX 1650", 8000000, 7, "PC Desktop"),
            Product("Mouse Logitech", 500000, 20, "Mouse"),
            Product("Keyboard Mechanical Full Size", 2000000, 10, "Keyboard"),
            Product("Lenovo Ideapad Gaming 3", 14000000, 10, "Laptop"),
            Product("ASUS TUF Gaming F15", 15000000, 15, "Laptop"),
            Product("PC Dekstop I3 Gen 12 GTX 1650", 5000000, 5, "PC Dekstop"),
            Product("Keyboard Mechanical 60%", 1000000, 20, "Keyboard")
        ]

        for product in default_products:
            self.add_product(product)

    def add_product(self, product):
        self.products.append(product)

    def purchase_product(self, product, quantity):
        for p in self.products:
            if p.name == product.name:
                if p.stock >= quantity:
                    p.stock -= quantity
                    return Product(p.name, p.price, quantity, p.category)
                else:
                    messagebox.showwarning("Warning", f"Insufficient stock for {p.name}. Available stock: {p.stock}")
                    return None
        messagebox.showwarning("Warning", f"Product {product.name} not found.")
        return None


class ShoppingCart:
    def __init__(self):
        self.items = []

    def calculate_total(self):
        return sum(item["product"].price * item["quantity"] for item in self.items)


class LoginApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Login")
        self.geometry("300x200")

        self.label_username = tk.Label(self, text="Username:")
        self.label_username.pack(pady=10)

        self.entry_username = tk.Entry(self)
        self.entry_username.pack(pady=5)

        self.label_password = tk.Label(self, text="Password:")
        self.label_password.pack(pady=10)

        self.entry_password = tk.Entry(self, show="*")
        self.entry_password.pack(pady=5)

        self.btn_login = tk.Button(self, text="Login", command=self.login)
        self.btn_login.pack(pady=10)

    def login(self):
        entered_username = self.entry_username.get()
        entered_password = self.entry_password.get()

        valid_credentials = {"admin": "password", "user1": "pass123"}

        if entered_username in valid_credentials and entered_password == valid_credentials[entered_username]:
            messagebox.showinfo("Login Successful", "Welcome to the Computer Store!")
            self.destroy()
            computer_store_app = ComputerStoreApp(ComputerStore("Tech Haven"), Customer(entered_username, ""))
            computer_store_app.mainloop()
        else:
            messagebox.showwarning("Login Failed", "Invalid username or password")


class ComputerStoreApp(tk.Tk):
    def __init__(self, computer_store, customer):
        super().__init__()
        self.title("Computer Store App")
        self.geometry("800x600")

        font_style = ("Arial", 12)

        self.computer_store = computer_store
        self.customer = customer
        self.shopping_cart = ShoppingCart()

        self.label_username = tk.Label(self, text=f"Welcome, {self.customer.username}!", font=font_style)
        self.label_username.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.label_products = tk.Label(self, text="Available Products", font=font_style)
        self.label_products.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.listbox_products = tk.Listbox(self, font=font_style, height=10, width=50)
        self.listbox_products.grid(row=2, column=0, padx=10, pady=10, rowspan=5)

        self.btn_add_product = tk.Button(self, text="Add Product", command=self.add_product, font=font_style, padx=10,
                                         pady=5)
        self.btn_add_product.grid(row=8, column=0, padx=10, pady=10, sticky="w")

        self.btn_purchase = tk.Button(self, text="Purchase", command=self.purchase_product, font=font_style, padx=10,
                                      pady=5)
        self.btn_purchase.grid(row=9, column=0, padx=10, pady=10, sticky="w")

        self.label_cart = tk.Label(self, text="Shopping Cart", font=font_style)
        self.label_cart.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        self.listbox_cart = tk.Listbox(self, font=font_style, height=10, width=50)
        self.listbox_cart.grid(row=2, column=1, padx=10, pady=10, rowspan=5)

        self.label_total = tk.Label(self, text="Total:", font=font_style)
        self.label_total.grid(row=7, column=1, padx=10, pady=5, sticky="w")

        self.entry_total = tk.Entry(self, state=tk.DISABLED, font=font_style, width=15)
        self.entry_total.grid(row=7, column=1, padx=10, pady=5, sticky="e")

        self.label_payment_method = tk.Label(self, text="Payment Method:", font=font_style)
        self.label_payment_method.grid(row=8, column=1, padx=10, pady=5, sticky="w")

        payment_methods = ["Cash", "Credit Card"]
        self.var_payment_method = tk.StringVar(self)
        self.var_payment_method.set(payment_methods[0])
        self.optionmenu_payment_method = tk.OptionMenu(self, self.var_payment_method, *payment_methods)
        self.optionmenu_payment_method.config(font=font_style)
        self.optionmenu_payment_method.grid(row=8, column=1, padx=10, pady=5, sticky="e")

        # Dropdown menu for sorting category
        self.label_sort_category = tk.Label(self, text="Sort by Category:", font=font_style)
        self.label_sort_category.grid(row=0, column=2, padx=10, pady=10, sticky="w")

        categories = ["All", "Laptop", "PC Desktop", "Mouse", "Keyboard"]
        self.var_sort_category = tk.StringVar(self)
        self.var_sort_category.set(categories[0])

        self.combobox_sort_category = ttk.Combobox(self, textvariable=self.var_sort_category, values=categories, font=font_style)
        self.combobox_sort_category.grid(row=0, column=2, padx=10, pady=10, sticky="e")

        self.btn_apply_sort_category = tk.Button(self, text="Apply", command=self.apply_sort_category,
                                                 font=font_style, padx=10, pady=5)
        self.btn_apply_sort_category.grid(row=1, column=2, padx=10, pady=20, sticky="n")

        self.btn_checkout = tk.Button(self, text="Checkout", command=self.checkout, font=font_style, padx=10, pady=5)
        self.btn_checkout.grid(row=9, column=1, padx=10, pady=10, sticky="w")

        self.update_product_list()

        self.btn_add_product.bind("<Enter>", lambda event, btn=self.btn_add_product: btn.config(bg='lightgray'))
        self.btn_add_product.bind("<Leave>", lambda event, btn=self.btn_add_product: btn.config(bg='SystemButtonFace'))

    def update_product_list(self):
        self.listbox_products.delete(0, tk.END)
        for product in self.computer_store.products:
            price_in_rupiah = locale.currency(product.price, grouping=True)
            display_text = f"{product.name} - Price: {price_in_rupiah} - Stock: {product.stock} - Category: {product.category}"
            self.listbox_products.insert(tk.END, display_text)

    def add_product(self):
        name = simpledialog.askstring("Input", "Enter product name:")
        if name is None:
            return

        price = self.get_validated_price()
        stock = self.get_validated_stock()
        category = simpledialog.askstring("Input", "Enter product category:")
        if category is None:
            return

        if price is not None and stock is not None:
            product = Product(name, price, stock, category)
            self.computer_store.add_product(product)
            self.update_product_list()
        else:
            messagebox.showwarning("Warning", "Invalid input. Please enter valid information.")

    def purchase_product(self):
        selected_product = self.get_selected_product()
        if selected_product:
            quantity = self.get_validated_quantity()
            self.process_purchase(selected_product, quantity)

    def process_purchase(self, selected_product, quantity):
        purchased_product = self.computer_store.purchase_product(selected_product, quantity)
        if purchased_product:
            self.shopping_cart.add_item(purchased_product, quantity)
            self.show_purchase_confirmation(purchased_product, quantity)
            self.update_cart()
            self.update_product_list()

    def show_purchase_confirmation(self, purchased_product, quantity):
        message = f"Product {purchased_product.name} purchased. Quantity: {quantity}"
        messagebox.showinfo("Purchase Confirmation", message)

    def checkout(self):
        total = self.shopping_cart.calculate_total()
        payment_method = self.var_payment_method.get()

        if self.confirm_checkout(total, payment_method):
            self.finalize_checkout(total, payment_method)

    def confirm_checkout(self, total, payment_method):
        confirmation_message = f"Total Purchase: {total:.2f}. Payment Method: {payment_method}. Confirm checkout?"
        return messagebox.askyesno("Checkout Confirmation", confirmation_message)

    def finalize_checkout(self, total, payment_method):
        message = f"Thank you for shopping!\nTotal Purchase: {total:.2f}. Payment Method: {payment_method}."
        messagebox.showinfo("Checkout", message)
        self.reset_checkout()

    def reset_checkout(self):
        self.shopping_cart = ShoppingCart()
        self.update_cart()
        self.var_payment_method.set("Cash")

    def update_cart(self):
        self.listbox_cart.delete(0, tk.END)
        for item in self.shopping_cart.items:
            # Convert price to Indonesian Rupiah (IDR)
            price_in_rupiah = locale.currency(item['product'].price, grouping=True)
            display_text = f"{item['product'].name} - Price: {price_in_rupiah} - Quantity: {item['quantity']} - Category: {item['product'].category}"
            self.listbox_cart.insert(tk.END, display_text)

        total = self.shopping_cart.calculate_total()
        formatted_total = locale.currency(total, grouping=True)

        self.entry_total.config(state=tk.NORMAL)
        self.entry_total.delete(0, tk.END)
        self.entry_total.insert(0, formatted_total)
        self.entry_total.config(state=tk.DISABLED)

    def get_selected_product(self):
        selected_index = self.listbox_products.curselection()
        if selected_index:
            return self.computer_store.products[selected_index[0]]
        return None

    def get_validated_price(self):
        return self.get_validated_input("Enter product price:", float, lambda x: x >= 0,
                                        "Price must be a non-negative number.")

    def get_validated_stock(self):
        return self.get_validated_input("Enter product stock:", int, lambda x: x >= 0,
                                        "Stock must be a non-negative integer.")

    def get_validated_quantity(self):
        return self.get_validated_input("Enter product quantity:", int, lambda x: x > 0,
                                        "Quantity must be a positive integer.")

    def get_validated_input(self, prompt, data_type, validation, error_message):
        while True:
            try:
                user_input = data_type(simpledialog.askstring("Input", prompt))
                if not validation(user_input):
                    raise ValueError(error_message)
                return user_input
            except ValueError as e:
                messagebox.showwarning("Warning", f"Invalid input: {e}")

    def apply_sort_category(self):
        selected_category = self.var_sort_category.get()
        self.filter_and_display_products(category=selected_category)

    def filter_and_display_products(self, search_term=None, sort_option=None, category=None):
    # Filter products based on search term and category
        filtered_products = self.computer_store.products
        if search_term:
            filtered_products = [product for product in filtered_products if search_term.lower() in product.name.lower()]
        if category and category != "All":
            filtered_products = [product for product in filtered_products if product.category == category]

    # Sort products based on sort option
        if sort_option == "Name (A-Z)":
            filtered_products.sort(key=lambda x: x.name)
        elif sort_option == "Name (Z-A)":
            filtered_products.sort(key=lambda x: x.name, reverse=True)
        elif sort_option == "Price (Low to High)":
            filtered_products.sort(key=lambda x: x.price)
        elif sort_option == "Price (High to Low)":
            filtered_products.sort(key=lambda x: x.price, reverse=True)

    # Display filtered and sorted products
        self.listbox_products.delete(0, tk.END)
        for product in filtered_products:
            price_in_rupiah = locale.currency(product.price, grouping=True)
            display_text = f"{product.name}\n  Price: {price_in_rupiah}\n  Stock: {product.stock}\n  Category: {product.category}\n{'='*50}"
            self.listbox_products.insert(tk.END, display_text)


if __name__ == "__main__":
    login_app = LoginApp()
    login_app.mainloop()

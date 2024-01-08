# Course: HDip in Computing in Data Analytics
# Module: Multi-Paradigm Programming
# Lecturer:Dominic Carr
# Project: Shop Project 
# Student: Sarah Hastings 
# Student Number: G00235562

# Importing the necessary libraries
from dataclasses import dataclass, field
from typing import List
import csv
import os


# Creation of data class, data container, like a struct in C for Proudct, Product Stock, Shop, Customer
# Data class with product name (string) and price(float)
@dataclass
class Product:
    name: str
    price: float = 0.0

# Data class with product (an instance of product) and quantity
@dataclass
class ProductStock:
    product: Product
    quantity: int

# Data class for representing a Shop, including cash and a list of ProductStock
@dataclass
class Shop:
    cash: float = 0.0
    stock: List[ProductStock] = field(default_factory=list)
    
    # Method to load shop data from a CSV file
    def load_shop_data(self, file_path):
        with open(file_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            first_row = next(csv_reader)
            # Set the shop's cash from the CSV file
            self.cash = float(first_row[0])
            # Iterate through each row in the CSV file to return the shop's stock
            for row in csv_reader:
                product = Product(row[0], float(row[1]))
                product_stock = ProductStock(product, float(row[2]))
                self.stock.append(product_stock)
    
    # Method to display shop information
    def display_shop(self):
        print(f'Shop has €{self.cash:.2f} in cash')
        # Iterate through each product in the shop's stock
        for item in self.stock:
            self.print_product(item.product)
            # Print details of the product
            print(f'The Shop has {item.quantity:.0f} of the above')
            print('-------------------')

    # Static method to print product information
    @staticmethod
    def print_product(product):
        print(f'\nPRODUCT NAME: {product.name} \nPRODUCT PRICE: €{product.price:.2f}')

# Data class for representing a Customer, including name, budget, and a shopping list
@dataclass
class Customer:
    name: str = ""
    budget: float = 0.0
    shopping_list: List[ProductStock] = field(default_factory=list)

# Data class for representing an OrderProcessor
@dataclass
class OrderProcessor:
    # Static method to process an order for a customer and update the shop
    @staticmethod
    def process_order(customer, shop):
        # Displaying processing message
        print("Processing order...")
        print("-------------------")
        total_order_cost = 0
        #Iterate through each item in the customer's shopping list
        for item in customer.shopping_list:
            found_in_stock = False
            # Checking if the product is in the shop's stock
            for prod in shop.stock:
                if item.product.name.lower() == prod.product.name.lower():
                    found_in_stock = True
                    # Checking quantity available in stock
                    if prod.quantity >= item.quantity:
                        item_cost = item.quantity * prod.product.price
                        # Checking if customer has enough budget
                        if customer.budget >= item_cost:
                            # Deducting cost, updating funds, and reducing stock quantity
                            shop.cash += item_cost
                            customer.budget -= item_cost
                            print(f"€{item_cost:.2f} deducted from the customer funds for {item.quantity:.0f} of {item.product.name}.\n")
                            prod.quantity -= item.quantity
                            total_order_cost += item_cost
                        else:
                            print(f"Insufficient funds, {customer.name} has €{customer.budget:.2f} but €{item_cost:.2f} required for {item.product.name}\n")
                    elif prod.quantity < item.quantity:
                        # If stock quantity is less than requested, update cost for available stock
                        print(f"We only have {prod.quantity:.0f} of {prod.product.name} at the moment. You will be charged only for the products sold.\n")
                        item_cost = prod.quantity * prod.product.price
                        if customer.budget >= item_cost:
                            # Deducting cost, updating funds, and reducing stock quantity
                            print(f"€{item_cost:.2f} deducted from the customer funds for {prod.quantity:.0f} unit(s) of {item.product.name}.\n")
                            prod.quantity -= prod.quantity
                            shop.cash += item_cost
                            customer.budget -= item_cost
                            total_order_cost += item_cost
                        else:
                            print(f"Insufficient funds, {customer.name} has €{customer.budget:.2f} but €{item_cost:.2f} required for {item.product.name}\n")
            if not found_in_stock:
                print(f"Sorry, {item.product.name} is not available in the shop's stock.\n")

        print(f"TOTAL ORDER COST: €{total_order_cost:.2f}\n")
        print(f"UPDATING CASH\n-------------------\nCustomer {customer.name} has €{customer.budget:.2f} left.\n")

# Data class for representing a ShopApplication
@dataclass
class ShopApplication:
    shop: Shop
    order_processor: OrderProcessor
    
    # Constructor to initialize Shop and OrderProcessor
    def __init__(self):
        self.shop = Shop()
        self.order_processor = OrderProcessor()
    # Method to clear the screen
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    # Method to create and stock the shop using data from a file
    def create_and_stock_shop(self, file_path):
        self.shop.load_shop_data(file_path)
    # Method to read customer data from a file
    def read_customer(self):
        file_name = input("Please enter your customer file name: ")
        file_path = f"../{file_name}.csv"

        try:
            with open(file_path) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                first_row = next(csv_reader)
                customer = Customer(first_row[0], float(first_row[1]))
                # Iterating through each row in the customer's CSV file to populate the shopping list
                for row in csv_reader:
                    name = row[0]
                    quantity = float(row[1])
                    product = Product(name)
                    product_stock = ProductStock(product, quantity)
                    customer.shopping_list.append(product_stock)

                return customer
        except Exception as err:
            print(f"Invalid customer file name: {file_name}.")
            self.return_to_menu()

    # Method to print customer information
    def print_customer(self, customer):
        print(f'CUSTOMER NAME: {customer.name} \nCUSTOMER BUDGET: €{customer.budget:.2f}')
        print("-------------------\n")
        print("CUSTOMER ORDER:")
        # Iterating through each item in the customer's shopping list
        for item in customer.shopping_list:
            # Finding the product price from the shop's stock
            product_price = next((prod.product.price for prod in self.shop.stock if prod.product.name.lower() == item.product.name.lower()), 0.0)
            print(f'\nPRODUCT NAME: {item.product.name} \nPRODUCT PRICE: €{product_price:.2f}')
            print(f"{customer.name} ORDERS {item.quantity:.0f} OF ABOVE PRODUCT\n")
            print("*************************")
        print("Please wait while we check our stock...")
        print("-------------------\n")

      # Method for live order where the user interacts with the application
    def live_order(self):
        customer = Customer()
        customer.name = input("What is your name? ")
        # Validating and setting the customer's budget
        while True:
            try:
                customer.budget = float(input("What is your budget? "))
                break
            except ValueError:
                print("Error: Please enter your budget as a number ")

        product_name = input("Please enter the name of the product you are looking for ")
        product = Product(product_name)
        # Validating and setting the quantity of the product
        while True:
            try:
                quantity = int(input(f"Please enter the quantity of {product_name} you are looking for "))
                break
            except ValueError:
                print("Error: Please enter the quantity as an integer ")

        product_stock = ProductStock(product, quantity)
        customer.shopping_list.append(product_stock)
        # Asking if the customer wants to order additional items
        additional_items = input("Would you like to order additional items? (Y/N): ").upper()
        # Validating the input for additional items
        while additional_items not in ['Y', 'N']:
            print("Invalid input. Please enter 'Y' for Yes or 'N' for No.")
            additional_items = input("Would you like to order additional items? (Y/N): ").upper()
        # Loop for ordering additional items
        while additional_items == "Y":
            name = input("What would you like to buy?: ").lower()
            quantity = int(input("How many would you like to buy?: "))
            product = Product(name)
            product_stock = ProductStock(product, quantity)
            customer.shopping_list.append(product_stock)
            additional_items = input("Would you like to order additional items? (Y/N): ").upper()
            # Validating the input for additional items
            while additional_items not in ['Y', 'N']:
                print("Invalid input. Please enter 'Y' for Yes or 'N' for No.")
                additional_items = input("Would you like to order additional items? (Y/N): ").upper()

        return customer

    # Method to return to the main menu
    def return_to_menu(self):
        menu = input("\nPress any key to return to the main menu: ")
        if menu:
            self.display_menu()
    # Method to display the main menu
    def display_menu(self):
        self.clear_screen()
        print("\n")
        print("\t\tWelcome to my shop")
        print("\t\t----------------------------------")
        print("\t\tMain Menu")
        print("\t\tSelect 1 for Shop Overview")
        print("\t\tSelect 2 for Batch orders")
        print("\t\tSelect 3 for Live orders")
        print("\t\tSelect 0 to Exit Shop Application")

    # Main method to run the shop application
    def main(self):
        while True:
            self.display_menu()
            choice = input("\n Please select an option from the main menu: ")

            if choice == "1":
                print("1: SHOP OVERVIEW")
                self.shop.display_shop()
                self.return_to_menu()

            elif choice == "2":
                print("2: BATCH ORDERS")
                customer = self.read_customer()
                if customer:
                    self.print_customer(customer)
                    self.order_processor.process_order(customer, self.shop)
                    self.return_to_menu()

            elif choice == "3":
                print("3: *** LIVE MODE ***")
                print("Please choose from our products listed below:\n")
                self.shop.display_shop()
                customer = self.live_order()
                self.print_customer(customer)
                self.order_processor.process_order(customer, self.shop)
                self.return_to_menu()

            elif choice == "0":
                print("\nThank you for shopping here. Goodbye.")
                break

            else:
                self.display_menu()

# Entry point of the application
if __name__ == "__main__":
    # Creating an instance of ShopApplication
    shop_app = ShopApplication()
    # Loading shop data from a file
    shop_app.create_and_stock_shop('../stock.csv') 
    # Running the main functionality of the shop application
    shop_app.main()

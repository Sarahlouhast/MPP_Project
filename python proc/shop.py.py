# Course: HDip in Computing in Data Analytics
# Module: Multi-Paradigm Programming
# Lecturer:Dominic Carr
# Project: Shop Project 
# Student: Sarah Hastings 
# Student Number: G00235562


'''
# ===== ===== ===== ===== ===== =====
# Importing external libraries
# ===== ===== ===== ===== ===== =====
'''
# Import python libraries
from dataclasses import dataclass, field
from typing import List
import csv
import os 
import time
import itertools

# Note to print shop.py in the Command Prompt type the following: python shop.py

'''
# ===== ===== ===== ===== ===== =====
# Definiton of dataclasses
# ===== ===== ===== ===== ===== =====
'''
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

# Data class with cash(float) and stock(list of Product Stock)
@dataclass 
class Shop:
    cash: float = 0.0
    stock: List[ProductStock] = field(default_factory=list)
# Data class with customer name(string), budget(float), shopping list(list of proudct stock)
@dataclass
class Customer:
    name: str = ""
    budget: float = 0.0
    shopping_list: List[ProductStock] = field(default_factory=list)

'''
# ===== ===== ===== ===== ===== =====
# Definition of the functions
# ===== ===== ===== ===== ===== =====
'''
# Create a function to create a shop
def create_and_stock_shop():
    # Initialise an instance of the shop data class
    s = Shop()
    # Read in stock csv file and get shop cash from first row
    with open('../stock.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        # Set the shop's cash based on the first value in the CSV file
        first_row = next(csv_reader)
        s.cash = float(first_row[0])
        # Iterate through rows of csv file to initialise of product, product stock and append the ProductStock instance to the shop's stock list
        for row in csv_reader: 
            p = Product(row[0], float(row[1]))  
            ps = ProductStock(p, float(row[2]))
            s.stock.append(ps)
    # Return the full initalised shop dataclass
    return s

# Function to read in customer csv file, customer enters file name only
def read_customer():
    # Prompt user to input customer file name
    path = input("Please enter your customer file name: ")
    # Create a file name including the file path
    path = "../" + str(path) + ".csv"
    try:
        # Open and read the csv file
        with open(path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            first_row = next(csv_reader)
            # Initialise customer with name column 0 of row 0, customer budget column 1 of row 0
            c = Customer(first_row[0], float(first_row[1]))
            # Iterate through the rest of the rows of the file to create product, product stock and append to customer's shopping list
            for row in csv_reader:
                # Extract name and quantity from the CSV row
                name = row[0]
                quantity = float(row[1])
                # Create a Product instance with the extracted name
                p = Product(name)
                # Create a ProductStock instance with the Product and quantity
                ps = ProductStock(p, quantity)
                # Append the ProductStock instance to the customer's shopping list
                c.shopping_list.append(ps)
            # Return the customer instance with values    
            return c 
    # Create exception in case invalid file name is input
    except Exception as err:
        print("Invalid customer file name. ")
        # Return the user to the menu
        return_to_menu()
        
# Display the name and price of a product 
def print_product(p):
    print(f'\nPRODUCT NAME: {p.name} \nPRODUCT PRICE: €{p.price:.2f}')
    
# Display the cash in the shop and each product name, price and quantity 
def print_shop(s):
    # Print the total cash in the shop
    print(f'Shop has €{s.cash:.2f} in cash')
    # Iterate through each product stock in the shop's stock and print the details and quantity
    for item in s.stock:
        print_product(item.product)
        print(f'The Shop has {item.quantity:.0f} of the above')
        # Print for readability
        print('-------------------')

# Return to main menu after a key is pressed
def return_to_menu():
    # Prompt the user to press any key
    menu = input("\nPress any key to return to main menu: ")
    # Always true, ensuring the below is always excuted to display the main menu options
    if True:
        display_menu()

# Display the main menu options       
def display_menu():
    # Clear screen of any previous input for readability
    clear()
    # Print the main menu options
    print("\n")
    print("\t\tWelcome to my shop")
    print("\t\t----------------------------------")
    print("\t\tMain Menu")
    print("\t\tSelect 1 for Shop Overview")
    print("\t\tSelect 2 for Batch orders")
    print("\t\tSelect 3 for Live orders")
    print("\t\tSelect 0 to Exit Shop Application")

# Prcoess the order - update shop stock, shop cash, customer cash
def process_order(c, s):
    # Display processing message
    print("Processing order...")
    print("-------------------")
    # Initialize total order cost
    total_order_cost = 0  
    
    # Iterate through each item in the customer's shopping list
    for item in c.shopping_list:
        found_in_stock = False

        # Check if each item is in the shop's stock
        for prod in s.stock:
            # If item is a shop stock item
            if item.product.name.lower() == prod.product.name.lower():
                found_in_stock = True

                # Check if the quantity in stock can fulfill the order
                if prod.quantity >= item.quantity:
                    # Calculate cost
                    item_cost = item.quantity * prod.product.price
                    # Check customer has enough cash to cover the cost of this purchase
                    if c.budget >= item_cost:
                        # Process sale, update shop cash
                        s.cash += item_cost
                        # Process sale, update customer cash
                        c.budget -= item_cost
                        # Process sale, decrease stock quantity of sold items
                        print(f"€{item_cost:.2f} deducted from the customer funds for {item.quantity:.0f} of {item.product.name}.\n")
                        prod.quantity -= item.quantity
                        # Accumulate the costs only if the order is successful
                        total_order_cost += item_cost
                    else:
                        # Insufficient funds message
                        print(f"Insufficient funds, {c.name} has €{c.budget:.2f} but €{item_cost:.2f} required for {item.product.name}\n")

                elif prod.quantity < item.quantity:
                    # Partial order message
                    print(f"We only have {prod.quantity:.0f} of {prod.product.name} at the moment. You will be charged only for the products sold.\n");
                    # Calculate cost based on partial order
                    item_cost = prod.quantity * prod.product.price
                    if c.budget >= item_cost:
                        print(f"€{item_cost:.2f} deducted from the customer funds for {prod.quantity:.0f} unit(s) of {item.product.name}.\n")
                        # Process sale, decrease stock
                        prod.quantity -= prod.quantity
                        # Process sale, increase shop cash after sale
                        s.cash += item_cost
                        # Deduct sale amount for this item from customer cash
                        c.budget -= item_cost
                        # Accumulate the costs only if the order is successful
                        total_order_cost += item_cost
                    else:
                        # Insufficient funds message
                        print(f"Insufficient funds, {c.name} has €{c.budget:.2f} but €{item_cost:.2f} required for {item.product.name}\n")
        # If the item is not found in stock
        if not found_in_stock:
            print(f"Sorry, {item.product.name} is not available in the shop's stock.\n")

    # Display the total order cost once after checking the stock
    print(f"TOTAL ORDER COST: €{total_order_cost:.2f}\n")
    print(f"UPDATING CASH\n-------------------\nCustomer {c.name} has €{c.budget:.2f} left.\n")


# Display customer details
def print_customer(c, s):
    # Print customer name and budget
    print(f'CUSTOMER NAME: {c.name} \nCUSTOMER BUDGET: €{c.budget:.2f}')
    print("-------------------\n")
    print("CUSTOMER ORDER:")
    
    # Iterate through the customer's shopping list
    for item in c.shopping_list:
        # Find the product price in the stock - next function used to find the price of the product, if the product is not found, default to 0.0
        product_price = next((prod.product.price for prod in s.stock if prod.product.name.lower() == item.product.name.lower()), 0.0)
        
        # Print product details and order quantity
        print(f'\nPRODUCT NAME: {item.product.name} \nPRODUCT PRICE: €{product_price:.2f}')
        print(f"{c.name} ORDERS {item.quantity:.0f} OF ABOVE PRODUCT\n")
        # Print for readability
        print("*************************")
    # Print for readability
    print("Please wait while we check our stock...")
    print("-------------------\n")

# Interactive mode to deal with live customer orders        
def live_order(s):
    # Intialise an array to store the shopping list
    shopping_list = []
    # Create a new instance of the Customer class
    c=Customer()
    # Prompt the customer to enter their name
    c.name = input("What is your name? ")
    while True:
        try:
            # Prompt customer to enter their budget  
            c.budget = float(input("What is your budget? "))
            break
        # Display error message incase a number is not entered
        except ValueError:
            print("Error: Please enter your budget as an number ")
    # Prompt customer to enter product name and store as a Product 
    product  = input("Please enter the name of the product you are looking for ")
    p = Product(product)

    # Prompt customer to enter quantity of item
    while True:
        try:
            quantity = int(input(f"Please enter the quantity of {product} you are looking for "))
            break
        # Display error message incase a number is not entered
        except ValueError:
            print("Error: Please enter the quantity as an integer ")
    # Create a ProductStock using the product and quantity
    ps = ProductStock(p, quantity)    
    # Append the items to the customers shopping list
    c.shopping_list.append(ps)

    # Ask customer if wants to buy additional items
    additional_items = input("Would you like to order additional items? (Y/N): ").upper()

    # Display error message if does not enter Y, N
    while additional_items not in ['Y', 'N']:
        print("Invalid input. Please enter 'Y' for Yes or 'N' for No.")
        additional_items = input("Would you like to order additional items? (Y/N): ").upper()

    # Ask if the customer wants to order more additional items
    while additional_items == "Y":
        name = input("What would you like to buy?: ").lower()
        quantity = int(input("How many would you like to buy?: "))
        p = Product(name)
        ps = ProductStock(p, quantity)
        c.shopping_list.append(ps)
        
        additional_items = input("Would you like to order additional items? (Y/N): ").upper()

        while additional_items not in ['Y', 'N']:
            print("Invalid input. Please enter 'Y' for Yes or 'N' for No.")
            additional_items = input("Would you like to order additional items? (Y/N): ").upper()

    # Return a customer with their shopping list
    return c

# Clear the screen for readability
def clear():
    # Check if the platform is Windows
    if os.name == 'nt':
        os.system('cls')  # Use 'cls' to clear the screen on Windows
    else:
        os.system('clear')  # Use 'clear' for Unix-based systems


# Main function - is the start of the program - controls all other functionality of the program
def main():
    #Clear screen for readability
    #clear()
    #print("Setting up the shop for today ...\n")
    #time.sleep(1)  # Add this line to pause for 1 seconds, these were used in debugging
    # Create the shop by calling this function
    s = create_and_stock_shop()
 
    # A forever loop 
    while True:
        # Display the user menu
        display_menu()
        # Store input as choice
        choice = input("\n Please select option from the main menu: ")

        # If option 1 is selected, print the current shop state by calling print_shop
        if (choice =="1"):
            print("1: SHOP OVERVIEW")
            print_shop(s)
            return_to_menu()    

        # If option 2 is selected, prompt user to enter customer file name by read_customer function
        elif (choice =="2"):    
            
            print("2: BATCH ORDERS")
            # Create a customer 
            c = read_customer()
            # If a customer has been created, print their order
            if c:
                print_customer(c,s)
                # Process the customers order
                process_order(c,s)

            return_to_menu() 

        # If option 3 is selected, create customer by calling the live_order function   
        elif (choice=="3"):            
            print("3:*** LIVE MODE ***")
            print("Please choose from our products listed below:\n")
            print_shop(s)
            c =live_order(s)
            # Print customer details
            print_customer(c,s)
            # Process the customers order
            process_order(c,s)

            # Return to menu
            return_to_menu() 

        # Exit option if user selects 0, exit the program
        elif (choice == "0"):
            # Exit clause to break out out of the entire program and back to the command prompt
            print("\nThank you for shopping here. Goodbye.")
            break;

    # For anything else, display the menu
        else: 
            display_menu()

if __name__ == "__main__":
    # Only execute if run as a script

    # Call the main function above
    main()


from datetime import datetime

# Computerized Sales, Inventory, and Expense Monitoring System for “Kuya Pares”

USERNAME = "owner"
PASSWORD = "kuYaPares"

# LOG IN SYSTEM
def login():
    print("\t====================================")
    print("\t          KUYA PARES LOGIN")
    print("\t====================================")

    attempts = 3
    while attempts > 0:
        username = input("\tUsername: ").strip()
        password = input("\tPassword: ").strip()

        if username == USERNAME and password == PASSWORD:
            print("\tLogin successful! Welcome to Kuya Pares.")
            return True

        attempts -= 1
        print(f"Incorrect username or password. Attempts left: {attempts}")

    print("Too many failed attempts. Try again Next Time.")
    return False

# DASHBOARD OF THE SYSTEM
def main():
    if not login():
        return

    while True:
        print("\t====================================")
        print("\tKUYA PARES MANAGEMENT SYSTEM DASHBOARD")
        print("\t====================================")
        print("\t1. New Order")
        print("\t2. Manage Products")
        print("\t3. Manage Inventory")
        print("\t4. Expenses Module")
        print("\t5. Daily Sales and Profit Report")
        print("\t6. Exit")

        choice = input("\nEnter your choice: ").strip()
        if choice == "1":
            new_order()
        elif choice == "2":
            manage_products()
        elif choice == "3":
            manage_inventory()
        elif choice == "4":
            expenses_module()
        elif choice == "5":
            sales_report()
        elif choice == "6":
            print("Thank you for using Kuya Pares Management System!")
            break
        else:
            print("Invalid choice. Please choose 1-6.")

products = [
    {"id": 1, "name": "Beef Pares", "price": 80.00, "stock": 50},
    {"id": 2, "name": "Siomai Rice", "price": 25.00, "stock": 20},
    {"id": 3, "name": "Rice", "price": 15.00, "stock": 10},
    {"id": 4, "name": "Siomai", "price": 10.00, "stock": 5},
    {"id": 5, "name": "Lechon Pares", "price": 90.00, "stock": 50}
]

inventory = [
    {"id": 1, "name": "Beef", "quantity": 7.85, "unit": "kg"},
    {"id": 2, "name": "Lechon", "quantity": 5.85, "unit": "kg"},
    {"id": 3, "name": "Siomai", "quantity": 5, "unit": "pcs"},
    {"id": 4, "name": "Rice", "quantity": 8.55, "unit": "kg"},
    {"id": 5, "name": "Sili", "quantity": 10.5, "unit": "kg"},
    {"id": 6, "name": "Toyo", "quantity": 10, "unit": "pcs"},
    {"id": 7, "name": "Bawang", "quantity": 10, "unit": "pcs"},
    {"id": 8, "name": "Mantika", "quantity": 30, "unit": "kg"},
]

sales = []
expenses = []
receipt_number = 1

def money(amount):
    return f"P{amount:,.2f}"

def show_products():
    print("\tAVAILABLE PRODUCTS")
    print("-" * 60)
    print(f"{'ID':<4}{'Product Name':<25}{'Price':>12}{'Stock':>10}")
    print("-" * 60)
    for product in products:
        print(f"{product['id']:<4}{product['name']:<25}{money(product['price']):>12}{product['stock']:>10}")
    print("-" * 60)

#CHOICES NUM: 1
def new_order():
    global receipt_number
    cart = []
    show_products()

    while True:
        try:
            product_id = int(input("Enter product ID (or 0 to finish): "))
            if product_id == 0:
                break
            product = next((p for p in products if p["id"] == product_id), None)
            if product is None:
                print("Invalid product ID.")
                continue

            quantity = int(input("Enter quantity: "))
            if quantity <= 0:
                print("Quantity must be at least 1.")
            elif quantity > product["stock"]:
                print("Not enough stock.")
            else:
                cart.append({"id": product["id"], "name": product["name"],
                             "price": product["price"], "quantity": quantity})
                product["stock"] -= quantity
                print(f"Added {quantity} x {product['name']} = {money(product['price'] * quantity)}")
        except ValueError:
            print("Please enter a valid number.")

    if not cart:
        print("No items ordered.")
        return

    total = sum(item["price"] * item["quantity"] for item in cart)
    
    print("\t========== ORDER OF SUMMARY ==========")
    print(f"{'Product':<24}{'Qty':>5}{'Price':>12}{'Total':>12}")
    print("-" * 53)
    for item in cart:
        line_total = item["price"] * item["quantity"]
        print(f"{item['name']:<24}{item['quantity']:>5}{money(item['price']):>12}{money(line_total):>12}")
    print("-" * 53)
    print(f"Total Amount: {money(total)}")

    try:
        cash = float(input("Cash Received: P"))
    except ValueError:
        print("Invalid cash amount. Order cancelled.")
        for item in cart:
            next(p for p in products if p["id"] == item["id"])["stock"] += item["quantity"]
        return

    if cash < total:
        print("Insufficient payment. Order cancelled.")
        for item in cart:
            next(p for p in products if p["id"] == item["id"])["stock"] += item["quantity"]
        return

    paid = input("Mark order as paid? (y/n): ").strip().lower() in ("y", "yes")
    sale = {
        "receipt": receipt_number,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "items": cart,
        "total": total,
        "cash": cash,
        "change": cash - total,
        "paid": paid,
    }
    sales.append(sale)

    print("\n========== RECEIPT ==========")
    print(f"Receipt No.: {receipt_number}")
    print(f"Date: {sale['date']}")
    for item in cart:
        print(f"{item['name']} x {item['quantity']} - {money(item['price'] * item['quantity'])}")
    print(f"Total: {money(total)}")
    print(f"Cash: {money(cash)}")
    print(f"Change: {money(cash - total)}")
    print(f"Payment Status: {'Paid' if paid else 'Unpaid'}")
    print("Order saved successfully!")
    receipt_number += 1

#CHOICES NUM: 2
def manage_products():
    while True:
        print("\n========== MANAGE PRODUCTS ==========")
        print("1. Add Product")
        print("2. Update Product")
        print("3. View Products")
        print("4. Delete Product")
        print("5. Back to Main Menu")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            name = input("Enter product name: ").strip()
            try:
                price = float(input("Enter product price: P"))
                stock = int(input("Enter initial stock: "))
                if not name or price < 0 or stock < 0:
                    print("Name, price, and stock must be valid.")
                    continue
                new_id = max((p["id"] for p in products), default=0) + 1
                products.append({"id": new_id, "name": name, "price": price, "stock": stock})
                print("Product added successfully!")
            except ValueError:
                print("Invalid price or stock.")

        elif choice == "2":
            show_products()
            try:
                product_id = int(input("Enter product ID to update: "))
                product = next((p for p in products if p["id"] == product_id), None)
                if not product:
                    print("Product not found.")
                    continue
                new_name = input(f"New name [{product['name']}]: ").strip()
                new_price = input(f"New price [{product['price']:.2f}]: ").strip()
                new_stock = input(f"New stock [{product['stock']}]: ").strip()
                if new_name:
                    product["name"] = new_name
                if new_price:
                    product["price"] = float(new_price)
                if new_stock:
                    product["stock"] = int(new_stock)
                print("Product updated successfully!")
            except ValueError:
                print("Invalid input.")

        elif choice == "3":
            show_products()

        elif choice == "4":
            show_products()
            try:
                product_id = int(input("Enter product ID to delete: "))
                product = next((p for p in products if p["id"] == product_id), None)
                if product:
                    products.remove(product)
                    print("Product deleted successfully!")
                else:
                    print("Product not found.")
            except ValueError:
                print("Invalid product ID.")

        elif choice == "5":
            break
        else:
            print("Invalid choice. Try again.")

#CHOICES NUM: 3
def manage_inventory():
    while True:
        print("\n========== INVENTORY ==========")
        print(f"{'ID':<4}{'Item Name':<22}{'Quantity':>12}{'Unit':>8}")
        print("-" * 48)
        for item in inventory:
            print(f"{item['id']:<4}{item['name']:<22}{item['quantity']:>12}{item['unit']:>8}")
        print("\n1. Add Stock")
        print("2. Update Stock")
        print("3. View Inventory")
        print("4. Back to Main Menu")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            name = input("Enter ingredient name: ").strip()
            unit = input("Enter unit (kg, L, pcs): ").strip() or "pcs"
            try:
                quantity = float(input("Enter quantity to add: "))
                if quantity <= 0 or not name:
                    print("Enter a valid name and positive quantity.")
                    continue
                new_id = max((i["id"] for i in inventory), default=0) + 1
                inventory.append({"id": new_id, "name": name, "quantity": quantity, "unit": unit})
                print("Stock added successfully!")
            except ValueError:
                print("Invalid quantity.")

        elif choice == "2":
            try:
                item_id = int(input("Enter item ID: "))
                item = next((i for i in inventory if i["id"] == item_id), None)
                if not item:
                    print("Item not found.")
                    continue
                quantity = float(input("Enter new quantity: "))
                if quantity < 0:
                    print("Quantity cannot be negative.")
                    continue
                item["quantity"] = quantity
                print("Stock updated successfully!")
            except ValueError:
                print("Invalid input.")

        elif choice == "3":
            pass
            
        elif choice == "4":
            break
        else:
            print("Invalid choice. Try again.")

#CHOICES NUM: 4
def expenses_module():
    print("\n========== RECORD EXPENSE ==========")
    category = input("Expense category (Ingredients, Supplies, Utilities, Other): ").strip()
    description = input("Description: ").strip()
    try:
        amount = float(input("Amount spent: P"))
        if amount <= 0:
            print("Amount must be greater than zero.")
            return
    except ValueError:
        print("Invalid amount.")
        return

    expenses.append({
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "category": category or "Other",
        "description": description,
        "amount": amount,
    })
    print("Expense recorded successfully!")

#CHOICES NUM: 5
def sales_report():
    date_text = input(f"Enter date (YYYY-MM-DD) [default: {datetime.now().date()}]: ").strip()
    report_date = date_text or str(datetime.now().date())
    todays_sales = [sale for sale in sales if sale["date"].startswith(report_date)]
    todays_expenses = [expense for expense in expenses if expense["date"].startswith(report_date)]
    total_sales = sum(sale["total"] for sale in todays_sales if sale["paid"])
    total_expenses = sum(expense["amount"] for expense in todays_expenses)
    total_orders = len(todays_sales)
    paid_orders = sum(1 for sale in todays_sales if sale["paid"])
    unpaid_orders = total_orders - paid_orders

    print("\n========== DAILY SALES AND PROFIT REPORT ==========")
    print(f"Date: {report_date}")
    print(f"Total Orders: {total_orders}")
    print(f"Paid Orders: {paid_orders}")
    print(f"Unpaid Orders: {unpaid_orders}")
    print(f"Total Paid Sales: {money(total_sales)}")
    print(f"Total Expenses: {money(total_expenses)}")
    print(f"Profit (Paid Sales - Expenses): {money(total_sales - total_expenses)}")

    print("\nSales Details:")
    print(f"{'No.':<6}{'Date & Time':<22}{'Status':<12}{'Amount':>10}")
    print("-" * 50)
    if not todays_sales:
        print("No sales recorded.")
    for sale in todays_sales:
        print(f"{sale['receipt']:<6}{sale['date']:<22}{('Paid' if sale['paid'] else 'Unpaid'):<12}{money(sale['total']):>10}")

    print("\nExpenses:")
    print(f"{'Date & Time':<22}{'Category':<18}{'Amount':>10}")
    print("-" * 50)
    if not todays_expenses:
        print("No expenses recorded.")
    for expense in todays_expenses:
        print(f"{expense['date']:<22}{expense['category']:<18}{money(expense['amount']):>10}")

# Main Important Code to run the whole system
if __name__ == "__main__":
    main()
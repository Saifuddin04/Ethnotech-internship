import mysql.connector

# ---------------- DATABASE CONNECTION ----------------
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="admin", 
        database="food_delivery"
    )


# ---------------- ADD CUSTOMER ----------------
def add_customer():
    name = input("Enter Name: ")
    phone = input("Enter Phone: ")
    address = input("Enter Address: ")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO Customer (name, phone, address) VALUES (%s, %s, %s)",
        (name, phone, address)
    )

    conn.commit()
    print("✅ Customer Added!")

    cursor.close()
    conn.close()


# ---------------- VIEW RESTAURANTS ----------------
def view_restaurants():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Restaurant")
    data = cursor.fetchall()

    print("\n🍽 Restaurants:")
    for r in data:
        print(f"ID: {r[0]} | Name: {r[1]} | Location: {r[2]}")

    cursor.close()
    conn.close()


# ---------------- VIEW FOOD ITEMS ----------------
def view_food_items():
    restaurant_id = input("Enter Restaurant ID: ")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT food_id, name, price FROM Food_Item WHERE restaurant_id = %s",
        (restaurant_id,)
    )

    items = cursor.fetchall()

    print("\n🍔 Food Items:")
    for item in items:
        print(f"ID: {item[0]} | {item[1]} | ₹{item[2]}")

    cursor.close()
    conn.close()


# ---------------- CREATE ORDER ----------------
def create_order():
    customer_id = input("Enter Customer ID: ")
    delivery_id = input("Enter Delivery Person ID: ")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO Orders (customer_id, delivery_id, order_date, status, total_amount) VALUES (%s, %s, NOW(), %s, %s)",
        (customer_id, delivery_id, "Pending", 0)
    )

    conn.commit()
    order_id = cursor.lastrowid

    print(f"🛒 Order Created! Order ID: {order_id}")

    cursor.close()
    conn.close()

    return order_id


# ---------------- ADD ITEM TO ORDER ----------------
def add_item_to_order(order_id):
    food_id = input("Enter Food ID: ")
    quantity = int(input("Enter Quantity: "))

    conn = get_connection()
    cursor = conn.cursor()

    # Insert into Order_Item
    cursor.execute(
        "INSERT INTO Order_Item (order_id, food_id, quantity) VALUES (%s, %s, %s)",
        (order_id, food_id, quantity)
    )

    # Update total
    cursor.execute(
        "SELECT price FROM Food_Item WHERE food_id = %s",
        (food_id,)
    )
    price = cursor.fetchone()[0]

    total_add = price * quantity

    cursor.execute(
        "UPDATE Orders SET total_amount = total_amount + %s WHERE order_id = %s",
        (total_add, order_id)
    )

    conn.commit()
    print("✅ Item added to order!")

    cursor.close()
    conn.close()


# ---------------- VIEW ORDER DETAILS ----------------
def view_order(order_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT total_amount, status FROM Orders WHERE order_id = %s",
        (order_id,)
    )
    order = cursor.fetchone()

    print(f"\n🧾 Order ID: {order_id}")
    print(f"Total: ₹{order[0]}")
    print(f"Status: {order[1]}")

    cursor.execute("""
        SELECT F.name, OI.quantity
        FROM Order_Item OI
        JOIN Food_Item F ON OI.food_id = F.food_id
        WHERE OI.order_id = %s
    """, (order_id,))

    items = cursor.fetchall()

    print("\nItems:")
    for item in items:
        print(f"{item[0]} x {item[1]}")

    cursor.close()
    conn.close()


# ---------------- MAIN MENU ----------------
def main():
    while True:
        print("\n==== ONLINE FOOD DELIVERY SYSTEM ====")
        print("1. Add Customer")
        print("2. View Restaurants")
        print("3. View Food Items")
        print("4. Create Order")
        print("5. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            add_customer()

        elif choice == "2":
            view_restaurants()

        elif choice == "3":
            view_food_items()

        elif choice == "4":
            order_id = create_order()
            while True:
                add_more = input("Add item to this order? (y/n): ")
                if add_more.lower() == "y":
                    add_item_to_order(order_id)
                else:
                    break
            view_order(order_id)

        elif choice == "5":
            print("👋 Goodbye!")
            break

        else:
            print("❌ Invalid choice!")


if __name__ == "__main__":
    main()
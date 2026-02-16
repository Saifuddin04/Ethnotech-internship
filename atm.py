balance = 1000
password = "1234"


def login():
    for attempt in range(3):
        print("==========================s")
        entered = input("Enter password: ")
        print("==========================")

        if entered == password:
            print("Login successful!\n")
            return True
        else:
            print("Wrong password")

    print("Too many attempts!")
    return False


def check_balance():
    print(f"Current Balance: ₹{balance}")


def deposit():
    global balance
    amount = float(input("Enter amount to deposit: ₹"))

    if amount <= 0:
        print("Invalid amount")
        return

    balance += amount
    print("Deposit successful!")


def withdraw():
    global balance
    amount = float(input("Enter amount to withdraw: ₹"))

    if amount <= 0:
        print("Invalid amount")
        return

    if amount > balance:
        print("Insufficient balance")
        return

    balance -= amount
    print("Please collect your cash")


def menu():
    while True:
        print("\n====== ATM MENU ======")
        print("1. Check Balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Exit")

        choice = input("Choose option: ")

        if choice == "1":
            check_balance()

        elif choice == "2":
            deposit()
            check_balance()

        elif choice == "3":
            check_balance()
            withdraw()
            check_balance()

        elif choice == "4":
            print("Thank you for using the ATM")
            break

        else:
            print("Invalid choice")



print("Welcome to Python Bank ATM\n")

if login():
    menu()
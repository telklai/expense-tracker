import sqlite3 
import datetime

conn = sqlite3.connect("expenses.db")
cur = conn.cursor()

while True:
    print("select an option:")
    print("1. Enter a new expense")
    print("2. View expense summary")

    choice = int(input())

    if choice == 1:
        date = input("Enter the date of the expense (YYYY-MM-DD): ")
        description = input("Enter the description of the expense: ")

        cur.execute("SELECT DISTINCT catagory FROM expenses")

        catagories = cur.fetchall()

        print("Select a catagory by number:")
        for idx, catagory in enumerate(catagories):
            print(f"{idx + 1}. {catagory[0]}")
        print(f"{len(catagories) + 1}. Create a new catagory")

        catagory_choice = int(input())
        if catagory_choice == len(catagories) + 1:
            catagory = input("Enter the new catagory name: ")
        else:
            catagory = catagories[catagory_choice - 1] [0]

        price = input("Enter the price of the expense: ")

        cur.execute("INSERT INTO expenses (Date, description, catagory, price) VALUES (?, ?, ?, ?)", (date, description, catagory, price))

        conn.commit()
        
    elif choice == 2:
        print("Select an option:")
        print("1. View all expenses")
        print("2. View monthly expenses by catagory")

        view_choice = int(input())
        if view_choice == 1:
            cur.execute("SELECT * FROM expenses")
            expenses = cur.fetchall()
            for expense in expenses:
                print(expense)
        elif view_choice == 2:
            month = input("Enter the month (MM): ")
            year = input("Enter the year (YYYY): ")
            cur.execute("""SELECT catagory, SUM(price) FROM expenses 
                        WHERE strftime('%m', Date) = ? AND strftime('%Y', DATE) = ?
                        GROUP BY catagory""", (month, year))
            expenses = cur.fetchall()
            for expense in expenses:
                print(f"Catagory: {expense[0]}, Total: {expense[1]}")
        else:
            exit()
    else:
        exit()

    repeat = input("Would you like to do something else (y/n)?\n")
    if repeat.lower() != "y":
        break

conn.close()
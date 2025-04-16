# Touch-N-Go Member Manager
# Adrian Fanjoy
# Test cases

import DB_Manage

# Boolean to run menu
running = True

# Menu
while running:
    print("1. Create database")
    print("2. Delete database")
    print("3. Exit")
    choice = input("Choose from the options above:")

    # Switch case
    if choice == "1":
        print(DB_Manage.create_database())
    elif choice == "2":
        print(DB_Manage.delete_database("memberdb"))
    elif choice == "3":
        running = False

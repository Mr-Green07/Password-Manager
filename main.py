
import getpass
from password_manager import PasswordManager

def print_items(items):
    if items:
        for i, item in enumerate(items):
            print(f"{i + 1}. {item}")
    else:
        print("No items found.")

def view_item_details(password_manager, item_type):
    items = password_manager.list_items()
    print_items(items)
    index = int(input("Enter the index of the item to view details: ")) - 1
    password_manager.view_item_details(item_type, index)

def main():
    print("Welcome to the Password Manager!")

    while True:
        print("\nMenu:")
        print("1. Login")
        print("2. Signup")
        print("3. Exit")

        choice = input("Enter your choice (1-3): ")

        if choice == '1':
            account_name = input("Enter account name: ")
            master_password = getpass.getpass("Enter your master password: ")
            password_manager = PasswordManager(master_password)
            if password_manager.login(account_name):
                print(f"Logged in as '{account_name}'.")
                break
            else:
                print("Login failed. Account not found.")

        elif choice == '2':
            account_name = input("Enter account name: ")
            master_password = getpass.getpass("Create your master password: ")
            password_manager = PasswordManager(master_password)
            if password_manager.signup(account_name):
                print(f"Account '{account_name}' created successfully.")
                break
            else:
                print("Signup failed. Account already exists.")

        elif choice == '3':
            print("Exiting Password Manager. Goodbye!")
            password_manager._save_data()  # Save data before exiting
            exit()

        else:
            print("Invalid choice. Please enter a valid option (1-3).")

    while True:
        print("\nPassword Manager Menu:")
        print("1. Add Login")
        print("2. Add Note")
        print("3. List Items")
        print("4. View Item Details")
        print("5. Edit Item")
        print("6. Delete Item")
        print("7. Logout")
        print("8. Exit")

        choice = input("Enter your choice (1-8): ")

        if choice == '1':
            password_manager.add_login()

        elif choice == '2':
            password_manager.add_note()

        elif choice == '3':
            print("Enter item type: ")
            print("1. Logins")
            print("2. Notes")
            item_type = int(input())
            items = password_manager.list_items(item_type)

        elif choice == '4':
            item_type = input("Enter item type (logins, notes): ")
            view_item_details(password_manager, item_type)

        elif choice == '5':
            item_type = input("Enter item type (logins, notes): ")
            items = password_manager.list_items()
            print_items(items)
            index = int(input("Enter the index of the item to edit: ")) - 1
            new_data = input("Enter new data: ")
            if password_manager.edit_item(item_type, index, new_data):
                print("Item edited successfully.")
            else:
                print("Error: Unable to edit item.")

        elif choice == '6':
            item_type = input("Enter item type (logins, notes): ")
            items = password_manager.list_items(item_type)
            print_items(items)
            index = int(input("Enter the index of the item to delete: ")) - 1
            if password_manager.delete_item(item_type, index):
                print("Item deleted successfully.")
            else:
                print("Error: Unable to delete item.")

        elif choice == '7':
            print("Logging out.")
            password_manager._save_data()  # Save data before logging out
            break

        elif choice == '8':
            password_manager._save_data()  # Save data before exiting
            print("Exiting Password Manager. Goodbye!")
            exit()

        else:
            print("Invalid choice. Please enter a valid option (1-8).")

if __name__ == "__main__":
    main()

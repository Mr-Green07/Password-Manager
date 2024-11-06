
import getpass
from password_manager import PasswordManager
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QLineEdit, QInputDialog, QMessageBox
import sys

class PasswordManagerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Password Manager')
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.label = QLabel('Welcome to the Password Manager!', self)
        self.layout.addWidget(self.label)

        self.login_button = QPushButton('Login', self)
        self.login_button.clicked.connect(self.login)
        self.layout.addWidget(self.login_button)

        self.signup_button = QPushButton('Signup', self)
        self.signup_button.clicked.connect(self.signup)
        self.layout.addWidget(self.signup_button)

        self.exit_button = QPushButton('Exit', self)
        self.exit_button.clicked.connect(self.exit_app)
        self.layout.addWidget(self.exit_button)

    def login(self):
        account_name, ok = QInputDialog.getText(self, 'Login', 'Enter account name:')
        if ok:
            master_password, ok = QInputDialog.getText(self, 'Login', 'Enter your master password:', QLineEdit.Password)
            if ok:
                password_manager = PasswordManager(master_password)
                if password_manager.login(account_name):
                    QMessageBox.information(self, 'Login', f"Logged in as '{account_name}'.")
                    self.password_manager = password_manager
                    self.show_password_manager_menu()
                else:
                    QMessageBox.warning(self, 'Login', 'Login failed. Account not found.')

    def signup(self):
        account_name, ok = QInputDialog.getText(self, 'Signup', 'Enter account name:')
        if ok:
            master_password, ok = QInputDialog.getText(self, 'Signup', 'Create your master password:', QLineEdit.Password)
            if ok:
                password_manager = PasswordManager(master_password)
                if password_manager.signup(account_name):
                    QMessageBox.information(self, 'Signup', f"Account '{account_name}' created successfully.")
                    self.password_manager = password_manager
                    self.show_password_manager_menu()
                else:
                    QMessageBox.warning(self, 'Signup', 'Signup failed. Account already exists.')

    def exit_app(self):
        if hasattr(self, 'password_manager'):
            self.password_manager._save_data()  # Save data before exiting
        sys.exit()

    def show_password_manager_menu(self):
        self.label.setText('Password Manager Menu:')
        self.login_button.hide()
        self.signup_button.hide()
        self.exit_button.hide()

        self.add_login_button = QPushButton('Add Login', self)
        self.add_login_button.clicked.connect(self.add_login)
        self.layout.addWidget(self.add_login_button)

        self.add_note_button = QPushButton('Add Note', self)
        self.add_note_button.clicked.connect(self.add_note)
        self.layout.addWidget(self.add_note_button)

        self.list_items_button = QPushButton('List Items', self)
        self.list_items_button.clicked.connect(self.list_items)
        self.layout.addWidget(self.list_items_button)

        self.view_item_details_button = QPushButton('View Item Details', self)
        self.view_item_details_button.clicked.connect(self.view_item_details)
        self.layout.addWidget(self.view_item_details_button)

        self.edit_item_button = QPushButton('Edit Item', self)
        self.edit_item_button.clicked.connect(self.edit_item)
        self.layout.addWidget(self.edit_item_button)

        self.delete_item_button = QPushButton('Delete Item', self)
        self.delete_item_button.clicked.connect(self.delete_item)
        self.layout.addWidget(self.delete_item_button)

        self.logout_button = QPushButton('Logout', self)
        self.logout_button.clicked.connect(self.logout)
        self.layout.addWidget(self.logout_button)

        self.exit_button = QPushButton('Exit', self)
        self.exit_button.clicked.connect(self.exit_app)
        self.layout.addWidget(self.exit_button)

    def add_login(self):
        self.password_manager.add_login()

    def add_note(self):
        self.password_manager.add_note()

    def list_items(self):
        item_type, ok = QInputDialog.getInt(self, 'List Items', 'Enter item type (1 for Logins, 2 for Notes):')
        if ok:
            items = self.password_manager.list_items(item_type)
            self.print_items(items)

    def view_item_details(self):
        item_type, ok = QInputDialog.getText(self, 'View Item Details', 'Enter item type (logins, notes):')
        if ok:
            items = self.password_manager.list_items()
            self.print_items(items)
            index, ok = QInputDialog.getInt(self, 'View Item Details', 'Enter the index of the item to view details:') - 1
            if ok:
                self.password_manager.view_item_details(item_type, index)

    def edit_item(self):
        item_type, ok = QInputDialog.getText(self, 'Edit Item', 'Enter item type (logins, notes):')
        if ok:
            items = self.password_manager.list_items()
            self.print_items(items)
            index, ok = QInputDialog.getInt(self, 'Edit Item', 'Enter the index of the item to edit:') - 1
            if ok:
                new_data, ok = QInputDialog.getText(self, 'Edit Item', 'Enter new data:')
                if ok:
                    if self.password_manager.edit_item(item_type, index, new_data):
                        QMessageBox.information(self, 'Edit Item', 'Item edited successfully.')
                    else:
                        QMessageBox.warning(self, 'Edit Item', 'Error: Unable to edit item.')

    def delete_item(self):
        item_type, ok = QInputDialog.getText(self, 'Delete Item', 'Enter item type (logins, notes):')
        if ok:
            items = self.password_manager.list_items(item_type)
            self.print_items(items)
            index, ok = QInputDialog.getInt(self, 'Delete Item', 'Enter the index of the item to delete:') - 1
            if ok:
                if self.password_manager.delete_item(item_type, index):
                    QMessageBox.information(self, 'Delete Item', 'Item deleted successfully.')
                else:
                    QMessageBox.warning(self, 'Delete Item', 'Error: Unable to delete item.')

    def logout(self):
        self.password_manager._save_data()  # Save data before logging out
        self.close()

    def print_items(self, items):
        if items:
            items_str = "\n".join([f"{i + 1}. {item}" for i, item in enumerate(items)])
            QMessageBox.information(self, 'Items', items_str)
        else:
            QMessageBox.information(self, 'Items', 'No items found.')

if __name__ == '__main__':
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    ex = PasswordManagerApp()
    ex.show()
    if not app is None:
        sys.exit(app.exec_())



# def print_items(items):
#     if items:
#         for i, item in enumerate(items):
#             print(f"{i + 1}. {item}")
#     else:
#         print("No items found.")

# def view_item_details(password_manager, item_type):
#     items = password_manager.list_items()
#     print_items(items)
#     index = int(input("Enter the index of the item to view details: ")) - 1
#     password_manager.view_item_details(item_type, index)

# def main():
#     print("Welcome to the Password Manager!")

#     while True:
#         print("\nMenu:")
#         print("1. Login")
#         print("2. Signup")
#         print("3. Exit")

#         choice = input("Enter your choice (1-3): ")

#         if choice == '1':
#             account_name = input("Enter account name: ")
#             master_password = getpass.getpass("Enter your master password: ")
#             password_manager = PasswordManager(master_password)
#             if password_manager.login(account_name):
#                 print(f"Logged in as '{account_name}'.")
#                 break
#             else:
#                 print("Login failed. Account not found.")

#         elif choice == '2':
#             account_name = input("Enter account name: ")
#             master_password = getpass.getpass("Create your master password: ")
#             password_manager = PasswordManager(master_password)
#             if password_manager.signup(account_name):
#                 print(f"Account '{account_name}' created successfully.")
#                 break
#             else:
#                 print("Signup failed. Account already exists.")

#         elif choice == '3':
#             print("Exiting Password Manager. Goodbye!")
#             password_manager._save_data()  # Save data before exiting
#             exit()

#         else:
#             print("Invalid choice. Please enter a valid option (1-3).")

#     while True:
#         print("\nPassword Manager Menu:")
#         print("1. Add Login")
#         print("2. Add Note")
#         print("3. List Items")
#         print("4. View Item Details")
#         print("5. Edit Item")
#         print("6. Delete Item")
#         print("7. Logout")
#         print("8. Exit")

#         choice = input("Enter your choice (1-8): ")

#         if choice == '1':
#             password_manager.add_login()

#         elif choice == '2':
#             password_manager.add_note()

#         elif choice == '3':
#             print("Enter item type: ")
#             print("1. Logins")
#             print("2. Notes")
#             item_type = int(input())
#             items = password_manager.list_items(item_type)

#         elif choice == '4':
#             item_type = input("Enter item type (logins, notes): ")
#             view_item_details(password_manager, item_type)

#         elif choice == '5':
#             item_type = input("Enter item type (logins, notes): ")
#             items = password_manager.list_items()
#             print_items(items)
#             index = int(input("Enter the index of the item to edit: ")) - 1
#             new_data = input("Enter new data: ")
#             if password_manager.edit_item(item_type, index, new_data):
#                 print("Item edited successfully.")
#             else:
#                 print("Error: Unable to edit item.")

#         elif choice == '6':
#             item_type = input("Enter item type (logins, notes): ")
#             items = password_manager.list_items(item_type)
#             print_items(items)
#             index = int(input("Enter the index of the item to delete: ")) - 1
#             if password_manager.delete_item(item_type, index):
#                 print("Item deleted successfully.")
#             else:
#                 print("Error: Unable to delete item.")

#         elif choice == '7':
#             print("Logging out.")
#             password_manager._save_data()  # Save data before logging out
#             break

#         elif choice == '8':
#             password_manager._save_data()  # Save data before exiting
#             print("Exiting Password Manager. Goodbye!")
#             exit()

#         else:
#             print("Invalid choice. Please enter a valid option (1-8).")

# if __name__ == "__main__":
#     main()

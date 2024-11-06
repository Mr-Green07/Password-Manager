import getpass
from password_manager import PasswordManager
import wx



class PasswordManagerApp(wx.App):
    def OnInit(self):
        self.frame = MainFrame(None, title="Password Manager")
        self.frame.Show()
        return True

class MainFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(MainFrame, self).__init__(*args, **kw)
        self.panel = wx.Panel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.menu_label = wx.StaticText(self.panel, label="Menu:")
        self.sizer.Add(self.menu_label, 0, wx.ALL, 5)

        self.login_button = wx.Button(self.panel, label="Login")
        self.sizer.Add(self.login_button, 0, wx.ALL, 5)
        self.login_button.Bind(wx.EVT_BUTTON, self.on_login)

        self.signup_button = wx.Button(self.panel, label="Signup")
        self.sizer.Add(self.signup_button, 0, wx.ALL, 5)
        self.signup_button.Bind(wx.EVT_BUTTON, self.on_signup)

        self.exit_button = wx.Button(self.panel, label="Exit")
        self.sizer.Add(self.exit_button, 0, wx.ALL, 5)
        self.exit_button.Bind(wx.EVT_BUTTON, self.on_exit)

        self.panel.SetSizerAndFit(self.sizer)

    def on_login(self, event):
        account_name = wx.GetTextFromUser("Enter account name:", "Login")
        master_password = wx.GetPasswordFromUser("Enter your master password:", "Login")
        password_manager = PasswordManager(master_password)
        if password_manager.login(account_name):
            wx.MessageBox(f"Logged in as '{account_name}'.", "Login Successful")
            self.show_password_manager_menu(password_manager)
        else:
            wx.MessageBox("Login failed. Account not found.", "Login Failed")

    def on_signup(self, event):
        account_name = wx.GetTextFromUser("Enter account name:", "Signup")
        master_password = wx.GetPasswordFromUser("Create your master password:", "Signup")
        password_manager = PasswordManager(master_password)
        if password_manager.signup(account_name):
            wx.MessageBox(f"Account '{account_name}' created successfully.", "Signup Successful")
            self.show_password_manager_menu(password_manager)
        else:
            wx.MessageBox("Signup failed. Account already exists.", "Signup Failed")

    def on_exit(self, event):
        self.Close()

    def show_password_manager_menu(self, password_manager):
        menu_dialog = PasswordManagerMenuDialog(self, password_manager)
        menu_dialog.ShowModal()
        menu_dialog.Destroy()

class PasswordManagerMenuDialog(wx.Dialog):
    def __init__(self, parent, password_manager):
        super(PasswordManagerMenuDialog, self).__init__(parent, title="Password Manager Menu")
        self.password_manager = password_manager
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.add_login_button = wx.Button(self, label="Add Login")
        self.sizer.Add(self.add_login_button, 0, wx.ALL, 5)
        self.add_login_button.Bind(wx.EVT_BUTTON, self.on_add_login)

        self.add_note_button = wx.Button(self, label="Add Note")
        self.sizer.Add(self.add_note_button, 0, wx.ALL, 5)
        self.add_note_button.Bind(wx.EVT_BUTTON, self.on_add_note)

        self.list_items_button = wx.Button(self, label="List Items")
        self.sizer.Add(self.list_items_button, 0, wx.ALL, 5)
        self.list_items_button.Bind(wx.EVT_BUTTON, self.on_list_items)

        self.view_item_details_button = wx.Button(self, label="View Item Details")
        self.sizer.Add(self.view_item_details_button, 0, wx.ALL, 5)
        self.view_item_details_button.Bind(wx.EVT_BUTTON, self.on_view_item_details)

        self.edit_item_button = wx.Button(self, label="Edit Item")
        self.sizer.Add(self.edit_item_button, 0, wx.ALL, 5)
        self.edit_item_button.Bind(wx.EVT_BUTTON, self.on_edit_item)

        self.delete_item_button = wx.Button(self, label="Delete Item")
        self.sizer.Add(self.delete_item_button, 0, wx.ALL, 5)
        self.delete_item_button.Bind(wx.EVT_BUTTON, self.on_delete_item)

        self.logout_button = wx.Button(self, label="Logout")
        self.sizer.Add(self.logout_button, 0, wx.ALL, 5)
        self.logout_button.Bind(wx.EVT_BUTTON, self.on_logout)

        self.exit_button = wx.Button(self, label="Exit")
        self.sizer.Add(self.exit_button, 0, wx.ALL, 5)
        self.exit_button.Bind(wx.EVT_BUTTON, self.on_exit)

        self.SetSizerAndFit(self.sizer)

    def on_add_login(self, event):
        self.password_manager.add_login()

    def on_add_note(self, event):
        self.password_manager.add_note()

    def on_list_items(self, event):
        item_type = wx.GetTextFromUser("Enter item type (logins, notes):", "List Items")
        items = self.password_manager.list_items(item_type)
        print(items)

    def on_view_item_details(self, event):
        item_type = wx.GetTextFromUser("Enter item type (logins, notes):", "View Item Details")
        view_item_details(self.password_manager, item_type)

    def on_edit_item(self, event):
        item_type = wx.GetTextFromUser("Enter item type (logins, notes):", "Edit Item")
        items = self.password_manager.list_items(item_type)
        print_items(items)
        index = int(wx.GetTextFromUser("Enter the index of the item to edit:", "Edit Item")) - 1
        new_data = wx.GetTextFromUser("Enter new data:", "Edit Item")
        if self.password_manager.edit_item(item_type, index, new_data):
            wx.MessageBox("Item edited successfully.", "Edit Item")
        else:
            wx.MessageBox("Error: Unable to edit item.", "Edit Item")

    def on_delete_item(self, event):
        item_type = wx.GetTextFromUser("Enter item type (logins, notes):", "Delete Item")
        items = self.password_manager.list_items(item_type)
        print_items(items)
        index = int(wx.GetTextFromUser("Enter the index of the item to delete:", "Delete Item")) - 1
        if self.password_manager.delete_item(item_type, index):
            wx.MessageBox("Item deleted successfully.", "Delete Item")
        else:
            wx.MessageBox("Error: Unable to delete item.", "Delete Item")

    def on_logout(self, event):
        self.password_manager._save_data()
        self.Close()

    def on_exit(self, event):
        self.password_manager._save_data()
        self.Close()

if __name__ == "__main__":
    app = PasswordManagerApp()
    app.MainLoop()
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

# password_manager.py
import base64
import json
import msvcrt
import os
from encryption import derive_key, encrypt, decrypt
from pymongo import MongoClient
from getpass import getpass

class PasswordManager:
    def __init__(self, master_password, db_url='mongodb+srv://manager:UdsqXsJnWSMw7NPj@cluster0.t0apcqe.mongodb.net/?retryWrites=true&w=majority', db_name='password_manager'):
        self.master_password = master_password
        self.current_account = None
        self.client = MongoClient(db_url)
        self.db = self.client[db_name]
        self.accounts_collection = self.db['accounts']

    def _save_data(self):
        # Save encrypted data to MongoDB
        salt = os.urandom(16)
        key = derive_key(self.master_password, salt)
        ciphertext, tag = encrypt(json.dumps(self.current_account_data), key, salt)

        account_data = {
            'account_name': self.current_account,
            'ciphertext': ciphertext,
            'tag': tag,
            'salt': salt
        }

        self.accounts_collection.replace_one({'account_name': self.current_account}, account_data, upsert=True)

    def _load_data(self):
        # Load and decrypt data from MongoDB
        account_data = self.accounts_collection.find_one({'account_name': self.current_account})

        if account_data:
            ciphertext = account_data['ciphertext']
            tag = account_data['tag']
            salt = account_data['salt']
            key = derive_key(self.master_password, salt)

            decrypted_data = decrypt(ciphertext, key, salt, tag)
            self.current_account_data = json.loads(decrypted_data)
        else:
            self.current_account_data = {}

    def signup(self, account_name):
        if not self.accounts_collection.find_one({'account_name': account_name}):
            self.current_account = account_name
            self.current_account_data = {'logins': [], 'notes': [], 'payments': []}
            self._save_data()
            return True
        else:
            return False

    def login(self, account_name):
        account_data = self.accounts_collection.find_one({'account_name': account_name})

        if account_data:
            self.current_account = account_name
            self._load_data()
            return True
        else:
            return False

    def add_item(self, item_type, data):
        if self.current_account:
            if item_type not in self.current_account_data:
                self.current_account_data[item_type] = []
            self.current_account_data[item_type].append(data)
            self._save_data()
            return True
        else:
            return False

    def list_accounts(self):
        return list(self.accounts.keys())


    def edit_item(self, item_type, index, new_data):
        if self.current_account and item_type in self.accounts[self.current_account]:
            if 0 <= index < len(self.accounts[self.current_account][item_type]):
                self.accounts[self.current_account][item_type][index] = new_data
                self._save_data()
                return True
        return False

    def delete_item(self, item_type, index):
        if self.current_account and item_type in self.accounts[self.current_account]:
            if 0 <= index < len(self.accounts[self.current_account][item_type]):
                del self.accounts[self.current_account][item_type][index]
                self._save_data()
                return True
        return False


    def add_login(self):
        # account_name =input("Enter Account Name: ")
        account_url = input("Enter Account URL (Optional): ")
        user_id = input("Enter User ID: ")
        password = getpass("Enter Password: ")

        login_data = {
            'type': 'login',
            # 'account_name': account_name,
            'account_url': account_url,
            'user_id': user_id,
            'password': password
        }

        self.current_account_data.setdefault('logins', []).append(login_data)
        self._save_data()

    def add_note(self):
        title = input("Enter Note Title: ")
        content = input("Enter Note Content: ")

        note_data = {
            'type': 'note',
            'title': title,
            'content': content
        }

        self.current_account_data.setdefault('notes', []).append(note_data)
        self._save_data()

    def list_items(self, item_type):
            print("Listing Items:")
            if item_type == 1:
                items = self.current_account_data['logins']
                print(f"Login:")

                for i, item in enumerate(items):
                    print(f"{i + 1}.\n\tAccount Name: {item.get('account_name', 'N/A')}")
                    print(f"\tURL: {item.get('account_url', 'N/A')}")
                    print(f"\tPassword: {item.get('password', 'N/A')}")

            elif item_type == 2:
                items = self.current_account_data['notes']

                print(f"Note:")

                for i, item in enumerate(items):
                    print(f"{i + 1}.\n\tTitle: {item.get('title', 'N/A')}")
                    print(f"\tContent: {item.get('content', 'N/A')}")


            if not self.current_account_data:
                print("No items found.")

    def view_item_details(self, item_type, index):
        items = self.current_account_data.get(item_type, [])
        if 0 <= index < len(items):
            item = items[index]
            print("\nItem Details:")
            for key, value in item.items():
                print(f"{key.capitalize()}: {value}")
        else:
            print("Invalid index.")

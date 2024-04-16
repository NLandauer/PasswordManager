# ******************************************************************************
# Author:         Noelle Landauer
# Lab:            Lab 3 (second version), CIS 233Y
# Date:           06.11.22
# Description:  Password manager program that keeps track of accounts inside
#       category folders (lists), stores account and list information
#       MongoDB database
# Changes: Fixed InputValidation to be case-insensitive
# Sources:      Class lecture
#       https://www.mongodb.com/docs/manual/reference/method/db.collection.update/
# ******************************************************************************

from InputValidation import input_value
from AccountList import AccountList
from Account import Account
from TwoFactorAccount import TwoFactor
from datetime import datetime


class PasswordManager:

    # Initializes empty lists for AccountLists (folders) and Accounts
    def __init__(self):
        self.__account_lists = []
        self.__all_accounts = []

    # Inserts seed data into database on startup
    # Reads data into account_lists and all_accounts on startup
    # Loops through menu options until user quits
    # Calls relevant function based on user choice
    def run_app(self):
        PasswordManager.seed_data()
        self.__account_lists = PasswordManager.read_lists()
        self.__all_accounts = PasswordManager.read_accounts()
        choice = 1
        while choice in range(0, 9):
            self.menu_display(self.menu_dict())
            choice = input_value(data_type='int', prompt='Your choice: ', ge=1, le=9,
                                 error_msg='Please enter a number between 1 and 9.')
            if choice == 1:
                self.show_all_account_lists()
            elif choice == 2:
                self.create_account_list()
            elif choice == 3:
                self.delete_account_list()
            elif choice == 4:
                self.show_all_accounts_within_list()
            elif choice == 5:
                self.add_new_account()
            elif choice == 6:
                self.remove_account_from_list()
            elif choice == 7:
                self.update_password()
            elif choice == 8:
                self.merge_account_lists()
            elif choice == 9:
                print("Goodbye!")
                break

    # Displays menu & loops
    def menu_display(self, menu_dict):
        print("\nOptions for Noelle's Password Manager: ")
        for i in menu_dict.values():
            print(i)

    # Menu (dictionary) of options
    def menu_dict(self):
        menu_options = {
            1: "(1) Show all account folders.",
            2: "(2) Create a new account folder.",
            3: "(3) Delete an account folder.",
            4: "(4) Show all accounts in a particular folder.",
            5: "(5) Add a new account to a folder.",
            6: "(6) Remove an account from a folder.",
            7: "(7) Update a password on an account.",
            8: "(8) Merge two folders.",
            9: "(9) Exit program."
        }
        return menu_options

    # returns current account_lists from database
    @staticmethod
    def read_lists():
        return AccountList.read_lists()

    # returns current accounts from database
    @staticmethod
    def read_accounts():
        return Account.read_accounts()

    # instructs Database to insert seed data
    @staticmethod
    def seed_data():
        from Database import Database
        Database.seed_data()

    # Display current AccountLists/folders
    def show_all_account_lists(self):
        print()
        self.__account_lists = PasswordManager.read_lists()
        if len(self.__account_lists) == 0:
            print("You have no account folders.\n")
        else:
            print("Your current account folders are: ")
            for account in self.__account_lists:
                print(account)

    # Create new empty AccountList/folder
    # Appends to master list of AccountLists & updates database
    def create_account_list(self):
        name = input_value(data_type='string', prompt='Folder name: ', error_msg='You must give each folder a name.')
        security_scale = input_value(data_type='int', prompt='Security rank of this folder (1-10): ',
                                     error_msg='Folders require a security ranking between 1 and 10.',
                                     ge=1, le=10)
        new_list = AccountList(name, security_scale, account_list=[])
        self.__account_lists.append(new_list)
        AccountList.update_list_in_database(new_list)

    # Choose an AccountList from master list of AccountLists (not a menu option, used in functions below)
    def choose_account_list(self, **kwargs):
        choice = input_value(data_type='list', error_msg='That folder is not on the list.',
                             choices=self.__account_lists, **kwargs)
        # choice = test_database.select_object(error_msg='That folder is not on the list.',
        #                      choices=self.__account_lists, **kwargs)
        return choice

    # Delete an AccountList/folder from master list of AccountLists & database
    def delete_account_list(self):
        deleted_list = self.choose_account_list(prompt='Input the folder to be deleted: ')
        self.__account_lists.remove(deleted_list)
        AccountList.delete_list_from_database(deleted_list)

    # Display accounts within a given AccountList/folder
    def show_all_accounts_within_list(self):
        chosen_list = self.choose_account_list(prompt='Which folder do you want to see all the accounts? ')
        print("\nThe folder", chosen_list, "contains: ")
        if chosen_list == 'All Accounts':
            AccountList.update_all_account_list()
        accounts = AccountList.read_accounts_from_list(chosen_list.get_name())
        if len(accounts) == 0:
            print("You have no accounts in that folder.")
        else:
            for account in accounts:
                print(account)

    # Adds a new Account
    # Option for Two-Factor accounts
    # Collects all data for new Account object
    # Updates database with new account
    # Calls to place Account in a folder/account_list
    def add_new_account(self):
        site_name = input_value(data_type='string', prompt='What is the website name? ')
        login_url = input_value(data_type='string', prompt='What is the login url? ')
        username = input_value(data_type='string', prompt='What is your username for this site? ')
        password = input_value(data_type='string', prompt='What is your password for this site? ')
        creation_date = datetime.today()
        two_factor = input_value(data_type='y_or_n', prompt="Does this account require two-factor authentication? ")
        if two_factor is True:
            factor_type = input_value(data_type='list',
                                      prompt='What type of two-factor account? ''Choose from: ',
                                      choices=['app', 'pin', 'question'],
                                      dictionary={'a': 'app', 'A': 'app', 'app': 'app', 'App': 'app',
                                                  'p': 'pin', 'P': 'pin', 'pin': 'pin', 'Pin': 'pin',
                                                  'ques': 'question', 'question': 'question',
                                                  'Question': 'question', 'q': 'question', 'Q': 'question'})
            authentication_info = input_value(data_type='string', prompt='What authentication information is needed? '
                                                                         '(ex. pin, answer to secret question): ')
            new_account = TwoFactor(site_name, login_url, username, password, creation_date, factor_type,
                                    authentication_info)
        else:
            new_account = Account(site_name, login_url, username, password, creation_date)
        Account.update_database(new_account)
        self.__all_accounts.append(new_account)
        AccountList.update_all_account_list()
        PasswordManager.add_account_to_list(self, new_account)

    # Adds Account to List & updates database
    # not currently a menu option, but could be added to menu independently of add_new_account()
    def add_account_to_list(self, account):
        account_list = self.choose_account_list(prompt='Which folder do you want this account to go into?')
        account_list.add_account(account.get_name())
        AccountList.update_list_in_database(account_list)

    # Removes an Account from a given AccountList & updates database
    def remove_account_from_list(self):
        selected_account_list = self.choose_account_list(prompt='Which folder is the account in? ')
        deleted_account = input_value(data_type='list', prompt='Which account do you want to delete?',
                                      choices=selected_account_list.get_account_list())
        selected_account_list.remove(deleted_account)
        AccountList.update_list_in_database(selected_account_list)

    # Selects Account and replaces password
    # updates database
    def update_password(self):
        accounts = self.__all_accounts
        account = input_value(data_type='list', prompt='Which account is updating its password? ',
                              choices=accounts)
        new_password = input_value(data_type='string', prompt='What is your new password? ')
        Account.update_password(account, new_password)

    # adds two AccountLists together (with contents) & updates database with new account_list
    # does not delete the old account_lists like previous version
    def merge_account_lists(self):
        account1 = self.choose_account_list(prompt='Folder 1 to merge: ')
        account2 = self.choose_account_list(prompt='Folder 2 to merge: ')
        merged_list = account1 + account2
        self.__account_lists.append(merged_list)
        AccountList.update_list_in_database(merged_list)


if __name__ == "__main__":
    passwordManager1 = PasswordManager()
    passwordManager1.run_app()

# class holds Account objects in AccountList objects
# Data needed: name of AccountList and security ranking 1-10
from Database import Database


class AccountList:

    def __init__(self, name, security_scale, account_list):
        self.__name = name
        self.__account_list = account_list
        self.__security_scale = security_scale

    def __iter__(self):
        return iter(self.__name)

    def add_account(self, account):
        self.__account_list.append(account)

    def remove(self, account):
        self.__account_list.remove(account)

    def __str__(self):
        return F"{self.__name}"

    def __repr__(self):
        return F"{self.__name}"

    # combines 2 AccountList objects
    # resulting AccountList includes average security scale & accounts of both
    def __add__(self, other):
        new_security_scale = (self.__security_scale + other.__security_scale) / 2
        new_account_list = (self.__account_list + other.__account_list)
        combo_list = AccountList(self.get_name() + '/' + other.get_name(), new_security_scale, new_account_list)
        return combo_list

    def get_name(self):
        return self.__name

    def get_account_list(self):
        return self.__account_list

    def get_security(self):
        return self.__security_scale

    # turns AccountList object into dictionary, with _id = name
    def to_dict_with_id(self):
        return {
            "_id": self.get_name(),
            "name": self.get_name(),
            "accounts": self.get_account_list(),
            "security_scale": self.get_security()
        }

    # returns current account_lists from database
    @staticmethod
    def read_lists():
        return Database.read_lists()

    # returns current account on a given list form database
    @staticmethod
    def read_accounts_from_list(account_list):
        return Database.read_accounts_from_list(account_list)

    # deletes list from database (does not affect accounts)
    @staticmethod
    def delete_list_from_database(deleted_list):
        Database.delete_list_from_database(deleted_list)

    # passes along changed account_list to database for updating
    @staticmethod
    def update_list_in_database(account_list):
        Database.update_list_in_database(account_list)

    # tells database to update All Account list (needed when accounts added or removed)
    @staticmethod
    def update_all_account_list():
        Database.update_all_account_list()

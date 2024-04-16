# Class to hold data for each Account object
# Data needed: site name, login url, username, password, date last changed password

from datetime import datetime
from Database import Database


class Account:

    def __init__(self, site_name, login_url, username, password, date_last_changed):
        self.__site_name = site_name
        self.__login_url = login_url
        self.__username = username
        self.__password = password
        self.__date_last_changed = date_last_changed

    def __str__(self):
        return self.__site_name

    def __repr__(self):
        return 'Site: ' + self.__site_name + ', Username: ' + self.__username

    def change_password(self, new_password):
        self.__password = new_password
        self.__date_last_changed = datetime.today()

    def get_name(self):
        return self.__site_name

    def get_url(self):
        return self.__login_url

    def get_username(self):
        return self.__username

    def get_password(self):
        return self.__password

    def get_date_changed(self):
        return self.__date_last_changed

    # turns Account object into dictionary, with "_id" = name
    # default "factor_type" = "one_factor"
    def to_dict_with_id(self):
        return {
            "_id": self.get_name(),
            "factor_type": "one_factor",
            "site_name": self.get_name(),
            "login_url": self.get_url(),
            "user_name": self.get_username(),
            "password:": self.get_password(),
            "date_last_changed": self.get_date_changed()
        }

    # passes along account to be updated/inserted into database
    @staticmethod
    def update_database(account):
        Database.update_account_in_database(account)

    # changes password & data last changed on Account object
    # passes along account to be updated in database
    @staticmethod
    def update_password(account, new_password):
        account.__password = new_password
        account.__date_last_changed = datetime.today()
        Database.update_account_in_database(account)

    # reads all currents accounts in database
    @staticmethod
    def read_accounts():
        return Database.read_accounts()

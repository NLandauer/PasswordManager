from pymongo import *
from datetime import datetime


class Database:
    __client = None
    __db = None
    __accounts = None
    __account_lists = None

    # log on to MongoDB client
    @classmethod
    def __connect(cls):
        if cls.__client is None:
            cls.__client = MongoClient(
                "mongodb+srv://CIUser:CIS233Y@sandbox.ukevd.mongodb.net/?retryWrites=true&w=majority")
            cls.__db = cls.__client.PasswordManager
            cls.__accounts = cls.__db.Accounts
            cls.__account_lists = cls.__db.AccountLists

    # drops old collections and adds in 2 collections: Accounts & AccountLists
    # adds data to each collection
    # "_id" = site_name
    @classmethod
    def seed_data(cls):
        cls.__connect()
        cls.__db.Accounts.drop()
        cls.__db.AccountLists.drop()
        citi = {
            "_id": "citi",
            "factor_type": "one_factor",
            "site_name": "citi",
            "login_url": "www.citibank.com/login",
            "user_name": "nl@gmail.com",
            "password": "p@ssword!",
            "date_last_changed": datetime.today()}
        cap1 = {
            "_id": "cap1",
            "factor_type": "two_factor",
            "site_name": "cap1",
            "login_url": "capitalone.com/login",
            "user_name": "NMLandauer",
            "password": "p@@!!w)rd",
            "date_last_changed": datetime.today(),
            "second_factor_needed": "pin",
            "factor_info": "1234"
        }
        fidelity = {
            "_id": "fidelity",
            "factor_type": "two_factor",
            "site_name": "fidelity",
            "login_url": "fidelity.com",
            "user_name": "nl@gmail.com",
            "password": "!passw0rd",
            "date_last_changed": datetime.today(),
            "second_factor_needed": "question",
            "factor_info": "MamaKitty"
        }
        reddit = {
            "_id": "reddit",
            "factor_type": "one_factor",
            "site_name": "reddit",
            "login_url": "www.reddit.com",
            "user_name": "iamaficus",
            "password": "redditpassword",
            "date_last_changed": datetime.today()}
        facebook = {
            "_id": "facebook",
            "factor_type": "one_factor",
            "site_name": "facebook",
            "login_url": "facebook.com",
            "user_name": "nl@gmail.com",
            "password": "faceb00ksucks",
            "date_last_changed": datetime.today()}
        twitter = {
            "_id": "twitter",
            "factor_type": "one_factor",
            "site_name": "twitter",
            "login_url": "twitter.com",
            "user_name": "ficus4life",
            "password": "MuskCantOwnMe1",
            "date_last_changed": datetime.today()}
        amazon = {
            "_id": "amazon",
            "factor_type": "two_factor",
            "site_name": "amazon",
            "login_url": "amazon.com",
            "user_name": "nl@gmail.com",
            "password": "Bez05B00",
            "date_last_changed": datetime.today(),
            "second_factor_needed": "app",
            "factor_info": "__amaz"
        }
        ebay = {
            "_id": "ebay",
            "factor_type": "two_factor",
            "site_name": "ebay",
            "login_url": "login.ebay.com",
            "user_name": "nl@gmail.com",
            "password": "#bl@hstuff!",
            "date_last_changed": datetime.today(),
            "second_factor_needed": "question",
            "factor_info": "FordPinto"
        }
        ogw = {
            "_id": "ogw",
            "factor_type": "one_factor",
            "site_name": "ogw",
            "login_url": "www.onegreenworld.com",
            "user_name": "NLandauer",
            "password": "2many@pp1es",
            "date_last_changed": datetime.today()
        }
        adaptive = {
            "_id": "adaptive",
            "factor_type": "one_factor",
            "site_name": "adaptive",
            "login_url": "adaptiveseeds.com",
            "user_name": "nl@gmail.com",
            "password": "2manyt0mato@s",
            "date_last_changed": datetime.today()
        }
        cls.__accounts = cls.__db.Accounts
        cls.__account_lists = cls.__db.AccountLists
        seed_accounts = [citi, cap1, fidelity, reddit, facebook, twitter, amazon, ebay, ogw, adaptive]
        result = cls.__accounts.insert_many(seed_accounts)
        all_accounts = list(cls.__accounts.find())
        cls.__account_lists.insert_one({
            "_id": "All Accounts",
            "name": "All Accounts",
            "accounts": [account["_id"] for account in all_accounts],
            "security_scale": 10
        })
        cls.__account_lists.insert_one({
            "_id": "Banks",
            "name": "Banks",
            "accounts": [account["_id"] for account in [citi, cap1, fidelity]],
            "security_scale": 10
        })
        cls.__account_lists.insert_one({
            "_id": "Social Media",
            "name": "Social Media",
            "accounts": [account["_id"] for account in [reddit, facebook, twitter]],
            "security_scale": 5
        })
        cls.__account_lists.insert_one({
            "_id": "Shopping",
            "name": "Shopping",
            "accounts": [account["_id"] for account in [amazon, ebay]],
            "security_scale": 9
        })
        cls.__account_lists.insert_one({
            "_id": "Nurseries",
            "name": "Nurseries",
            "accounts": [account["_id"] for account in [ogw, adaptive]],
            "security_scale": 4
        })

    # displays current state of account and account_list collections
    # for testing purposes
    @classmethod
    def display_current_data(cls):
        cls.__connect()
        accounts = cls.__accounts.find()
        print("Accounts: ")
        for account in accounts:
            print(account)
        print("Lists: ")
        account_lists = cls.__account_lists.find()
        for acc_list in account_lists:
            print(acc_list)

    # reads all accounts from database
    # recreates & returns Account objects from database dictionaries
    @classmethod
    def read_accounts(cls):
        from Account import Account
        from TwoFactorAccount import TwoFactor
        cls.__connect()
        accounts = cls.__accounts.find()
        account_objects = []
        for account_dict in accounts:
            if account_dict['factor_type'] == 'one_factor':
                account_objects.append(Account(
                    account_dict['site_name'],
                    account_dict['login_url'],
                    account_dict['user_name'],
                    account_dict['password'],
                    account_dict['date_last_changed']
                ))
            elif account_dict['factor_type'] == 'two_factor':
                account_objects.append(TwoFactor(
                    account_dict['site_name'],
                    account_dict['login_url'],
                    account_dict['user_name'],
                    account_dict['password'],
                    account_dict['date_last_changed'],
                    account_dict['second_factor_needed'],
                    account_dict['factor_info']
                ))
            else:
                print("Unknown factor type for this account: ", account_dict)
        return account_objects

    # returns current accounts from a given list
    @classmethod
    def read_accounts_from_list(cls, account_list):
        cls.__connect()
        accounts = cls.__account_lists.find({"name": {"$eq": account_list}}, {"accounts": 1})
        return accounts[0]["accounts"]

    # reads all account_lists from database
    # recreates & returns AccountList objects from database dictionaries
    @classmethod
    def read_lists(cls):
        from AccountList import AccountList
        cls.__connect()
        account_lists = cls.__account_lists.find()
        all_lists = []
        for list_dict in account_lists:
            account_list = AccountList(
                list_dict['name'],
                list_dict['security_scale'],
                list_dict['accounts']
            )
            all_lists.append(account_list)
        return all_lists

    # updates one account or inserts new account
    @classmethod
    def update_account_in_database(cls, account):
        cls.__connect()
        account_dict = account.to_dict_with_id()
        cls.__accounts.update_one({"_id": account.get_name()}, {"$set": account_dict}, upsert=True)
        Database.update_all_account_list()

    # updates All Accounts list, needed when adding/deleting accounts
    @classmethod
    def update_all_account_list(cls):
        cls.__connect()
        all_accounts = list(cls.__accounts.find())
        cls.__account_lists.update_one({"_id": "All Accounts"},
                                       {"$set": {"accounts": [account["_id"] for account in all_accounts]}})

    # updates or inserts one account_list
    @classmethod
    def update_list_in_database(cls, account_list):
        cls.__connect()
        updated_dict = account_list.to_dict_with_id()
        cls.__account_lists.update_one({"_id": account_list.get_name()}, {"$set": updated_dict}, upsert=True)

    # deletes one list form database
    @classmethod
    def delete_list_from_database(cls, deleted_list):
        cls.__connect()
        cls.__account_lists.delete_one({"_id": deleted_list.get_name()})

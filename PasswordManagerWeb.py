# ******************************************************************************
# Author:         Noelle Landauer
# Lab:            Lab 4, CIS 233Y
# Date:           06.15.22
# Description:  Web UI with Flask & Jinja2 templates added to password management program
# Sources:      Class lecture
# ******************************************************************************

from flask import Flask, render_template, request, redirect, url_for
from AccountList import AccountList
from Account import Account


class PasswordManagerWeb:
    __app = Flask(__name__, template_folder='templates')
    __account_lists = None
    __all_accounts = None

    def __init__(self):
        PasswordManagerWeb.__app.secret_key = "blahblahblah@#^345"

    def run(self):
        PasswordManagerWeb.seed_data()
        PasswordManagerWeb.__account_lists = PasswordManagerWeb.read_lists()
        PasswordManagerWeb.__all_accounts = PasswordManagerWeb.read_accounts()
        PasswordManagerWeb.__app.run(port=8000)

    @staticmethod
    def seed_data():
        from Database import Database
        Database.seed_data()

    # returns current account_lists from database
    @staticmethod
    def read_lists():
        return AccountList.read_lists()

    # returns current accounts from database
    @staticmethod
    def read_accounts():
        return Account.read_accounts()

    @staticmethod
    def find_account_list(account_list_name):
        for account_list in PasswordManagerWeb.__account_lists:
            if account_list_name == account_list.get_name():
                return account_list
        return None

    @staticmethod
    def find_account(account_name):
        for account in PasswordManagerWeb.__all_accounts:
            if account_name == account.get_name():
                return account
        return None

    @staticmethod
    @__app.route("/")
    def redirect_to_main():
        return redirect(url_for("main_menu"))

    @staticmethod
    @__app.route("/main_menu")
    def main_menu():
        return render_template("main_menu.html")

    @staticmethod
    @__app.route("/display_account_lists")
    def display_account_lists():
        return render_template("display_account_lists.html", account_lists=PasswordManagerWeb.__account_lists)

    @staticmethod
    @__app.route("/select_account_list_to_print")
    def select_account_list_to_print():
        return render_template("select_account_list_to_print.html", account_lists=PasswordManagerWeb.__account_lists)

    @staticmethod
    @__app.route("/display_accounts_in_folder")
    def display_accounts_in_folder():
        account_list_name = request.args["account_list_name"]
        accounts = AccountList.read_accounts_from_list(account_list_name)
        for account_list in PasswordManagerWeb.__account_lists:
            if account_list.get_name() == account_list_name:
                print(account for account in account_list)
                return render_template("display_accounts_in_folder.html", account_list=account_list, accounts=accounts)
        return "<h1>Could not find account folder named%" + account_list_name + "</h1>"

    @staticmethod
    @__app.route("/input_account_list_to_add")
    def input_account_list_to_add():
        return render_template("input_account_list_to_add.html", account_lists=PasswordManagerWeb.__account_lists)

    @staticmethod
    @__app.route("/add_account_list")
    def add_account_list():
        name = request.args["account_list_name"]
        security_scale = int(request.args["security_scale"])
        new_list = AccountList(name, security_scale, account_list=[])
        PasswordManagerWeb.__account_lists.append(new_list)
        AccountList.update_list_in_database(new_list)
        return render_template("new_account_list_successful.html", account_list=name)

    @staticmethod
    @__app.route("/select_account_list_to_delete")
    def select_account_list_to_delete():
        return render_template("select_account_list_to_delete.html", account_lists=PasswordManagerWeb.__account_lists)

    @staticmethod
    @__app.route("/delete_account_list")
    def delete_account_list():
        deleted_list = request.args["account_list_name"]
        account_list = PasswordManagerWeb.find_account_list(deleted_list)
        if account_list is not None:
            AccountList.delete_list_from_database(account_list)
            PasswordManagerWeb.__account_lists.remove(account_list)
            return render_template("delete_account_list_successful.html", account_list=deleted_list)
        else:
            return "<h1> Error: No folder " + deleted_list + "found.</h1>"

    @staticmethod
    @__app.route("/select_account_lists_to_merge")
    def select_account_lists_to_merge():
        return render_template("select_account_lists_to_merge.html", account_lists=PasswordManagerWeb.__account_lists)

    @staticmethod
    @__app.route("/merge_account_lists")
    def merge_account_lists():
        account_list_1 = PasswordManagerWeb.find_account_list(request.args["account_list_name_1"])
        account_list_2 = PasswordManagerWeb.find_account_list(request.args["account_list_name_2"])
        merged_list = account_list_1 + account_list_2
        PasswordManagerWeb.__account_lists.append(merged_list)
        AccountList.update_list_in_database(merged_list)
        return render_template("lists_merged_successfully.html", merged_list=merged_list)

    @staticmethod
    @__app.route("/select_account_list_to_remove_account")
    def select_account_list_to_remove_account():
        return render_template("select_account_list_to_remove_account.html",
                               account_lists=PasswordManagerWeb.__account_lists
                               )

    @staticmethod
    @__app.route("/select_account_to_remove")
    def select_account_to_remove():
        account_list_name = request.args["account_list_name"]
        account_list = PasswordManagerWeb.find_account_list(account_list_name)
        accounts = AccountList.read_accounts_from_list(account_list_name)
        return render_template("select_account_to_remove.html", account_list=account_list, accounts=accounts)

    @staticmethod
    @__app.route("/remove_account_from_list")
    def remove_account_from_list():
        account_name = request.args["account_name"]
        account_list_name = request.args["account_list_name"]
        account_list = PasswordManagerWeb.find_account_list(account_list_name)
        account = PasswordManagerWeb.find_account(account_name)
        account_list.remove(account_name)
        AccountList.update_list_in_database(account_list)
        return render_template("account_removal_successful.html",
                               account=account,
                               account_list=account_list
                               )

    @staticmethod
    @__app.route("/get_site_and_new_password")
    def get_site_and_new_password():
        return render_template("get_site_and_new_password.html", accounts=PasswordManagerWeb.__all_accounts)

    @staticmethod
    @__app.route("/update_password", methods=["POST"])
    def update_password():
        site_name = request.form["site_name"]
        new_password = request.form["new_password"]
        account = PasswordManagerWeb.find_account(site_name)
        if account is not None:
            Account.update_password(account, new_password)
            return render_template("update_successful.html", account=site_name)
        else:
            return "<h1>Error: No account named " + site_name + "found.</h1>"


if __name__ == "__main__":
    app = PasswordManagerWeb()
    app.run()

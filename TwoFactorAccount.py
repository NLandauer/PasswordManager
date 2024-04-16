# Subclass of Account for two-factor-accounts
# Additional data for each object (in addition to Account): type of two-factor account and information needed to fill in

from Account import Account


class TwoFactor(Account):
    def __init__(self, site_name, login_url, username, password, date_last_changed, second_factor_needed,
                 factor_info=None):
        Account.__init__(self, site_name, login_url, username, password, date_last_changed)
        self.__second_factor_needed = second_factor_needed
        self.__factor_info = factor_info

    def get_second_factor(self):
        return self.__second_factor_needed

    def get_factor_info(self):
        return self.__factor_info

    # turns 2-factor Account object into dictionary for database insertion
    def to_dict_with_id(self):
        return {
            "_id": self.get_name(),
            "factor_type": "two_factor",
            "site_name": self.get_name(),
            "login_url": self.get_url(),
            "user_name": self.get_username(),
            "password:": self.get_password(),
            "date_last_changed": self.get_date_changed(),
            "second_factor_needed": self.get_second_factor(),
            "factor_info": self.get_factor_info()
        }

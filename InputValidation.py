# Library of input validation functions, with optional prompts and error messages
# All input funneled through input_value()

# Integer input
# Optional kwargs ge (greater than or equal to), gt (greater than), le (Less than or equal to), lt (less than)
def input_int(prompt='Enter a whole number: ', error_msg='You must enter a whole number.',
              ge=None, gt=None, le=None, lt=None):
    while True:
        try:
            info = int(input(prompt))
            if ge is not None and info < ge:
                print(error_msg)
                continue
            if gt is not None and info <= gt:
                print(error_msg)
                continue
            if le is not None and info > le:
                print(error_msg)
                continue
            if lt is not None and info >= lt:
                print(error_msg)
                continue
            return info
        except ValueError:
            print(error_msg)
            continue


# Float input
# Optional kwargs ge (greater than or equal to), gt (greater than), le (Less than or equal to), lt (less than)
def input_float(prompt='Enter a number: ', error_msg='You must enter a number.',
                ge=None, gt=None, le=None, lt=None):
    while True:
        try:
            info = float(input(prompt))
            if ge is not None and info < ge:
                print(error_msg)
                continue
            if gt is not None and info <= gt:
                print(error_msg)
                continue
            if le is not None and info > le:
                print(error_msg)
                continue
            if lt is not None and info >= lt:
                print(error_msg)
                continue
            return info
        except ValueError:
            print(error_msg)
            continue


# String input
# Optional validity function, defaults to input=None is invalid
def input_string(prompt='Value: ', valid=None, error_msg="Please enter a value."):
    while valid is None:
        info = input(prompt)
        if info:
            return info
        else:
            print(error_msg)
            continue
    while valid is not None:
        info = input(prompt)
        if valid(info) is False:
            print(error_msg)
            continue
        elif valid(info) is True:
            return info


# Yes or no input
#  Returns yes = True, no = False
def input_yes_no(prompt='Yes or no? ', error_msg='Please enter y for yes or n for no.'):
    while True:
        info = input(prompt).lower()
        if info == 'y' or info == 'yes':
            return True
        elif info == 'n' or info == 'no':
            return False
        else:
            print(error_msg)
            continue


# User selects choice from list of objects (data_type 'list)
def select_from_list(choices=None, dictionary=None, prompt='Choose from the following options: ',
                     error_msg='That entry is not on the list.'):
    print(prompt)
    for obj in choices:
        print(obj)
    while True:
        try:
            info = input("Your choice is: ").lower()
            for obj in choices:
                if dictionary is None and info == str(obj).lower():
                    return obj
                elif dictionary is not None and info in dictionary.keys():
                    return dictionary[info]
            else:
                print(error_msg)
                continue
        except KeyError:
            print(error_msg)
            continue


# Sorts input requests by data_type
# Passes on other kwargs
def input_value(data_type=None, **kwargs):
    info = None
    if data_type == 'int':
        info = input_int(**kwargs)
    elif data_type == 'float':
        info = input_float(**kwargs)
    elif data_type == 'string':
        info = input_string(**kwargs)
    elif data_type == 'y_or_n':
        info = input_yes_no(**kwargs)
    elif data_type == 'list':
        info = select_from_list(**kwargs)
    else:
        print("Permitted data types are int, float, string, y_or_n, list")
    return info

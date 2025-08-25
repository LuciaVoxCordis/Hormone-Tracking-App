from global_vars import *

from csv_class import CSV

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def initialize_data_folder():
    if path.exists(wdir):
        print ("Data folder found")
    else:
        print ("Data folder not found, Creating...")
        mkdir(wdir)
        
def add_result(date, e, t):
    date = get_date(str(date))
    e = float(e)
    t = float(t)
    data = [date, e, t]
    if ValueError in data:
        return ValueError
    else:
        return data

    
def add_note():
    date = get_date("Please enter a date for this note/event (DD-MM-YYYY): ")
    note = input("Please enter the note/event: ")
    CSV.add_entry("notes",date, note)
    
def remove(mode):
    date = get_date("Please enter the date of the entry you would like to remove (DD-MM-YYYY)")
    CSV.remove_entry(mode, date)

def get_date(date_str):
    try:
        valid_date = datetime.strptime(date_str,date_format)
        return valid_date.strftime(date_format)
    except ValueError:
        print("invalid date format.")
        return ValueError
    
def change_e_lower():
    try:
        e_lower = int(input("Please enter new Oestrogen lower target: "))
        return e_lower
    except ValueError:
        print ("Invalid format, please enter a number.")
        return change_e_lower()
    
def change_e_upper():
    try:
        e_upper = int(input("Please enter new Oestrogen upper target: "))
        return e_upper
    except ValueError:
        print ("Invalid format, please enter a number.")
        return change_e_upper
    
def change_t_lower():
    try:
        t_lower = float(input("Please enter new Testosterone lower target: "))
        return t_lower
    except ValueError:
        print ("Invalid format, please enter a number.")
        return change_t_lower()
    
def change_t_upper():
    try:
        t_upper = float(input("Please enter new Testosterone upper target: "))
        return t_upper
    except ValueError:
        print ("Invalid format, please enter a number.")
        return change_t_upper()
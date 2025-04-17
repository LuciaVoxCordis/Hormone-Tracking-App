from os import path
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

#~~~~~~~~Frequently used variables~~~~~~~~#

wdir = path.dirname(__file__)
date_format = "%d-%m-%Y"


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Results CSV Class~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
class RESULTS_CSV:
    file_name = "Results.csv"
    columns = ["Date", "Oestradiol", "Testosterone"]
    

    @classmethod
    def initialize_csv(cls):
        try: 
            pd.read_csv(path.join(wdir, cls.file_name))  
            print ("Results.csv found!")
            return 
        except FileNotFoundError:
            print ("Results.csv not found, Creating...")
            df = pd.DataFrame(columns=cls.columns)
            df.to_csv(path.join(wdir, cls.file_name), index = False)
            
    @classmethod
    def add_entry(cls, date, e, t):
        data = {"D": [date], "E": [e], "T": [t]}
        df = pd.DataFrame(data=data)
        df.to_csv(path.join(wdir, cls.file_name), mode = 'a', index=False, header=False)
    
    @classmethod
    def remove_entry(cls, date):     #WIP
        df = pd.read_csv(path.join(wdir, cls.file_name))
        df["Date"] = pd.to_datetime(df["Date"], format = date_format)
        date = datetime.strptime(date, date_format)
        mask = (df["Date"] == date)
        isolated_entry = df.loc[mask].sort_values("Date")
        if isolated_entry.empty:
            print("No results found with the given date.")
        else:
            mask = (df["Date"] != date)
            filtered_df = df.loc[mask].sort_values("Date")
            df = pd.DataFrame(columns = cls.columns)
            df.to_csv(path.join(wdir, cls.file_name), index = False)
            filtered_df.to_csv(path.join(wdir, cls.file_name), mode = 'a', index=False, header=False, date_format=date_format)

    @classmethod
    def get_results(cls, start_date, end_date):
        df = pd.read_csv(path.join(wdir, cls.file_name))
        df["Date"] = pd.to_datetime(df["Date"], format = date_format)
        start_date = datetime.strptime(start_date, date_format)
        end_date = datetime.strptime(end_date, date_format)
        mask = (df["Date"] >= start_date) & (df["Date"] <= end_date) #this line took far too much googling and I'm still not *quite* sure how it works
        filtered_df = df.loc[mask].sort_values("Date")
        if filtered_df.empty:
            print("No results found within the given range.")
        else:
            print(f"Results from {start_date.strftime(date_format)} to {end_date.strftime(date_format)}.")
            print (filtered_df.to_string(index=False, formatters={"Date": lambda x: x.strftime(date_format)}))
        return filtered_df
    
    @classmethod
    def view_all(cls):
        df = pd.read_csv(path.join(wdir, cls.file_name))
        df["Date"] = pd.to_datetime(df["Date"], format = date_format)
        df.sort_values("Date", inplace = True)
        print (df.to_string(index = False, formatters = {"Date": lambda x: x.strftime(date_format)} ))
        return df
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Notes CSV Class~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
class NOTES_CSV:
    file_name = "Notes.csv"
    columns = ["Date", "Note"]
    
    @classmethod
    def initialize_csv(cls):
        try: 
            pd.read_csv(path.join(wdir, cls.file_name))  
            print ("Notes.csv found!")
            return 
        except FileNotFoundError:
            print ("Notes.csv not found, Creating...")
            df = pd.DataFrame(columns=cls.columns)
            df.to_csv(path.join(wdir, cls.file_name), index = False)
            
    @classmethod
    def add_entry(cls, date, note):
        data = {"D": [date],"n": [note]}
        df = pd.DataFrame(data=data)
        df.to_csv(path.join(wdir, cls.file_name), mode = 'a', index=False, header=False)
        
    @classmethod
    def remove_entry(cls, date):     #WIP
        df = pd.read_csv(path.join(wdir, cls.file_name))
        df["Date"] = pd.to_datetime(df["Date"], format = date_format)
        date = datetime.strptime(date, date_format)
        mask = (df["Date"] == date)
        isolated_entry = df.loc[mask].sort_values("Date")
        if isolated_entry.empty:
            print("No results found with the given date.")
        else:
            mask = (df["Date"] != date)
            filtered_df = df.loc[mask].sort_values("Date")
            df = pd.DataFrame(columns = cls.columns)
            df.to_csv(path.join(wdir, cls.file_name), index = False)
            filtered_df.to_csv(path.join(wdir, cls.file_name), mode = 'a', index=False, header=False, date_format=date_format)
            
    @classmethod
    def view_notes(cls):
        df = pd.read_csv(path.join(wdir, cls.file_name))
        df["Date"] = pd.to_datetime(df["Date"], format = date_format)
        df.sort_values("Date", inplace = True)
        print (df.to_string(index = False, formatters = {"Date": lambda x: x.strftime(date_format)} ))
        return df
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Settings JSON Class~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
class JSON:
    file_name = "Settings.json"
    data = {"e_lower": 400, "e_upper": 800,"t_lower": 0.3, "t_upper": 1.7}
    
    @classmethod
    def initialize_json(cls):
        try: 
            pd.read_json(path.join(wdir, cls.file_name), typ = 'series')
            print (".Json file found!")
            return 
        except FileNotFoundError:
            print (".Json file not found, Creating...")
            df = pd.Series(cls.data)
            df.to_json(path.join(wdir, cls.file_name), index=False)
            
    @classmethod
    def change_settings(cls, e_lower, e_upper, t_lower, t_upper):
        data = {"e_lower": e_lower, "e_upper": e_upper, "t_lower": t_lower, "t_upper": t_upper}
        df = pd.Series(data=data)
        df.to_json(path.join(wdir, cls.file_name), mode= 'w', index=False)
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def add_result():
    date = get_date("please enter the date of the test (DD-MM-YYYY): ")
    e = float(input("please enter Oestradiol levels (pmol/L): "))
    t = float(input("Please enter Testosterone levels (nmol/L): "))
    RESULTS_CSV.add_entry(date, e, t)
    
def add_note():
    date = get_date("Please enter a date for this note/event (DD-MM-YYYY): ")
    note = input("Please enter the note/event: ")
    NOTES_CSV.add_entry(date, note)
    
def remove(mode):
    date = get_date("Please enter the date of the entry you would like to remove (DD-MM-YYYY)")
    if mode == "result":
        RESULTS_CSV.remove_entry(date)
    elif mode == "note":
        NOTES_CSV.remove_entry(date)

def get_date(promt):
    date_str = input(promt)
    try:
        valid_date = datetime.strptime(date_str,date_format)
        return valid_date.strftime(date_format)
    except ValueError:
        print("invalid date format.")
        return get_date("Please enter a valid date format (DD-MM-YYYY)")
    
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
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Plotting~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#    
def plot_results(results_df):
    settings_df = pd.read_json(path.join(wdir, JSON.file_name), typ = 'series')
    notes_df = pd.read_csv(path.join(wdir, NOTES_CSV.file_name))
    notes_df["Date"] = pd.to_datetime(notes_df["Date"], format = date_format)
    results_df.set_index("Date", inplace = True)

    fig, ax1 = plt.subplots()

    color = '#F5A9B8'
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Oestradiol (pmol/L)', c = color)
    ax1.plot(results_df.index, results_df["Oestradiol"], c = color, marker = 'o', label = "oestadiol")
    ax1.axhspan(ymin = settings_df["e_lower"], ymax= settings_df["e_upper"], color = color, alpha = 0.25)
    ax1.set_ylim(bottom = 0)

    ax1.tick_params(axis='y', labelcolor=color)
    ax1.tick_params(axis = 'x', rotation = 45)

    ax2 = ax1.twinx()

    color = '#5BCEFA'
    ax2.set_ylabel('Testosterone (nmol/L)', color=color)
    ax2.plot(results_df.index, results_df["Testosterone"], color=color, marker = 'o', label = "Testosterone")
    ax2.axhspan(ymin = settings_df["t_lower"], ymax= settings_df["t_upper"], color = color, alpha = 0.25)
    ax2.set_ylim(bottom = 0)
    ax2.tick_params(axis='y', labelcolor=color)
    
    
    if notes_df.empty:
        pass
    else:
        for i, v in enumerate(notes_df["Date"]):
            plt.vlines(x = notes_df["Date"][i], ymin = 0, ymax = 1, transform = ax1.get_xaxis_transform(), colors = "grey", linestyles = "--")
            plt.text(x = notes_df["Date"][i], y = 0.1, transform = ax1.get_xaxis_transform(), s = notes_df["Note"][i], rotation = 90)
    
    fig.tight_layout()
    plt.show()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Main Loop~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def main():
    while True:
        print("\n1. Add new test results")
        print("2. Remove a test result")
        print("3. view all test results")
        print("4. View test results within a date range")
        print("5. add a new note/event")
        print("6. Remove a note/event")
        print("7. View notes")
        print("8. View and edit target levels")
        print("9. Exit")
        choice = input("Enter selection (1-9): ")
        
        if choice == "1":
            add_result()
        elif choice == "2":
            remove("result")
        elif choice == "3":
            df = RESULTS_CSV.view_all()
            if input("Do you wish to see a plot? (Y/N)").lower() == "y":
                plot_results(df)
        elif choice == "4":
            start_date = get_date("Please enter the date to display results from (DD-MM-YYYY): ")
            end_date = get_date("Please enter the date to display results to (DD-MM-YYYY): ")
            df = RESULTS_CSV.get_results(start_date, end_date)
            if input("Do you wish to see a plot? (Y/N)").lower() == "y":
                plot_results(df)
        elif choice == "5":
            add_note()
        elif choice == "6":
            remove("note")
        elif choice == "7":
            df = NOTES_CSV.view_notes()
            input ("Press any key to continue")
        elif choice == "8":
            settings_df = pd.read_json(path.join(wdir, JSON.file_name), typ = 'series')
            print("Current target levels are set to:")
            print(f"{settings_df['e_lower']}-{settings_df['e_upper']}pmol/L for Oestrogen\n{settings_df['t_lower']}-{settings_df['t_upper']}nmol/L for Testosterone.")
            if input ("Would you like to change this? (Y/N)").lower() == 'y':
                JSON.change_settings(change_e_lower(), change_e_upper(), change_t_lower(), change_t_upper())
        elif choice == "9":
            print ("Exiting...")
            break
        else:
            print("Please enter a valid option (1-9)")
            
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Run~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
if __name__ == "__main__":
    RESULTS_CSV.initialize_csv()
    NOTES_CSV.initialize_csv()
    JSON.initialize_json()
    
    df = pd.read_csv(path.join(wdir, NOTES_CSV.file_name))
    print (df)

    main() #and pray
    

    '''
    to do:
    Clean up & re-do the remove classmethod using pd.drop() if I can figure the damned thing out
    GUI
    '''
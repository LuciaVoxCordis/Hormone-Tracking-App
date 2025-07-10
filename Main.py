from global_vars import *
from csv_class import CSV
from json_class import JSON
from functions import add_result, add_note, initialize_data_folder, remove, get_date, change_e_lower, change_e_upper, change_t_lower, change_t_upper
from plotting import plot_results


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
            df = CSV.view_all("results")
            if input("Do you wish to see a plot? (Y/N)").lower() == "y":
                plot_results(df)
        elif choice == "4":
            start_date = get_date("Please enter the date to display results from (DD-MM-YYYY): ")
            end_date = get_date("Please enter the date to display results to (DD-MM-YYYY): ")
            df = CSV.get_results(start_date, end_date)
            if input("Do you wish to see a plot? (Y/N)").lower() == "y":
                plot_results(df)
        elif choice == "5":
            add_note()
        elif choice == "6":
            remove("note")
        elif choice == "7":
            df = CSV.view_all("notes")
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
    initialize_data_folder()
    CSV.initialize_files()
    JSON.initialize_json()
    main() #and pray
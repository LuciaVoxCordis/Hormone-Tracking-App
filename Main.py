from global_vars import *
from csv_class import CSV
from json_class import JSON
from functions import add_result, add_note, initialize_data_folder, remove, get_date, change_e_lower, change_e_upper, change_t_lower, change_t_upper
from plotting import plot_results


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Main Loop~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#def main():
#    while True:
#        print("\n1. Add new test results")
#        print("2. Remove a test result")
#        print("3. view all test results")
#        print("4. View test results within a date range")
#        print("5. add a new note/event")
#        print("6. Remove a note/event")
#        print("7. View notes")
#        print("8. View and edit target levels")
#        print("9. Exit")
#        choice = input("Enter selection (1-9): ")
#        
#        if choice == "1":
#            add_result()
#        elif choice == "2":
#            remove("result")
#        elif choice == "3":
#            df = CSV.view_all("results")
#            if input("Do you wish to see a plot? (Y/N)").lower() == "y":
#                plot_results(df)
#        elif choice == "4":
#            start_date = get_date("Please enter the date to display results from (DD-MM-YYYY): ")
#            end_date = get_date("Please enter the date to display results to (DD-MM-YYYY): ")
#            df = CSV.get_results(start_date, end_date)
#            if input("Do you wish to see a plot? (Y/N)").lower() == "y":
#                plot_results(df)
#        elif choice == "5":
#            add_note()
#        elif choice == "6":
#            remove("note")
#        elif choice == "7":
#            df = CSV.view_all("notes")
#            input ("Press any key to continue")
#        elif choice == "8":
#            settings_df = pd.read_json(path.join(wdir, JSON.file_name), typ = 'series')
#            print("Current target levels are set to:")
#            print(f"{settings_df['e_lower']}-{settings_df['e_upper']}pmol/L for Oestrogen\n{settings_df['t_lower']}-{settings_df['t_upper']}nmol/L for Testosterone.")
#            if input ("Would you like to change this? (Y/N)").lower() == 'y':
#                JSON.change_settings(change_e_lower(), change_e_upper(), change_t_lower(), change_t_upper())
#        elif choice == "9":
#            print ("Exiting...")
#            break
#        else:
#            print("Please enter a valid option (1-9)")
#            
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Tkinter~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

#window
window = tk.Tk()
window.geometry('800x600')
window.title('Hormone Tracking')

#tabs
tabs = ttk.Notebook(window)

#Results Tab
tab_results = ttk.Frame(tabs)
tab_results.pack()
label_add_result = ttk.Label(tab_results, text = 'Results')
label_add_result.pack()

#Results Table
table = ttk.Treeview(tab_results, columns = ('Date', 'Estrogen Level', 'Testosterone Level'), show = 'headings')
table.heading('Date', text = 'Date')
table.heading('Estrogen Level', text = 'Estrogen Level')
table.heading('Testosterone Level', text = 'Testosterone Level')
table.pack(fill = 'both', expand = True)

def draw_table():
    for i in table.get_children():
        table.delete(i) 
    df = CSV.view_all("results")
    for i, v in df.iterrows():
        date = v['Date'].strftime(date_format)
        e_levels = v['Oestradiol']
        t_levels = v['Testosterone']
        data = (date, e_levels, t_levels)
        table.insert(parent = '', index = 0, values = data)

frame_table_buttons = ttk.Frame(tab_results)
frame_table_buttons.pack()

def delete_items():
    for i in table.selection():
        CSV.remove_entry("result", table.item(i)['values'][0])
        draw_table()
        
button_delete_items = ttk.Button(frame_table_buttons, text = 'Delete selected item(s)', command = delete_items)
button_delete_items.pack(side = 'left', padx = 5)

def view_graph():
    df = CSV.view_all("results")
    plot_results(df)

button_view_graph = ttk.Button(frame_table_buttons, text = 'View results as graph', command = view_graph)
button_view_graph.pack(side = 'right', padx = 5)

#Add Results Frame
frame_add_results = ttk.Frame(tab_results)
frame_add_results.pack()

label_add_result = ttk.Label(frame_add_results, text = 'Add a new Result')
label_add_result.pack()

frame_labels = ttk.Frame(frame_add_results)
frame_labels.pack()
label_date = ttk.Label(frame_labels, text = 'Date: (DD-MM-YYYY)')
label_date.pack(side = 'left', padx = 5)
label_estrogen = ttk.Label(frame_labels, text = 'Estrogen Level (pmol/L)')
label_estrogen.pack(side = 'left', padx = 5)
label_testosterone = ttk.Label(frame_labels, text = 'Testosteron Level (nmol/L)')
label_testosterone.pack(side = 'left', padx = 5)

frame_results_entries = ttk.Frame(frame_add_results)
frame_results_entries.pack()
date_var = tk.StringVar(value = 'DD-MM-YYYY')
entry_date = ttk.Entry(frame_results_entries, textvariable = date_var)
entry_date.bind('<FocusIn>', lambda event: date_var.set(''))
entry_date.pack(side = 'left')

estrogen_var = tk.IntVar(value = 0)
entry_estrogen = ttk.Entry(frame_results_entries, textvariable = estrogen_var)
entry_estrogen.bind('<FocusIn>', lambda event: estrogen_var.set(''))
entry_estrogen.pack(side = 'left')

testosterone_var = tk.IntVar(value = 0)
entry_testosterone = ttk.Entry(frame_results_entries, textvariable = testosterone_var)
entry_testosterone.bind('<FocusIn>', lambda event: testosterone_var.set(''))
entry_testosterone.pack(side = 'left')

def handle_button_add_result():
    try:
        date = get_date(str(date_var.get()))
        estrogen = float(estrogen_var.get())
        testosterone = float(testosterone_var.get())
        if date == ValueError:
            print('date error!')
        else:
            data = [date, estrogen, testosterone]
            CSV.add_entry("results", date, estrogen, testosterone)
            draw_table()
    except TclError:
        print('float error!')

button_add_result = ttk.Button(frame_add_results, text = 'Add Result', command = handle_button_add_result)
button_add_result.pack()

#Notes Tab
tab_notes = ttk.Frame(tabs)
label_remove_result = ttk.Label(tab_notes, text = 'Notes')
label_remove_result.pack()

#Settings Tab
tab_settings = ttk.Frame(tabs)
label_settings = ttk.Label(tab_settings, text = 'Settings')#
label_settings.pack()


tabs.add(tab_results, text = 'Results')
tabs.add(tab_notes, text = 'Notes')
tabs.add(tab_settings, text = 'Settings')
tabs.pack()

            
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Run~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
if __name__ == "__main__":
    initialize_data_folder()
    CSV.initialize_files()
    JSON.initialize_json()
    draw_table()
    window.mainloop()
    
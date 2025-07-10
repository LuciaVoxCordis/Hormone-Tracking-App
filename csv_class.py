from global_vars import *
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~CSV Class~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

class CSV:
    results_filename = "results.csv"
    results_columns = ["Date", "Oestradiol", "Testosterone"]
    notes_filename = "Notes.csv"
    notes_columns = ["Date", "Note"]
    
    @classmethod
    def initialize_files(cls):
        cls.initialize_csv(cls.results_filename, cls.results_columns)
        cls.initialize_csv(cls.notes_filename, cls.notes_columns)
    
    @classmethod
    def initialize_csv(cls, filename, columns):
        try: 
            pd.read_csv(path.join(wdir, filename))  
            print (f"{filename} found!")
        except FileNotFoundError:
            print (f"{filename} not found, Creating...")
            df = pd.DataFrame(columns=columns)
            df.to_csv(path.join(wdir, filename), index = False)
        
    @classmethod
    def add_entry(cls, mode, *args):            
        if mode == "results":
            filename = cls.results_filename
            date, estrogen, testosterone = args
            data = {"D": [date], "E": [estrogen], "T": [testosterone]}
        elif mode == "notes":
            filename = cls.notes_filename
            date, note = args
            data = {"D": [date],"n": [note]}        
        df = pd.DataFrame(data=data)
        df.to_csv(path.join(wdir, filename), mode = 'a', index=False, header=False)
            
    @classmethod
    def remove_entry(cls, mode, date): #need to refactor to use .drop method but it hurts my head
        if mode == "result":
            filename = cls.results_filename
            columns = cls.results_columns
        elif mode == "note":
            filename = cls.notes_filename
            columns = cls.notes_columns
        df = pd.read_csv(path.join(wdir, filename))
        df["Date"] = pd.to_datetime(df["Date"], format = date_format)
        date = datetime.strptime(date, date_format)
        mask = (df["Date"] == date)
        isolated_entry = df.loc[mask].sort_values("Date")
        if isolated_entry.empty:
            print("No results found with the given date.")
        else:
            mask = (df["Date"] != date)
            filtered_df = df.loc[mask].sort_values("Date")
            df = pd.DataFrame(columns = columns)
            df.to_csv(path.join(wdir, filename), index = False)
            filtered_df.to_csv(path.join(wdir, filename), mode = 'a', index=False, header=False, date_format=date_format)
        
    @classmethod
    def get_results(cls, start_date, end_date):
        df = pd.read_csv(path.join(wdir, cls.results_filename))
        df["Date"] = pd.to_datetime(df["Date"], format = date_format)
        start_date = datetime.strptime(start_date, date_format)
        end_date = datetime.strptime(end_date, date_format)
        mask = (df["Date"] >= start_date) & (df["Date"] <= end_date)
        filtered_df = df.loc[mask].sort_values("Date")
        if filtered_df.empty:
            print("No results found within the given range.")
        else:
            print(f"Results from {start_date.strftime(date_format)} to {end_date.strftime(date_format)}.")
            print (filtered_df.to_string(index=False, formatters={"Date": lambda x: x.strftime(date_format)}))
        return filtered_df
    
    @classmethod
    def view_all(cls, mode):
        if mode == "results":
            filename = cls.results_filename
        elif mode == "notes":
            filename = cls.notes_filename            
        df = pd.read_csv(path.join(wdir, filename))
        df["Date"] = pd.to_datetime(df["Date"], format = date_format)
        df.sort_values("Date", inplace = True)
        print (df.to_string(index = False, formatters = {"Date": lambda x: x.strftime(date_format)} ))
        return df

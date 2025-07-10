from global_vars import *

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
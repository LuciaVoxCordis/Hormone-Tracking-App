from os import path, mkdir
import pandas as pd
from datetime import datetime

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Vars~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
wdir = path.join(path.dirname(__file__), 'Data')
date_format = "%d-%m-%Y"
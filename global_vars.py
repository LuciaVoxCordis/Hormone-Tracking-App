from os import path, mkdir
import pandas as pd
from datetime import datetime
import tkinter as tk
from tkinter import ttk, TclError

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Vars~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
wdir = path.join(path.dirname(__file__), 'Data')
date_format = "%d-%m-%Y"
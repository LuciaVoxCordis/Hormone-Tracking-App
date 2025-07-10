from global_vars import *
import matplotlib as plt

from csv_class import CSV
from json_class import JSON

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Plotting~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#    
def plot_results(results_df):
    settings_df = pd.read_json(path.join(wdir, JSON.file_name), typ = 'series')
    notes_df = pd.read_csv(path.join(wdir, CSV.notes_filename))
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
"""
Title: panels_summary.py
Version: 2.0
Release Date: 14 August 2017
Author: VFryer
The following code retrieves all panel names from PanelApp, with current panel versions.
The virtual environment must be activated before running this script (source bin/activate)
Usage: python3 panels_summary.py <output file location>
"""

import requests, json, csv, datetime, sys, os, sqlite3
#import plotly
#import plotly.graph_objs as go
#from plotly.offline import plot
import pandas as pd
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

out_path = sys.argv[1]

# save today's date to use in the filename to record a snapshot of panel versions on a weekly basis
todays_date = datetime.datetime.now().strftime("%Y-%m-%d")
print(todays_date)

# retrieve a list of all panel names
try:
    r = requests.get('https://panelapp.extge.co.uk/crowdsourcing/WebServices/list_panels')
    panel_data = r.json()
except:
    print("No connection establshed with PanelApp")
    sys.exit(1)

panel_list = panel_data["result"]

filename = os.path.join(out_path,'panel_versions_' + todays_date + '.csv')

csv_file = open(filename, 'w')
writer = csv.writer(csv_file, delimiter=",")

writer.writerow(['Panel Name', 'Panel ID', 'Version Number'])

tot_panel_count = 0
v1_panel_count = 0
v0_panel_count = 0

for panel in panel_list:
    panel_id = panel["Panel_Id"]
    panel_name = panel["Name"]
    curr_version_num = panel["CurrentVersion"]
    tot_panel_count +=1 # count the total number of panels in PanelApp
    if float(curr_version_num) <1:
    	v0_panel_count +=1 # count all panels < v1.0
    elif float(curr_version_num) >=1:
    	v1_panel_count +=1 # count all panels >= v1.0

# write the panel name, id and version number to a csv file
    row = [panel_name,panel_id,curr_version_num]
    writer.writerow(row)

# create a connection to the specified SQLite database
conn = sqlite3.connect("outputs/PanelApp_Data.db")
cur = conn.cursor()

# create a table in the database if it does not already exist
#try:
#    cur.execute("CREATE TABLE IF NOT EXISTS panelapp_summary (Date TEXT, Total_Panels TEXT, v0_Total TEXT, v1_Total TEXT)")
#except:
#    print("Cannot create table. It may already exist. Program will now end.")
#    sys.exit()

# save the panel counts into database table
cur.execute("INSERT INTO panelapp_summary ('Date','Total_Panels', 'v0_Total', 'v1_Total') VALUES (?,?,?,?)",(todays_date, str(tot_panel_count), str(v0_panel_count), str(v1_panel_count), ))
conn.commit()

# create a dataframe of all months values form  database table
df = pd.read_sql_query("SELECT * FROM panelapp_summary", conn)

# amend the dataframe for graph
df = df.set_index('Date')
df = df.sort_index()
df=df.drop('Total_Panels',1)
df=df.astype(int) # change dtypes to ints instead of objects
print(df)

ax = df.plot(kind='bar',stacked=True, title='PanelApp progress', legend=True, rot=0, colormap='winter')
ax.set_xlabel("Date", rotation=0)
ax.set_ylabel("Number of panels")
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.85, box.height]) # shrink width of plot to fit legend
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5)) # position legend outside of plot
fig = ax.get_figure()
fig.savefig(out_path + todays_date + '_panel_summary.png')

# close the connection to the database
cur.close()
conn.close()

"""
Title: panels_curr_version.py
Version: 
Release Date: 
Author: VFryer
The following code retrieves all panel names from PanelApp, with current panel versions.
Usage: python panels_curr_version.py <output file location>
"""

import requests,json,csv,datetime,sys,os

out_path = sys.argv[1]

# save today's date to use in the filename to record a snapshot of panel versions on a weekly basis
todays_date = datetime.datetime.now().strftime("%Y%m%d")

# retrieve a list of all panel names
r = requests.get('https://bioinfo.extge.co.uk/crowdsourcing/WebServices/list_panels')
panel_data = r.json()

panel_list = panel_data["result"]

filename = os.path.join(out_path,'panel_versions_list_' + todays_date + '.csv')

csv_file = open(filename, 'w')
writer = csv.writer(csv_file, delimiter=",")

writer.writerow(['Panel Name', 'Panel ID', 'Version Number'])

for panel in panel_list:
    panel_id = panel["Panel_Id"]
    panel_name = panel["Name"]
    curr_version_num = panel["CurrentVersion"]
    
# write the panel name, id and version number to a csv file
    row = [panel_name,panel_id,curr_version_num]
    writer.writerow(row)

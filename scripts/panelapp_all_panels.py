"""
The following code retrieves all panel names from PanelApp 
"""

import requests, json

# Get a list of all panel names currently in PanelApp using their list_panels endpoint to get the data in json format

r = requests.get('https://bioinfo.extge.co.uk/crowdsourcing/WebServices/list_panels')
panel_data = r.json()

# store the data in memory as a list of dictionaries (the current JSON format contians a dictionary of a list of dictionaries)

panel_list = panel_data["result"]

# iterate through the list of dictionaries, printing out only the values associated with "Name" key

for dict in panel_list:
    if "Name" in dict:
        print(dict["Name"])

    
# count the number of panels (this can be used to check against the PanelApp website and ensure the script is working)

print("Number of panels: " + str(len(panel_list)))


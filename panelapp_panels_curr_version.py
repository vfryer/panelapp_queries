"""
Ttle: panelapp_panels_curr_version.py
Version: v1.0
Release Date: 25/05/2017
Author: VFryer
The following code retrieves all panel names from PanelApp, with current panel versions.
"""

import requests,json,xlsxwriter,datetime

# save today's date to use in the filename to record a snapshot of panel versions on a weekly basis
todays_date = datetime.datetime.now().strftime("%Y%m%d")
# print(todays_date)

workbook = xlsxwriter.Workbook('panel_versions_list_' + todays_date + '.xlsx')
worksheet = workbook.add_worksheet('Panel_versions')

# Add a bold format to use to highlight cells.
bold = workbook.add_format({'bold': True})

worksheet.write('A1', 'Panel Name', bold)
worksheet.write('B1', 'Panel Id', bold)
worksheet.write('C1', 'Version Number', bold)

row = 1
col = 0

# retrieve a list of all panel names
r = requests.get('https://bioinfo.extge.co.uk/crowdsourcing/WebServices/list_panels')
panel_data = r.json()

panel_list = panel_data["result"]

for panel in panel_list:
    panel_id = panel["Panel_Id"]
    panel_name = panel["Name"]
    curr_version_num = panel["CurrentVersion"]

# write the panel name, id and version number to an Excel file
    worksheet.write(row, col, panel_name)
    worksheet.write(row, col+1, panel_id)
    worksheet.write(row, col+2, curr_version_num)
    row = row+1


# save all data to the Excel spreadsheet by closing it.
workbook.close()

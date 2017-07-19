"""
Title: panels_genes_curr.py
Version: 1.0
Release Date: 19/07/2017  
Author: VFryer
The following code retrieves all panel names from PanelApp, with current panel versions, gene symbols, gene status and mode of inheritance (MOI).
All captured data is exported into an SQLite database and a .csv (back-up for SQLite).
User specifies the location of the back-up .csv file(outputs/archive recommended) in the command line
Usage: python panels_genes_curr.py <output file location>
"""

import requests, json, csv, datetime, sys, os
import sqlite3, time, pandas as pd

# create a connection to the specified SQLite database
conn = sqlite3.connect("outputs/PanelApp_Data.db")
cur = conn.cursor()

# save today's date to use in the filename to record a snapshot of panel versions on a weekly basis
todays_date = datetime.datetime.now().strftime("%Y%m%d")
datestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

try:
    cur.execute(
        "CREATE TABLE IF NOT EXISTS panelapp_info (Datestamp TEXT,Panel_Name TEXT,Panel_ID TEXT,Version_Num TEXT,Gene_Symbol TEXT,Gene_Status TEXT,MOI TEXT)")
except:
    print("Cannot create table. It may already exist. Program will now end.")
    sys.exit()

out_path = sys.argv[1]

# retrieve a list of all panel names
r = requests.get('https://bioinfo.extge.co.uk/crowdsourcing/WebServices/list_panels')
panel_data = r.json()

panel_list = panel_data["result"]

filename = os.path.join(out_path, 'panels_genes_' + todays_date + '.csv')

csv_file = open(filename, 'w')
writer = csv.writer(csv_file, delimiter=",")

writer.writerow(['Panel Name', 'Panel ID', 'Version Number', 'Gene Name', 'Gene Status', 'Date Recorded','MOI'])

panel_count = 0

for panel in panel_list:
    panel_id = panel["Panel_Id"]
    panel_name = panel["Name"]
    version_num = panel["CurrentVersion"]
    print('Checking panel: ' + panel_name + '...')
    panel_count +=1

    try:
        url = 'https://bioinfo.extge.co.uk/crowdsourcing/WebServices/get_panel/' + panel_id + '/?version=' + version_num
        r = requests.get(url)

        panel_data = r.json()

        # retrieve gene name and status for each version
        gene_info = panel_data['result']['Genes']

        if gene_info == []:
            # write data retrieved into a .csv to be archived and saved for future reference
            row = [panel_name, panel_id, version_num, gene_symbol, 'N/A', 'N/A', 'N/A']
            writer.writerow(row)

            # write data to database for subsequent analysis
            cur.execute("INSERT INTO panelapp_info VALUES (?,?,?,?,?,?,?)",(datestamp,panel_name,panel_id,version_num, 'N/A', 'N/A', 'N/A'))
            conn.commit()


        # get all genes and their status
        for gene in gene_info:
            gene_symbol = gene["GeneSymbol"]
            gene_confidence = gene["LevelOfConfidence"]
            moi = gene["ModeOfInheritance"]
            # print(gene_symbol, gene_confidence)
            if gene_confidence == "LowEvidence":
                gene_status = "Red"
            elif gene_confidence == "HighEvidence":
                gene_status = "Green"
            elif gene_confidence == "ModerateEvidence":
                gene_status = "Amber"
            else:
                gene_status = "Unknown"

            # print(datestamp,panel_name,panel_id,version_num,gene_symbol,gene_status,moi)
            # write data retrieved into a .csv to be archived and saved for future reference
            row = [panel_name, panel_id, version_num, gene_symbol, gene_status, datestamp, moi]
            writer.writerow(row)

            # write data to database for subsequent analysis
            cur.execute("INSERT INTO panelapp_info VALUES (?,?,?,?,?,?,?)",(datestamp,panel_name,panel_id,version_num,gene_symbol,gene_status,moi))
            conn.commit()

    except:
        # if the try loop fails for any reason, inform user
        print("Panel not found")

print(str(panel_count) + " panels counted")

cur.close()
conn.close()


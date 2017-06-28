"""
Title: panels_genes_curr.py
Version:
Release Date:  
Author: VFryer
The following code retrieves all panel names from PanelApp, with current panel versions, gene symbols and gene status
Usage: python panels_genes_curr.py <output file location>
"""

import requests, json, csv, datetime, sys, os
import sqlite3, time

conn = sqlite3.connect("outputs/PanelApp_Data.db")
cur = conn.cursor()

# save today's date to use in the filename to record a snapshot of panel versions on a weekly basis
todays_date = datetime.datetime.now().strftime("%Y%m%d")
timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

table_name = 'panels_genes_' + todays_date

try:
    cur.execute(
        'CREATE TABLE IF NOT EXISTS panel_info (Datestamp TEXT,Panel_Name TEXT,Panel_ID TEXT,Version_Num TEXT,Gene_Symbol TEXT,Gene_Status TEXT,MOI TEXT)')
except:
    print("Cannot create database. Database may already exist")
    sys.exit()

out_path = sys.argv[1]

# retrieve a list of all panel names
r = requests.get('https://bioinfo.extge.co.uk/crowdsourcing/WebServices/list_panels')
panel_data = r.json()

panel_list = panel_data["result"]

filename = os.path.join(out_path, 'panels_genes_list_' + todays_date + '.csv')

csv_file = open(filename, 'w')
writer = csv.writer(csv_file, delimiter=",")

writer.writerow(['Panel Name', 'Panel ID', 'Version Number', 'Gene Name', 'Gene Status', 'Date Recorded','MOI'])

for panel in panel_list:
    panel_id = panel["Panel_Id"]
    panel_name = panel["Name"]
    version_num = panel["CurrentVersion"]
    print('Checking panel: ' + panel_name + '...')

    try:
        url = 'https://bioinfo.extge.co.uk/crowdsourcing/WebServices/get_panel/' + panel_id + '/?version=' + version_num
        # print(url)
        r = requests.get(url)

        panel_data = r.json()

        # retrieve gene name and status for each version
        gene_info = panel_data['result']['Genes']

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
                # print(panel_name,panel_version,gene_symbol,gene_status)
            row = [panel_name, panel_id, version_num, gene_symbol, gene_status, timestamp, moi]
            writer.writerow(row)
            cur.execute(
                'INSERT INTO panelapp_info (Datestamp,Panel_Name,Panel_ID,Version_Num,Gene_Symbol,Gene_Status,MOI) VALUES (?,?,?,?,?,?,?)',(timestamp,panel_name,panel_id,version_num,gene_symbol,gene_status,moi))
            conn.commit()

    except:
        print("Panel not found")

    # write the panel name, id and version number to a csv file

cur.close()
conn.close()
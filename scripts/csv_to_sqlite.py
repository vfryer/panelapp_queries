"""
Title: csv_to_sqlite.py
Version:
Release Date:  
Author: VFryer
The following code allows a .csv file all panels to be used to retrieve previous versions of panels and load the associated data into the PanelApp DB.
Usage: python csv_to_sqlite.py <csv file to upload>
"""

import requests, json, csv, datetime, sys, os
import sqlite3, time

conn = sqlite3.connect("outputs/PanelApp_Data.db")
cur = conn.cursor()

'''
try:
    cur.execute(
        "CREATE TABLE IF NOT EXISTS panelapp_info (Datestamp TEXT,Panel_Name TEXT,Panel_ID TEXT,Version_Num TEXT,Gene_Symbol TEXT,Gene_Status TEXT,MOI TEXT)")
except:
    print("Cannot create table. It may already exist. Program will now end.")
    sys.exit()

input_file = sys.argv[1]
datestamp = os.path.splitext(os.path.basename(input_file))[0]
datestamp = datestamp.split('_')[3]
datestamp = datestamp + " 01:00:00"
print(datestamp)

with open(input_file, 'r') as csvfile:
    read_csv = csv.reader(csvfile)
    next(read_csv, None)  # skip the headers
    for row in read_csv:

        panel_id = row[1]
        panel_name = row[0]
        version_num = row[2]
        print('Checking panel: ' + panel_name + '...')

        try:
            url = 'https://bioinfo.extge.co.uk/crowdsourcing/WebServices/get_panel/' + panel_id + '/?version=' + version_num
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

                # print(datestamp,panel_name,panel_id,version_num,gene_symbol,gene_status,moi)

                # write data to database for subsequent analysis
                cur.execute("INSERT INTO panelapp_info VALUES (?,?,?,?,?,?,?)",(datestamp,panel_name,panel_id,version_num,gene_symbol,gene_status,moi))
                conn.commit()

        except:
            # if the try loop fails for any reason, inform user
            print("Panel not found")
'''

def delete_data():
    cur.execute("SELECT DISTINCT Datestamp from panelapp_info")
    data = cur.fetchall()
    for row in data:
        print(row)

    cur.execute("DELETE FROM panelapp_info WHERE Datestamp LIKE '2017-06-29 12:11%'")
    conn.commit()

    cur.execute("SELECT DISTINCT Datestamp from panelapp_info")
    data = cur.fetchall()
    for row in data:
        print(row)


delete_data()
cur.close()
conn.close()
"""
Title: panels_genes_curr.py
Version:
Release Date:  
Author: VFryer
The following code retrieves all panel names from PanelApp, with current panel versions, gene symbols and gene status
Usage: python panels_genes_curr.py <output file location>
"""

import requests, json, csv, datetime, sys, os
import time, pandas as pd

# save today's date to use in the filename to record a snapshot of panel versions on a weekly basis
todays_date = datetime.datetime.now().strftime("%Y%m%d")
datestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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
            # write data retrieved into a .csv to be archived and saved for future reference
            row = [panel_name, panel_id, version_num, gene_symbol, gene_status, datestamp, moi]
            writer.writerow(row)

    except:
        # if the try loop fails for any reason, inform user
        print("Panel not found")
'''
prev_version = "2017-05-23"
curr_version = "2017-06-30"


writer = pd.ExcelWriter('panels_genes_list_' + prev_version + '_to_' + curr_version + '.xlsx')

def new_panels():
    # any panels that exist in latest panel version capture that did not exist in the previous panel capture
    cur.execute("SELECT DISTINCT panel_name FROM panelapp_info WHERE Datestamp LIKE ? AND panel_name NOT IN(SELECT panel_name FROM panelapp_info WHERE Datestamp LIKE ?)",(curr_version+'%',prev_version+'%'))
    data = cur.fetchall()
    print("New panels: ")
    for row in data:
        print(row)

def del_panels():
    # any panels that do not exist in latest panel version capture vs. a previously panel capture
    cur.execute("SELECT DISTINCT panel_name FROM panelapp_info WHERE Datestamp LIKE ? AND panel_name NOT IN(SELECT panel_name FROM panelapp_info WHERE Datestamp LIKE ?)",(prev_version+'%',curr_version+'%'))
    data = cur.fetchall()
    print("Retired panels: ")
    for row in data:
        print(data)

def promoted_panels():
    # any panels that have been promoted to v1.0 or higher from less than v1.0
    df1 = pd.read_sql_query("SELECT DISTINCT panel_name, version_num FROM panelapp_info WHERE Datestamp LIKE '2017-05-23%' AND version_num <1", conn)
    df2 = pd.read_sql_query("SELECT DISTINCT panel_name, version_num FROM panelapp_info WHERE Datestamp LIKE '2017-06-30%' AND version_num >=1", conn)
    print("Promoted panels: ")
    prom_panel_df = pd.merge(df1, df2, on='Panel_Name', how='inner')
    prom_panel_df.to_excel(writer, 'Promoted Panels')
    print(prom_panel_df)

def promoted_genes():
    df1 = pd.read_sql_query("SELECT panel_name, gene_symbol, gene_status FROM panelapp_info WHERE Datestamp LIKE '2017-05-23%' AND gene_status != 'Green'", conn)
    df2 = pd.read_sql_query("SELECT panel_name, gene_symbol, gene_status FROM panelapp_info WHERE Datestamp LIKE '2017-06-30%' AND gene_status = 'Green' AND version_num >=1", conn)
    print("Promoted genes: ")
    promoted_df = pd.merge(df1, df2, on=['Panel_Name','Gene_Symbol'], how='inner')
    promoted_df.to_excel(writer, 'Promoted Genes')
    print(promoted_df)

def demoted_genes():
    # any genes in panels v1.0 and higher, where gene was previously rated 'Green' but is no longer rated as 'Green'
    df1 = pd.read_sql_query("SELECT panel_name, gene_symbol, gene_status FROM panelapp_info WHERE Datestamp LIKE '2017-05-23%' AND gene_status = 'Green' AND version_num >=1", conn)
    df2 = pd.read_sql_query("SELECT panel_name, gene_symbol, gene_status FROM panelapp_info WHERE Datestamp LIKE '2017-06-30%' AND gene_status != 'Green'", conn)
    print("Demoted genes: ")
    demoted_df = pd.merge(df1, df2, on=['Panel_Name','Gene_Symbol'], how='inner')
    demoted_df.to_excel(writer, 'Demoted genes')
    print(demoted_df)

def moi_change():
    # any green genes in panels v1.0 and higher, in which the mode of inheritance of the gene has changed
    df1 = pd.read_sql_query("SELECT panel_name, gene_symbol, moi, version_num FROM panelapp_info WHERE Datestamp LIKE '2017-05-23%' AND version_num >=1", conn)
    df2 = pd.read_sql_query("SELECT panel_name, gene_symbol, moi, version_num FROM panelapp_info WHERE Datestamp LIKE '2017-06-30%' AND gene_status = 'Green'", conn)
    print("MOI changed genes: ")
    moi_change_df = pd.merge(df1, df2, on=['Panel_Name','Gene_Symbol'], how='inner')
    moi_change_df['MOI_x'].fillna(value='NaN', inplace=True)
    moi_change_df['MOI_y'].fillna(value='NaN', inplace=True)
    moi_change_df = moi_change_df[moi_change_df.MOI_x != moi_change_df.MOI_y]
    moi_change_df.to_excel(writer, 'MOI changed')
    print(moi_change_df)

'''
def update_data():
    # N.B. *** N.B. Data amended in SQLite B cannot be restored!***
    cur.execute("SELECT * from panelapp_info WHERE Datestamp LIKE '201705%'")
    data = cur.fetchall()

    cur.execute("UPDATE panelapp_info SET Datestamp = '2017-05-23 01:00:00' WHERE Datestamp = '20170523 01:00:00'")
    conn.commit()
    
    cur.execute("SELECT * from panelapp_info WHERE Datestamp LIKE '201705%'")
    data = cur.fetchall()

def delete_data():
    # ***N.B. data deleted from SQLite DB cannot be restored!***
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
'''

new_panels()
del_panels()
promoted_panels()
promoted_genes()
demoted_genes()
moi_change()
# update_data()
# delete_data()
'''

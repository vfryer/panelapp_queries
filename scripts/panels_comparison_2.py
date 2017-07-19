"""
Title: panels_genes_curr.py
Version:
Release Date:  
Author: VFryer
The following code retrieves all panel names from PanelApp, with current panel versions, gene symbols and gene status
Usage: python panels_genes_curr.py <output file location>
"""

import requests, json, csv, datetime, sys, os
import sqlite3, time, pandas as pd

# create a connection to the specified SQLite database
conn = sqlite3.connect("outputs/PanelApp_Data.db")
cur = conn.cursor()

# save today's date to use in the filename to record a snapshot of panel versions on a weekly basis
#todays_date = datetime.datetime.now().strftime("%Y%m%d")
#datestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#try:
#    cur.execute(
#        "CREATE TABLE IF NOT EXISTS panelapp_info (Datestamp TEXT,Panel_Name TEXT,Panel_ID TEXT,Version_Num TEXT,Gene_Symbol TEXT,Gene_Status TEXT,MOI TEXT)")
#except:
#    print("Cannot create table. It may already exist. Program will now end.")
#    sys.exit()

out_path = sys.argv[1]

# filename = os.path.join(out_path, 'panels_genes_list_' + todays_date + '.csv')

#csv_file = open(filename, 'w')
#writer = csv.writer(csv_file, delimiter=",")

prev_version = "2017-07-10"
curr_version = "2017-07-17"

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
    df1 = pd.read_sql_query("SELECT DISTINCT panel_name, panel_id, version_num FROM panelapp_info WHERE Datestamp LIKE '2017-07-10%' AND version_num <1", conn)
    df2 = pd.read_sql_query("SELECT DISTINCT panel_name, panel_id, version_num FROM panelapp_info WHERE Datestamp LIKE '2017-07-17%' AND version_num >=1", conn)
    print("Promoted panels: ")
    prom_panel_df = pd.merge(df1, df2, on='Panel_ID', how='inner')
    prom_panel_df = prom_panel_df.drop('Panel_Name_y',1)
    prom_panel_df = prom_panel_df.rename(columns={'Version_Num_x':'Prev_Version_Num','Panel_Name_x':'Panel_Name','Version_Num_y':'Curr_Version_Num'})
    prom_panel_df.to_excel(writer, 'Promoted Panels',index=False)
    print(prom_panel_df)

def new_genes():
    # any genes that have been added to any v1+ panels with status of 'green' that were not in previous panels
    cur.execute("SELECT DISTINCT panel_name FROM panelapp_info WHERE Datestamp LIKE ? AND panel_name NOT IN(SELECT panel_name FROM panelapp_info WHERE Datestamp LIKE ?)",(curr_version+'%',prev_version+'%'))
    data = cur.fetchall()
    print("New genes: ")
    for row in data:
        print(row)

#def del_genes():
    # any 'green' genes that have been removed from any v1+ panels

def promoted_genes():
    # any genes within v1.0+ panels that are currently 'green' that were previously not 'green'
    df1 = pd.read_sql_query("SELECT DISTINCT panel_name, panel_id, gene_symbol, gene_status, version_num FROM panelapp_info WHERE Datestamp LIKE '2017-07-10%' AND gene_status != 'Green'", conn)
    df2 = pd.read_sql_query("SELECT DISTINCT panel_name, panel_id, gene_symbol, gene_status, version_num FROM panelapp_info WHERE Datestamp LIKE '2017-07-17%' AND gene_status = 'Green' AND version_num >=1", conn)
    print("Promoted genes: ")
    promoted_df = pd.merge(df1, df2, on=['Panel_ID','Gene_Symbol'], how='inner')
    promoted_df = promoted_df.drop('Panel_Name_y',1)
    promoted_df = promoted_df.rename(columns={'Version_Num_x':'Prev_Version_Num','Panel_Name_x':'Panel_Name','Version_Num_y':'Curr_Version_Num','Gene_Status_x':'Prev_Gene_Status','Gene_Status_y':'Curr_Gene_Status'})
    promoted_df.to_excel(writer, 'Promoted Genes',index=False)
    print(promoted_df)

def demoted_genes():
    # any genes in panels v1.0 and higher, where gene was previously rated 'Green' but is no longer rated as 'Green'
    df1 = pd.read_sql_query("SELECT DISTINCT panel_name, panel_id, gene_symbol, gene_status, version_num FROM panelapp_info WHERE Datestamp LIKE '2017-07-10%' AND gene_status = 'Green' AND version_num >=1", conn)
    df2 = pd.read_sql_query("SELECT DISTINCT panel_name, panel_id, gene_symbol, gene_status, version_num FROM panelapp_info WHERE Datestamp LIKE '2017-07-17%' AND gene_status != 'Green'", conn)
    print("Demoted genes: ")
    demoted_df = pd.merge(df1, df2, on=['Panel_ID','Gene_Symbol'], how='inner')
    demoted_df = demoted_df.drop('Panel_Name_y',1)
    demoted_df = demoted_df.rename(columns={'Version_Num_x':'Prev_Version_Num','Panel_Name_x':'Panel_Name','Version_Num_y':'Curr_Version_Num','Gene_Status_x':'Prev_Gene_Status','Gene_Status_y':'Curr_Gene_Status'})
    demoted_df.to_excel(writer, 'Demoted genes', index=False)
    print(demoted_df)

def moi_change():
    # any green genes in panels v1.0 and higher, in which the mode of inheritance of the gene has changed
    df1 = pd.read_sql_query("SELECT DISTINCT panel_name, panel_id, gene_symbol, moi, version_num FROM panelapp_info WHERE Datestamp LIKE '2017-07-10%' AND version_num >=1", conn)
    df2 = pd.read_sql_query("SELECT DISTINCT panel_name, panel_id, gene_symbol, moi, version_num FROM panelapp_info WHERE Datestamp LIKE '2017-07-17%' AND gene_status = 'Green'", conn)
    print("MOI changed genes: ")
    moi_change_df = pd.merge(df1, df2, on=['Panel_ID','Gene_Symbol'], how='inner')
    moi_change_df['MOI_x'].fillna(value='NaN', inplace=True)
    moi_change_df['MOI_y'].fillna(value='NaN', inplace=True)
    moi_change_df = moi_change_df[moi_change_df.MOI_x != moi_change_df.MOI_y]
    moi_change_df = moi_change_df.drop('Panel_Name_y',1)
    moi_change_df = moi_change_df.rename(columns={'Version_Num_x':'Prev_Version_Num','Panel_Name_x':'Panel_Name','Version_Num_y':'Curr_Version_Num','MOI_x':'Prev_MOI','MOI_y':'Curr_MOI'})
    moi_change_df.to_excel(writer, 'MOI changed',index=False)
    print(moi_change_df)

'''
def update_data():
    # N.B. *** N.B. Data amended in SQLite database cannot be restored!***
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

    cur.execute("DELETE FROM panelapp_info WHERE Datestamp LIKE '2017-07-10 15:%'")
    conn.commit()

    cur.execute("SELECT DISTINCT Datestamp from panelapp_info")
    data = cur.fetchall()
    for row in data:
        print(row)
'''

new_panels()
del_panels()
promoted_panels()
new_genes()
#del_genes()
promoted_genes()
demoted_genes()
moi_change()
# update_data()
# delete_data()

writer.save()

# Add a step to copy existing database into a back-up folder?

cur.close()
conn.close()


"""
Title: panels_comparison.py
Version:
Release Date:  
Author: VFryer
The following code compares data from two datasets (different timestamps) to generate Excel spreadsheet scontainngthe details of comparisons.
Usage: python panels_comparison.py <output file location>
"""

import requests, csv, datetime, sys, os
import sqlite3, time, pandas as pd

# create a connection to the specified SQLite database
conn = sqlite3.connect("outputs/PanelApp_Data_test.db")
cur = conn.cursor()

# retrieve all timestamps for data withoin the database and rpint to command line to allow user to select which data to compare
cur.execute("SELECT DISTINCT Datestamp FROM panelapp_info")
data = cur.fetchall()
print("Data is available for the following dates:\n")
for row in data:
    print(row)
print('\n')

prev_version = input("Enter date of current PanelApp data capture in format yyyy-mm-dd:\n")
#prev_version = "2017-05-23"
curr_version = input("\nEnter data or previous PanelApp data capture in format yyyy-mm-dd:\n")
#curr_version = "2017-07-10"


# save today's date to use in the filename to record a snapshot of panel versions on a weekly basis
todays_date = datetime.datetime.now().strftime("%Y%m%d")
datestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#try:
#    cur.execute(
#        "CREATE TABLE IF NOT EXISTS panelapp_info (Datestamp TEXT,Panel_Name TEXT,Panel_ID TEXT,Version_Num TEXT,Gene_Symbol TEXT,Gene_Status TEXT,MOI TEXT)")
#except:
#    print("Cannot create table. It may already exist. Program will now end.")
#    sys.exit()

out_path = sys.argv[1]

filename = os.path.join(out_path, 'panels_genes_comp_' + todays_date + '.csv')

writer = pd.ExcelWriter('panels_genes_comp_' + prev_version + '_to_' + curr_version + '.xlsx')

def new_v1_panels():
    # any current v1+ panels that exist in latest panel version capture that did not exist in the previous panel capture
    cur.execute("SELECT DISTINCT panel_name, panel_id, version_num FROM panelapp_info WHERE Datestamp LIKE ? AND version_num >=1 AND panel_name NOT IN(SELECT panel_name FROM panelapp_info WHERE Datestamp LIKE ?)",(curr_version+'%',prev_version+'%'))
    data = cur.fetchall()
    # print("New v1 panels: ")
    new_v1_panels_df = pd.DataFrame(data, columns=['Panel Name','Panel_ID','Version_Num'])
    new_v1_panels_df.to_excel(writer, 'New v1 panels', index=False)

def new_v0_panels():
    # any current v0 panels that exist in latest panel version capture that did not exist in the previous panel capture
    cur.execute("SELECT DISTINCT panel_name, panel_id, version_num FROM panelapp_info WHERE Datestamp LIKE ? AND version_num <1 AND panel_name NOT IN(SELECT panel_name FROM panelapp_info WHERE Datestamp LIKE ?)",(curr_version+'%',prev_version+'%'))
    data = cur.fetchall()
    new_v0_panels_df = pd.DataFrame(data, columns=['Panel Name','Panel_ID','Version_Num'])
    new_v0_panels_df.to_excel(writer, 'New v0 panels', index=False)

def del_panels():
    # any panels that do not exist in latest panel version capture vs. previous panel capture
    cur.execute("SELECT DISTINCT panel_name, panel_id, version_num FROM panelapp_info WHERE Datestamp LIKE ? AND panel_name NOT IN(SELECT panel_name FROM panelapp_info WHERE Datestamp LIKE ?)",(prev_version+'%',curr_version+'%'))
    data = cur.fetchall()
    # print("Retired panels: ")
    del_panels_df = pd.DataFrame(data, columns=['Panel_Name', 'Panel_ID', 'Version_Num'])
    del_panels_df.to_excel(writer, 'Retired panels',index=False)
    # print(del_panels_df)

def promoted_panels():
    # any panels that have been promoted to v1.0 or higher from less than v1.0
    #df1 = pd.read_sql_query("SELECT DISTINCT panel_name, panel_id, version_num FROM panelapp_info WHERE Datestamp LIKE '2017-05-23%' AND version_num <1", conn)
    cur.execute("SELECT DISTINCT panel_name, panel_id, version_num FROM panelapp_info WHERE Datestamp LIKE ? AND version_num <1",(prev_version+'%', ))
    data = cur.fetchall()
    df1 = pd.DataFrame(data, columns=['Panel_Name','Panel_ID','Version_Num'])
    #df2 = pd.read_sql_query("SELECT DISTINCT panel_name, panel_id, version_num FROM panelapp_info WHERE Datestamp LIKE '2017-07-10%' AND version_num >=1", conn)
    cur.execute("SELECT DISTINCT panel_name, panel_id, version_num FROM panelapp_info WHERE Datestamp LIKE ? AND version_num >1",(curr_version+'%', ))
    data = cur.fetchall()
    df2 = pd.DataFrame(data, columns=['Panel_Name','Panel_ID','Version_Num'])
    # print("Promoted panels: ")
    prom_panel_df = pd.merge(df1, df2, on='Panel_ID', how='inner')
    prom_panel_df = prom_panel_df.drop('Panel_Name_y',1)
    prom_panel_df = prom_panel_df.rename(columns={'Version_Num_x':'Prev_Version_Num','Panel_Name_x':'Panel_Name','Version_Num_y':'Curr_Version_Num'})
    prom_panel_df.to_excel(writer, 'Promoted Panels',index=False)
    # print(prom_panel_df)

def updated_v1_panels():
    # any panels previously v1+ that have been updated to a new version
    #df1 = pd.read_sql_query("SELECT DISTINCT panel_name, panel_id, version_num FROM panelapp_info WHERE Datestamp LIKE '2017-05-23%' AND version_num >=1", conn)
    cur.execute("SELECT DISTINCT panel_name, panel_id, version_num FROM panelapp_info WHERE Datestamp LIKE ? AND version_num >=1",(prev_version+'%', ))
    data = cur.fetchall()
    df1 = pd.DataFrame(data, columns=['Panel_Name','Panel_ID','Version_Num'])
    #df2 = pd.read_sql_query("SELECT DISTINCT panel_name, panel_id, version_num FROM panelapp_info WHERE Datestamp LIKE '2017-07-10%' AND version_num >=1", conn)
    cur.execute("SELECT DISTINCT panel_name, panel_id, version_num FROM panelapp_info WHERE Datestamp LIKE ? AND version_num >=1",(curr_version+'%', ))
    data = cur.fetchall()
    df2 = pd.DataFrame(data, columns=['Panel_Name','Panel_ID','Version_Num'])
    # print("Updated v1 panels: ")
    up_v1_df = pd.merge(df1, df2, on='Panel_ID', how='inner')
    up_v1_df = up_v1_df.drop('Panel_Name_y',1)
    up_v1_df = up_v1_df[up_v1_df.Version_Num_x != up_v1_df.Version_Num_y]
    up_v1_df = up_v1_df.rename(columns={'Version_Num_x':'Prev_Version_Num','Panel_Name_x':'Panel_Name','Version_Num_y':'Curr_Version_Num'})
    up_v1_df.to_excel(writer, 'Updated v1 Panels',index=False)
    # print(up_v1_df)
    

def updated_v0_panels():
    # any panels previously < v1 that have been updated to a new version that is still <v1
    #df1 = pd.read_sql_query("SELECT DISTINCT panel_name, panel_id, version_num FROM panelapp_info WHERE Datestamp LIKE '2017-05-23%' AND version_num <1", conn)
    cur.execute("SELECT DISTINCT panel_name, panel_id, version_num FROM panelapp_info WHERE Datestamp LIKE ? AND version_num <1",(prev_version+'%', ))
    data = cur.fetchall()
    df1 = pd.DataFrame(data, columns=['Panel_Name','Panel_ID','Version_Num'])
    #df2 = pd.read_sql_query("SELECT DISTINCT panel_name, panel_id, version_num FROM panelapp_info WHERE Datestamp LIKE '2017-07-10%' AND version_num <1", conn)
    cur.execute("SELECT DISTINCT panel_name, panel_id, version_num FROM panelapp_info WHERE Datestamp LIKE ? AND version_num <1",(curr_version+'%', ))
    data = cur.fetchall()
    df2 = pd.DataFrame(data, columns=['Panel_Name','Panel_ID','Version_Num'])
    # print("Updated v0 panels: ")
    up_v0_df = pd.merge(df1, df2, on='Panel_ID', how='inner')
    up_v0_df = up_v0_df.drop('Panel_Name_y',1)
    up_v0_df = up_v0_df[up_v0_df.Version_Num_x != up_v0_df.Version_Num_y]
    up_v0_df = up_v0_df.rename(columns={'Version_Num_x':'Prev_Version_Num','Panel_Name_x':'Panel_Name','Version_Num_y':'Curr_Version_Num'})
    up_v0_df.to_excel(writer, 'Updated v0 Panels',index=False)
    # print(up_v0_df)


def name_changed_panels():
    # any panels with a different name (but same panel ID) to previous panel version
    #df1 = pd.read_sql_query("SELECT DISTINCT panel_name, panel_id, version_num FROM panelapp_info WHERE Datestamp LIKE '2017-05-23%'", conn)
    cur.execute("SELECT DISTINCT panel_name, panel_id, version_num FROM panelapp_info WHERE Datestamp LIKE ?",(prev_version+'%', ))
    data = cur.fetchall()
    df1 = pd.DataFrame(data, columns=['Panel_Name','Panel_ID','Version_Num'])
    #df2 = pd.read_sql_query("SELECT DISTINCT panel_name, panel_id, version_num FROM panelapp_info WHERE Datestamp LIKE '2017-07-10%'", conn)
    cur.execute("SELECT DISTINCT panel_name, panel_id, version_num FROM panelapp_info WHERE Datestamp LIKE ?",(curr_version+'%', ))
    data = cur.fetchall()
    df2 = pd.DataFrame(data, columns=['Panel_Name','Panel_ID','Version_Num'])
    # print("Name changed panels: ")
    name_change_df = pd.merge(df1, df2, on='Panel_ID', how='inner')
    name_change_df = name_change_df[name_change_df.Panel_Name_x != name_change_df.Panel_Name_y]
    name_change_df = name_change_df.rename(columns={'Panel_Name_x':'Prev_Panel_Name','Panel_Name_y':'Curr_Panel_Name','Version_Num_x':'Prev_Version_Num','Version_Num_y':'Curr_Version_Num'})
    name_change_df.to_excel(writer, 'Name Changed Panels',index=False)
    # print(name_change_df)


#def review_required():
    # any panels that require review (lower than v1 but 'approved' and live in PanelApp


def new_genes():
    # any genes that have been added to any v1+ panels with status of 'green' that were not in previous panels
    cur.execute("SELECT DISTINCT panel_name, gene_symbol, gene_status, version_num FROM panelapp_info WHERE Datestamp LIKE ? AND gene_status = 'Green' AND version_num >=1 AND panel_name NOT IN(SELECT panel_name FROM panelapp_info WHERE Datestamp LIKE ?)",(curr_version+'%',prev_version+'%'))
    data = cur.fetchall()
    # print("New genes: ")
    new_genes_df = pd.DataFrame(data, columns = ['Panel_Name','Gene_Symbol', 'Gene_Status','Version_Num'])
    new_genes_df.to_excel(writer, 'New genes', index=False)
    # print(new_genes_df)

def del_genes():
    # any 'green' genes that have been removed from any v1+ panels
    cur.execute("SELECT DISTINCT panel_name, gene_symbol, gene_status, version_num FROM panelapp_info WHERE Datestamp LIKE ? AND gene_status = 'Green' AND version_num >=1 AND panel_name NOT IN(SELECT panel_name FROM panelapp_info WHERE Datestamp LIKE ?)",(prev_version+'%',curr_version+'%'))
    data = cur.fetchall()
    # print("Retired genes: ")
    del_genes_df = pd.DataFrame(data, columns = ['Panel_Name','Gene_Symbol', 'Gene_Status','Version_Num'])
    del_genes_df.to_excel(writer, 'Retired genes', index=False)
    # print(del_genes_df)

def promoted_genes():
    # any genes within v1.0+ panels that are currently 'green' that were previously not 'green'
    #df1 = pd.read_sql_query("SELECT DISTINCT panel_name, panel_id, gene_symbol, gene_status, version_num FROM panelapp_info WHERE Datestamp LIKE '2017-05-23%' AND gene_status != 'Green'", conn)
    cur.execute("SELECT DISTINCT panel_name, panel_id, gene_symbol, gene_status, version_num FROM panelapp_info WHERE Datestamp LIKE ? AND gene_status != 'Green'",(prev_version+'%', ))
    data = cur.fetchall()
    df1 = pd.DataFrame(data, columns=['Panel_Name','Panel_ID','Gene_Name','Status','Version_Num'])
    #df2 = pd.read_sql_query("SELECT DISTINCT panel_name, panel_id, gene_symbol, gene_status, version_num FROM panelapp_info WHERE Datestamp LIKE '2017-07-10%' AND gene_status = 'Green' AND version_num >=1", conn)
    cur.execute("SELECT DISTINCT panel_name, panel_id, gene_symbol, gene_status, version_num FROM panelapp_info WHERE Datestamp LIKE ? AND gene_status = 'Green'",(curr_version+'%', ))
    data = cur.fetchall()
    df2 = pd.DataFrame(data, columns=['Panel_Name','Panel_ID','Gene_Name','Status','Version_Num'])
    # print("Promoted genes: ")
    promoted_df = pd.merge(df1, df2, on=['Panel_ID','Gene_Name'], how='inner')
    promoted_df = promoted_df.drop('Panel_Name_y',1)
    promoted_df = promoted_df.rename(columns={'Version_Num_x':'Prev_Version_Num','Panel_Name_x':'Panel_Name','Version_Num_y':'Curr_Version_Num','Gene_Status_x':'Prev_Gene_Status','Gene_Status_y':'Curr_Gene_Status'})
    promoted_df.to_excel(writer, 'Promoted Genes',index=False)
    # print(promoted_df)

def demoted_genes():
    # any genes in panels v1.0 and higher, where gene was previously rated 'Green' but is no longer rated as 'Green'
    #df1 = pd.read_sql_query("SELECT DISTINCT panel_name, panel_id, gene_symbol, gene_status, version_num FROM panelapp_info WHERE Datestamp LIKE '2017-05-23%' AND gene_status = 'Green' AND version_num >=1", conn)
    cur.execute("SELECT DISTINCT panel_name, panel_id, gene_symbol, gene_status, version_num FROM panelapp_info WHERE Datestamp LIKE ? AND gene_status = 'Green' AND version_num >=1",(prev_version+'%', ))
    data = cur.fetchall()
    df1 = pd.DataFrame(data, columns=['Panel_Name','Panel_ID','Gene_Name','Status','Version_Num'])

    #df2 = pd.read_sql_query("SELECT DISTINCT panel_name, panel_id, gene_symbol, gene_status, version_num FROM panelapp_info WHERE Datestamp LIKE '2017-07-10%' AND gene_status != 'Green'", conn)
    cur.execute("SELECT DISTINCT panel_name, panel_id, gene_symbol, gene_status, version_num FROM panelapp_info WHERE Datestamp LIKE ? AND gene_status != 'Green'",(curr_version+'%', ))
    data = cur.fetchall()
    df2 = pd.DataFrame(data, columns=['Panel_Name','Panel_ID','Gene_Name','Status','Version_Num'])

    # print("Demoted genes: ")
    demoted_df = pd.merge(df1, df2, on=['Panel_ID','Gene_Name'], how='inner')
    demoted_df = demoted_df.drop('Panel_Name_y',1)
    demoted_df = demoted_df.rename(columns={'Version_Num_x':'Prev_Version_Num','Panel_Name_x':'Panel_Name','Version_Num_y':'Curr_Version_Num','Gene_Status_x':'Prev_Gene_Status','Gene_Status_y':'Curr_Gene_Status'})
    demoted_df.to_excel(writer, 'Demoted genes', index=False)
    # print(demoted_df)

def moi_change():
    # any green genes in panels v1.0 and higher, in which the mode of inheritance of the gene has changed
    #df1 = pd.read_sql_query("SELECT DISTINCT panel_name, panel_id, gene_symbol, moi, version_num FROM panelapp_info WHERE Datestamp LIKE '2017-05-23%' AND version_num >=1", conn)
    cur.execute("SELECT DISTINCT panel_name, panel_id, gene_symbol, moi, version_num FROM panelapp_info WHERE Datestamp LIKE ? AND version_num >=1",(prev_version+'%', ))
    data = cur.fetchall()
    df1 = pd.DataFrame(data, columns=['Panel_Name','Panel_ID','Gene_Name','MOI','Version_Num'])

    #df2 = pd.read_sql_query("SELECT DISTINCT panel_name, panel_id, gene_symbol, moi, version_num FROM panelapp_info WHERE Datestamp LIKE '2017-07-10%' AND gene_status = 'Green'", conn)
    cur.execute("SELECT DISTINCT panel_name, panel_id, gene_symbol, moi, version_num FROM panelapp_info WHERE Datestamp LIKE ? AND gene_status = 'Green'",(curr_version+'%', ))
    data = cur.fetchall()
    df2 = pd.DataFrame(data, columns=['Panel_Name','Panel_ID','Gene_Name','MOI','Version_Num'])

    # print("MOI changed genes: ")
    moi_change_df = pd.merge(df1, df2, on=['Panel_ID','Gene_Name'], how='inner')
    moi_change_df['MOI_x'].fillna(value='NaN', inplace=True)
    moi_change_df['MOI_y'].fillna(value='NaN', inplace=True)
    moi_change_df = moi_change_df[moi_change_df.MOI_x != moi_change_df.MOI_y]
    moi_change_df = moi_change_df.drop('Panel_Name_y',1)
    moi_change_df = moi_change_df.rename(columns={'Version_Num_x':'Prev_Version_Num','Panel_Name_x':'Panel_Name','Version_Num_y':'Curr_Version_Num','MOI_x':'Prev_MOI','MOI_y':'Curr_MOI'})
    moi_change_df.to_excel(writer, 'MOI changed',index=False)
    # print(moi_change_df)

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

    cur.execute("DELETE FROM panelapp_info WHERE Datestamp LIKE '2017-07-10 16%'")
    conn.commit()

'''

new_v1_panels()
new_v0_panels()
del_panels()
promoted_panels()
updated_v0_panels()
updated_v1_panels()
name_changed_panels()
#review_required()
new_genes()
del_genes()
promoted_genes()
demoted_genes()
moi_change()
# update_data()
# delete_data()

writer.save()
print("\nComparison data is now available in \\outputs")

# Add a step to copy existing database into a back-up folder?

cur.close()
conn.close()


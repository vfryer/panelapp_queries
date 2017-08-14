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
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

# create a connection to the specified SQLite database
conn = sqlite3.connect("outputs/PanelApp_Data_test.db")
cur = conn.cursor()

# save today's date to use in the filename to record a snapshot of panel versions on a weekly basis
todays_date = datetime.datetime.now().strftime("%Y-%m-%d")
datestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#try:
#    cur.execute(
#        "CREATE TABLE IF NOT EXISTS panelapp_info (Datestamp TEXT,Panel_Name TEXT,Panel_ID TEXT,Version_Num TEXT,Gene_Symbol TEXT,Gene_Status TEXT,MOI TEXT)")
#except:
#    print("Cannot create table. It may already exist. Program will now end.")
#    sys.exit()

out_path = sys.argv[1]
'''
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

        red_count = 0
        amber_count = 0
        green_count = 0
        nolist_count = 0

        # get all genes and their status
        for gene in gene_info:
            gene_symbol = gene["GeneSymbol"]
            gene_confidence = gene["LevelOfConfidence"]
            #gene_evidence = gene["Evidences"]
            moi = gene["ModeOfInheritance"]
            #print(gene_symbol,gene_confidence)
            if gene_confidence == "LowEvidence":
            #if "Expert Review Red" in gene_evidence:
                gene_status = "Red"
                red_count +=1
                #print(gene_status)
            elif gene_confidence == "HighEvidence":
                gene_status = "Green"
                green_count +=1
                #print(gene_status)
            elif gene_confidence == "ModerateEvidence":
                gene_status = "Amber"
                amber_count +=1
                #print(gene_status)
            else:
                gene_status = "No List"
                nolist_count +=1
                #print(gene_status)

            # print(datestamp,panel_name,panel_id,version_num,gene_symbol,gene_status,moi)
            # write data retrieved into a .csv to be archived and saved for future reference
            row = [panel_name, panel_id, version_num, gene_symbol, gene_status, datestamp, moi]
            writer.writerow(row)

            # write data to database for subsequent analysis
            cur.execute("INSERT INTO panelapp_info VALUES (?,?,?,?,?,?,?)",(datestamp,panel_name,panel_id,version_num,gene_symbol,gene_status,moi))
            conn.commit()

        #print("Red: " + str(red_count) + " Green: " + str(green_count) + " Amber: " + str(amber_count) + " No List: " + str(unknown_count))   
        # Open table in database to store gene_status totals
        try:
            cur.execute("CREATE TABLE IF NOT EXISTS gene_status_summary (Date TEXT,Panel_Name TEXT,Green_Count INTEGER,Amber_Count INTEGER,Red_Count INTEGER,No_List_Count INTEGER)")
        except:
            print("Cannot create table. It may already exist. Program will now end.")
            sys.exit()

        cur.execute("INSERT INTO gene_status_summary VALUES (?,?,?,?,?,?)",(todays_date,panel_name,green_count,amber_count,red_count,nolist_count))
        conn.commit()
        
    except:
        # if the try loop fails for any reason, inform user
        print("Panel not found")

print(str(panel_count) + " panels counted")
'''
# create a dataframe of all months values form  database table
df = pd.read_sql_query("SELECT * FROM gene_status_summary", conn)

# amend the dataframe for graph
df = df.set_index('Panel_Name')
df=df.drop('No_List_Count',1) # to be added once no list items can be counted
#df=df.astype(int) # change dtypes to ints instead of objects
#print(df)

colours = {'Red':'red','Amber':'yellow','Green':'green','No List':'blue'}

ax = df.plot(kind='barh',stacked=True, title='Gene status per panel', legend=True, colormap='brg',figsize=(12,30))
ax.set_xlabel("Number of genes")
ax.tick_params(axis ='x',width=(40))
ax.set_ylabel("Panel name")
fig = ax.get_figure()
fig.tight_layout() # ensure all panel names are printed in full on the axis
fig.savefig(out_path + 'gene_status_summary.png')

cur.close()
conn.close()


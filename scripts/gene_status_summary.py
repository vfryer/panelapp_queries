"""
Title: gene_status_summary.py
Author: VFryer
The following code retrieves all panel names from PanelApp, with current panel versions, gene symbols, gene status and mode of inheritance (MOI).
All captured data is exported into an SQLite database and a .csv (back-up for SQLite).
User specifies the location of the back-up .csv file(outputs/archive recommended) in the command line.
The virtual environment must be activated before running this script (source bin/activate).
Usage: python scripts/gene_status_summary.py <output file location>
"""

import requests, json, csv, datetime, sys, os
import sqlite3, time, pandas as pd
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

# create a connection to the specified SQLite database
conn = sqlite3.connect("outputs/PanelApp_Data.db")
cur = conn.cursor()

# save today's date to use in the filename to record a snapshot of panel versions on a weekly basis
todays_date = datetime.datetime.now().strftime("%Y-%m-%d")
datestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
datestamp_spl = datestamp.split(' ')

#try:
#    cur.execute(
#        "CREATE TABLE IF NOT EXISTS panelapp_info (Datestamp TEXT,Panel_Name TEXT,Panel_ID TEXT,Version_Num TEXT,Gene_Symbol TEXT,Gene_Status TEXT,MOI TEXT)")
#except:
#    print("Cannot create table. It may already exist. Program will now end.")
#    sys.exit()

out_path = sys.argv[1]

# retrieve a list of all panel names
#r = requests.get('https://bioinfo.extge.co.uk/crowdsourcing/WebServices/list_panels')
r = requests.get('https://panelapp.genomicsengland.co.uk/WebServices/list_panels')
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
        #url = 'https://bioinfo.extge.co.uk/crowdsourcing/WebServices/get_panel/' + panel_id + '/?version=' + version_num
        url = 'https://panelapp.genomicsengland.co.uk/WebServices/get_panel/' + panel_id + '/?version=' + version_num
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

# create a dataframe of all months values from database table
cur.execute("SELECT Panel_Name, Green_Count, Amber_Count,Red_Count FROM gene_status_summary WHERE Date LIKE ?",(datestamp_spl[0]+'%',))
data = cur.fetchall()
df = pd.DataFrame(data, columns=['Panel_Name','Green_Count','Amber_Count','Red_Count'])

# amend the dataframe for graph by setting panel name as index, sort alphabetically
df = df.set_index('Panel_Name').sort_index(ascending=False)
#df = df.drop('No_List_Count',1) # to be added once no list items can be counted

#colours = ['royalblue'] add 4th colour when no_list genes are counted
# set colours for bars in barchart, these will cycle through three data points at a time
colours = ['seagreen','gold','firebrick']

# plot a stacked bar horizontal bar chart with a legend, set title, axes title and chart size
ax = df.plot(kind='barh',stacked=True, legend=True, color=colours,figsize=(30,30))
ax.set_title('Gene status per panel', fontsize = 30)
ax.legend(fontsize=30)
ax.set_xlabel("Number of genes", fontsize = 30)
#plt.xticks(rotation=90)
ax.tick_params(axis ='x',width=(40))
ax.set_ylabel("Panel name", fontsize = 30)
# add gridlines to barchart
ax.xaxis.grid(which='major', linewidth=1)
#plt.minorticks_on()
ax.xaxis.grid(which='minor', linewidth=0.5)
fig = ax.get_figure()
fig.tight_layout() # ensure all panel names are printed in full on the axis
fig.savefig(out_path + 'gene_status_summary_' + todays_date + '.png')

'''
def delete_data():
    # ***N.B. data deleted from SQLite DB cannot be restored!***
    #data may need to be deleted if this scrpt is run more than once on the same day as all data with the same Date will be plotted
    cur.execute("SELECT DISTINCT Datestamp from panelapp_info")
    data = cur.fetchall()
    for row in data:
        print(row)

    cur.execute("DELETE FROM panelapp_info WHERE Datestamp LIKE '2018-05-31 17%'")
    conn.commit()

delete_data()
'''

cur.close()
conn.close()


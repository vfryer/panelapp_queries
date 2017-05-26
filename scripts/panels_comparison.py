"""
Ttle: panels_comparison.py
Version: v1.0
Release Date: 26/05/2017
Author: VFryer
This program compares the current and previous Excel spreadsheets and outputs another spreadsheet.
This lists the existing, obsolete and new panels since the last version of panels was saved.
"""

import pandas as pd
import datetime

todays_date = datetime.datetime.now().strftime("%Y%m%d")

# open the file
prev_panels = pd.read_excel(r"C:\Users\Verity Fryer\PyCharmProjects\panelapp_queries\outputs\panel_versions_list_20170523_test.xlsx")
curr_panels = pd.read_excel(r"C:\Users\Verity Fryer\PyCharmProjects\panelapp_queries\outputs\panel_versions_list_20170525_test.xlsx")

df_inner = pd.merge(curr_panels,prev_panels,on=['Panel Id'], how='inner')
df_inner = df_inner.drop(['Panel Name_y'],axis=1)
print(df_inner)

df_left_if_null = pd.merge(curr_panels,prev_panels,on=['Panel Id'], how='left')
df_left_if_null = df_left_if_null[df_left_if_null['Panel Name_y'].isnull()]
df_left_if_null = df_left_if_null.drop(['Panel Name_y','Version Number_y'],axis=1)
print(df_left_if_null)

df_right_if_null = pd.merge(curr_panels,prev_panels,on=['Panel Id'], how='right')
df_right_if_null = df_right_if_null[df_right_if_null['Panel Name_x'].isnull()]
df_right_if_null = df_right_if_null.drop(['Panel Name_x','Version Number_x'],axis=1)
print(df_right_if_null)

writer = pd.ExcelWriter('output_' + todays_date + '.xlsx')
df_inner.to_excel(writer,'Existing panels')
df_left_if_null.to_excel(writer,'Obsolete panels')
df_right_if_null.to_excel(writer,'New panels')
writer.save()


"""
The following code retrieves the name of each panel in PanelApp, the number of genes in each panel, and the status of each gene within that panel ('Green', 'Amber' or 'Red') 
"""

import requests, json, xlsxwriter, datetime

todays_date = datetime.datetime.now().strftime("%Y%m%d")

# Create an Excel spreadsheet ready to be populated with data
workbook = xlsxwriter.Workbook('panels_status_'+ todays_date + '.xlsx')
worksheet1 = workbook.add_worksheet('Panels')
worksheet2 = workbook.add_worksheet('Genes')
# Add a bold format to use to highlight cells.
bold = workbook.add_format({'bold': True})

# Add some data headers.
worksheet1.write('A1', 'Panel Name', bold)
worksheet1.write('B1', 'Version Number', bold)
worksheet1.write('C1', 'Total Genes', bold)
worksheet1.write('D1', 'Green Genes', bold)
worksheet1.write('E1', 'Amber Genes', bold)
worksheet1.write('F1', 'Red Genes', bold)
worksheet1.write('G1', 'Unknown Genes', bold)

worksheet2.write('A1', 'Panel Name', bold)
worksheet2.write('B1', 'Gene Name', bold)
worksheet2.write('C1', 'Gene Status', bold)

# Header of Excel file is row 0, start adding information to Excel at row 1.
# Columns will start at column 0
row = 1
row2 = 1
col = 0

# iterate through the list of dictionaries, retrieving panel name, panel version, panel id (to be used to search each panel) and the number of genes per panel
comp_file = pd.read_excel(r"C:\Users\Verity Fryer\PyCharmProjects\panelapp_queries\scripts\output_20170526.xlsx",sheetname='Existing panels', index_col=1)

for row in comp_file.iterrows():
    panel_id = row(['Panel Id'])
    print(panel_id)
    version_num = row(['Version Number'])
    print(version_num)
    try:
        get_panel_version = requests.get('https://bioinfo.extge.co.uk/crowdsourcing/WebServices/get_panel/' + panel_id + '/?version=' + str(
                version_num))
        version_data = get_panel_version.json()
        print(version_data)
        # print(panel_name + ' v' + str(version_num))

        gene_info = version_data['result']['Genes']

        panel_name = item["Name"]
        panel_version = item["CurrentVersion"]
        panel_id = item["Panel_Id"]
        panel_total_genes = item["Number_of_Genes"]

        gene_info = version_data['result']['Genes']

        # as the genes will be counted during iteration, set all counters to 0
        green_count = 0
        red_count = 0
        amber_count = 0
        unknown_count = 0
        # retrieve gene and gene status information for all genes within the panel

        for gene in gene_info:
            gene_symbol = gene['GeneSymbol']
            gene_confidence = gene['LevelOfConfidence']
            # print(gene_symbol, gene_confidence)
            if gene_confidence == "LowEvidence":
                gene_status = "Red"
                red_count = red_count + 1
            elif gene_confidence == "HighEvidence":
                gene_status = "Green"
                green_count = green_count + 1
            elif gene_confidence == "ModerateEvidence":
                gene_status = "Amber"
                amber_count = amber_count + 1
            else:
                gene_status = "Unknown"
                unknown_count = unknown_count + 1

            worksheet2.write(row2, col, panel_name)
            worksheet2.write(row2, col+1, gene_symbol)
            worksheet2.write(row2, col+2, gene_status)
            row2 = row2+1

        panel_count = panel_count + 1

        if panel_total_genes == None:
            panel_total_genes = 0
        else:
            pass
        print(panel_name + " v" + panel_version)  # + " Total genes: " + str(panel_total_genes))
#  handle non-retrieval of data from endpoint
    except:
        print(panel_id + " panel could not be found in PanelApp.")

#    calculated_gene_tot = (green_count + red_count + amber_count + unknown_count)

    worksheet1.write(row, col, panel_name)
    worksheet1.write(row, col+1, panel_version)
    worksheet1.write(row, col+2, panel_total_genes)
    worksheet1.write(row, col+3, green_count)
    worksheet1.write(row, col+4, amber_count)
    worksheet1.write(row, col+5, red_count)
    worksheet1.write(row, col+6, unknown_count)
    row = row+1

# print("Green genes: " + str(green_count) + "\nRed genes: " + str(red_count) + "\nAmber genes: " + str(amber_count) + "\nUnknown genes: " + str(unknown_count))
# print("Calculated gene total: " +str(calculated_gene_tot))

'''
To check that all genes are being captured, compare total number of genes for a panel
calculated by adding together all the green, amber, red and unknown genes)
against the number of genes associated with the panel.

    if panel_total_genes == None and calculated_gene_tot == 0:
        pass
    elif calculated_gene_tot != panel_total_genes:
        print(panel_name + " v" + panel_version + " Total genes: " + str(panel_total_genes))
        print("Genes totals don't match!")
        print("Green genes: " + str(green_count) + "\nRed genes: " + str(red_count) + "\nAmber genes: " + str(
            amber_count) + "\nUnknown genes: " + str(unknown_count))
        print("Calculated gene total: " + str(calculated_gene_tot))
    else:
        pass
'''

workbook.close()

# Print the number of panels to signal the end of the script and the number of rows to be expected in the Excel file
print("Number of panels: " + str(len(panel_list)))

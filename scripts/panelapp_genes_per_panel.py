"""
The following code retrieves the name of each panel in PanelApp, the number of genes in each panel, and the status of each gene within that panel ('Green', 'Amber' or 'Red') 
"""

import requests, json, xlsxwriter, datetime

todays_date = datetime.datetime.now().strftime("%Y%m%d")
# print(todays_date)

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

# Get a list of all panel names currently in PanelApp using list_panels endpoint to get the data in json format.
# Store the data in memory as a list of dictionaries (the current JSON format contains a dictionary of a list of dictionaries)

# Retrieve a list of all current panels in PanelApp
r = requests.get('https://bioinfo.extge.co.uk/crowdsourcing/WebServices/list_panels')
panel_data = r.json()
panel_list = panel_data["result"]
# print(panel_list)

# Header of Excel file is rwow 0, start adding information to Excel at row 1.
# Columns will start at column 0
row = 1
row2 = 1
col = 0


# iterate through the list of dictionaries, retrieving panel name, panel version, panel id (to be used to search each panel) and the number of genes per panel
for item in panel_list:
    panel_name = item["Name"]
    panel_version = item["CurrentVersion"]
    panel_id = item["Panel_Id"]
    panel_total_genes = item["Number_of_Genes"]
    if panel_total_genes == None:
        panel_total_genes = 0
    else:
        pass
    print(panel_name + " v" + panel_version) # + " Total genes: " + str(panel_total_genes))

# handle non-retrieval of data from endpoint
    try:
        panel_request = requests.get('https://bioinfo.extge.co.uk/crowdsourcing/WebServices/get_panel/' + panel_id)
        panel_data = panel_request.json()
#       print(panel_data)
    except:
        print(panel_id + panel_name + " panel could not be found in PanelApp.")

# specify the list within a dictionary to retrieve gene information
    gene_info = panel_data['result']['Genes']
#    print(gene_info)

# as the genes will be counted during iteration, set all counters to 0
    green_count = 0
    red_count = 0
    amber_count = 0
    unknown_count = 0

# get all genes and their status
    for gene in gene_info:
        gene_symbol = gene["GeneSymbol"]
        gene_confidence = gene["LevelOfConfidence"]
        # print(gene_symbol, gene_confidence)
        if gene_confidence == "LowEvidence":
            gene_status = "Red"
            red_count = red_count+1
        elif gene_confidence == "HighEvidence":
            gene_status = "Green"
            green_count = green_count+1
        elif gene_confidence == "ModerateEvidence":
            gene_status = "Amber"
            amber_count = amber_count+1
        else:
            gene_status = "Unknown"
            unknown_count = unknown_count+1
        # print(gene_symbol, gene_status)
        worksheet2.write(row2, col, panel_name)
        worksheet2.write(row2, col+1, gene_symbol)
        worksheet2.write(row2, col+2, gene_status)
        row2 = row2+1


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
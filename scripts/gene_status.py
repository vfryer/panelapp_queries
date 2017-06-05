# for a version of a panel

import json, requests, datetime, xlsxwriter, pandas as pd

# if this were to be another function calling from an earlier function then previous variables would need to be captured
# panel_id = get_panel_id()
# version_num = get_version_num()

todays_date = datetime.datetime.now().strftime("%Y%m%d")
# print(todays_date)

workbook = xlsxwriter.Workbook('gene_status_' + todays_date + '.xlsx')
worksheet = workbook.add_worksheet()

row = 0
col = 0

worksheet.write(row, col, 'Panel Name')
worksheet.write(row, col + 1, 'Panel Version')
worksheet.write(row, col + 2, 'Total Genes')
worksheet.write(row, col + 3, 'Green Genes')
worksheet.write(row, col + 4, 'Amber Genes')
worksheet.write(row, col + 5, 'Red Genes')
worksheet.write(row, col + 6, 'Unknown Genes')

row = 1

# provide a list of panels with version numbers

panel_list = pd.read_excel('panel_versions_list_20170605.xlsx')

for panel in panel_list:

    panel_name = str(panel_list.Name)
    print(panel_name) 
    panel_version = str(panel_list.Version)    
    print(panel_version)
'''
    panel_request = requests.get('https://bioinfo.extge.co.uk/crowdsourcing/WebServices/get_panel/' + panel_name + '/?version=' + panel_version)
    panel_data = panel_request.json
    print(panel_data)

    # retrieve gene name and status for each version
    gene_info = panel_data
    row +1

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

#    calculated_gene_tot = (green_count + red_count + amber_count + unknown_count)
    worksheet.write(row, col, panel_name)
    worksheet.write(row, col+1, panel_version)
    worksheet.write(row, col+2, panel_total_genes)
    worksheet.write(row, col+3, green_count)
    worksheet.write(row, col+4, amber_count)
    worksheet.write(row, col+5, red_count)
    worksheet.write(row, col+6, unknown_count)
    row = row+1

# print("Green genes: " + str(green_count) + "\nRed genes: " + str(red_count) + "\nAmber genes: " + str(amber_count) + "\nUnknown genes: " + str(unknown_count))
# print("Calculated gene total: " +str(calculated_gene_tot))
'''
workbook.close()


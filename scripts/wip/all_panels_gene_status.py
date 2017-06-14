"""
Retrieve the status of all genes in all panels for a given panel list

For each panel in a given list (.csv file):
 - Retrieve the status of all genes within that panel
 - Export this information as a list

Input is an .csv file containing panel name, panel id and version number.
"""

import json, requests, datetime, xlsxwriter, csv, sys, pandas as pd

# if this were to be another function calling from an earlier function then previous variables would need to be captured
# panel_id = get_panel_id()
# version_num = get_version_num()

todays_date = datetime.datetime.now().strftime("%Y%m%d")
# print(todays_date)

'''
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
'''

with open(sys.argv[1], 'r') as csvfile:
    panel_list = csv.reader(csvfile)
    csvfile.readline()

    for panel in panel_list:

        panel_name = (panel[0])
        panel_id = (panel[1])
        panel_version = (panel[2])
        
        print("Checking " + panel_name + "...")
        
        url = 'https://bioinfo.extge.co.uk/crowdsourcing/WebServices/get_panel/' + panel_id + '/?version=' + panel_version
        print(url)
        r = requests.get(url)

        panel_data = r.json()
 
        # retrieve gene name and status for each version
        gene_info = panel_data['result']['Genes']
     
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
            # print(panel_name,panel_version,gene_symbol,gene_status)
            
        # print("Green genes: " + str(green_count) + "\nRed genes: " + str(red_count) + "\nAmber genes: " + str(amber_count) + "\nUnknown genes: " + str(unknown_count))
        # calc_gene_tot = (green_count + red_count + amber_count + unknown_count)
        # print("Calculated gene total: " +str(calc_gene_tot))
        
        # then search for the panel name in the previous panel list which has been selected (sys.argv[2]?).
        with open(sys.argv[2], 'r') as csvfile_prev:
            panel_list_prev = csv.reader(csvfile_prev)
            csvfile_prev.readline()

            for panel in panel_list_prev:

                panel_name_prev = (panel[0])
                panel_id_prev = (panel[1])
                panel_version_prev = (panel[2])
            
                if panel_name == panel_name_prev:
            	    if panel_version == panel_version_prev:
            		    print("Panel versions match")
            	    else:
                        print(panel_name,panel_version,panel_version_prev)
                        
        # if this panel name is in the prev_panel_list, search for the version number of that panel
        # if the panel version numbers are the same, genes_unchanged = calc_gene_tot and all other gene counts will be the same.
        # if the panel version numbers don't match, retrieve the panel_data for the prev_version
        # then iterate through the genes in the curr_version to see if they exist in the same panel in the prev_version
        
'''
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

workbook.close()
'''

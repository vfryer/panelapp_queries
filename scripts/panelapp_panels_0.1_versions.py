"""
Retrieve a list of all .1 increment versions of all panels (e.g. 0.1, 0.2, 0.3 etc).
Retrieve the gene names and gene status for all genes within these versions of the panels
Output an MS Excel file containing two tabs.
First tab contains panel name, panel id, panel version, gene name and the level of confidence for genes in that version
Second tab contains the count of red, amber, green and unknown genes for each version of each panel.
"""

import requests,json,xlsxwriter,datetime

todays_date = datetime.datetime.now().strftime("%Y%m%d")
# print(todays_date)

workbook = xlsxwriter.Workbook('all_major_panel_versions_data' + todays_date + '.xlsx')
worksheet = workbook.add_worksheet('Panel_versions')
worksheet2 = workbook.add_worksheet('Genes')

# Add a bold format to use to highlight cells.
bold = workbook.add_format({'bold': True})

worksheet.write('A1', 'Panel Name', bold)
worksheet.write('B1', 'Panel Id', bold)
worksheet.write('C1', 'Version Number', bold)
worksheet.write('D1', 'Gene', bold)
worksheet.write('E1', 'Evidence', bold)

worksheet2.write('A1', 'Panel Name', bold)
worksheet2.write('B1', 'Panel Version', bold)
worksheet2.write('C1', 'Green Genes', bold)
worksheet2.write('D1', 'Amber Genes', bold)
worksheet2.write('E1', 'Red Genes', bold)
worksheet2.write('F1', 'Unknown Genes', bold)

row = 1
row2 = 1
col = 0

# retrieve a list of all panel names
r = requests.get('https://bioinfo.extge.co.uk/crowdsourcing/WebServices/list_panels')
panel_data = r.json()

panel_list = panel_data["result"]

panels_complete = 0

for panel in panel_list:
#    panel_id = "553f94b3bb5a1616e5ed4593" # for testing purposes
    panel_id = panel["Panel_Id"]
#    panel_name = 'Vici Syndrome and other autophagy disorders' # for testing purposes
    panel_name = panel["Name"]
    curr_version_num = float(panel["CurrentVersion"])
    print(panel_name, curr_version_num)

# add script to retrieve the current versions of all panels
# then use the current panel version numbers to reduce the while loop below
# e.g. while version_num is <= curr_version_num

# search for each panel name and version numbers (version numbers from 0.0 to 2.0 with increments of 0.01)
# if a version number exists, print/write to file
# if a version number doesn't exist, skip and search for the next version number or panel
    version_num = round(0.0,1)
    # while loop executes only until the version number being searched is <= current version of the panel
    if version_num < curr_version_num:
        version_num = str(round(version_num, 1))
        try:
            get_panel_version = requests.get('https://bioinfo.extge.co.uk/crowdsourcing/WebServices/get_panel/' + panel_id + '/?version=' + str(version_num))
            version_data = get_panel_version.json()
            print(panel_name + ' v' + str(version_num))

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
                worksheet.write(row, col, panel_name)
                worksheet.write(row, col+1, panel_id)
                worksheet.write(row, col+2, version_num)
                worksheet.write(row, col+3, gene_symbol)
                worksheet.write(row, col+4, gene_confidence)

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

            # increment version number by 0.01
            version_num = float(version_num) + 0.1
            version_num = round(version_num,1)
        # handle panels for which a panel version number doesn't exist
        # print a message to the user, then round the version number into a float with 1 d.p. (2 d.p. means rounding operation won't work)
        except:
            print('No v' + str(version_num) + ' for ' + panel_name + ' ' + panel_id + ' could be retrieved')
            version_num = curr_version_num
    else:
        version_num = curr_version_num
        get_panel_version = requests.get('https://bioinfo.extge.co.uk/crowdsourcing/WebServices/get_panel/' + panel_id + '/?version=' + str(version_num))
        version_data = get_panel_version.json()
        print(panel_name + ' v' + str(version_num))

        gene_info = version_data['result']['Genes']

        for gene in gene_info:
            gene_symbol = gene['GeneSymbol']
            gene_confidence = gene['LevelOfConfidence']
            # print(gene_symbol, gene_confidence)
            worksheet.write(row, col, panel_name)
            worksheet.write(row, col + 1, panel_id)
            worksheet.write(row, col + 2, version_num)
            worksheet.write(row, col + 3, gene_symbol)
            worksheet.write(row, col + 4, gene_confidence)

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
    worksheet2.write(row2, col + 1, version_num)
    worksheet2.write(row2, col + 2, green_count)
    worksheet2.write(row2, col + 3, amber_count)
    worksheet2.write(row2, col + 4, red_count)
    worksheet2.write(row2, col + 5, unknown_count)
    row2 = row2 + 1
# this loop does not capture incidences where the version number is in format of greater than 2 d.p, e.g. x.xxx.
# it also does not capture data from version numbers 2 d.p. long that end in 0 e.g. v1.10 (which is different to v1.1!)

    # print a message to the user to gauge how far through the script is.
    panels_complete = panels_complete + 1
    print(str(panels_complete) + ' panels complete of ' + str(len(panel_list)))

# would be nice to sort the data alphabetically/into ascending order in the output file

# save all data to the Excel spreadsheet by closing it.
workbook.close()
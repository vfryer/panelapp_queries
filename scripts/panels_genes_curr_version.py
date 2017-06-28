"""
Title: panels_curr_version.py
Version:
Release Date:  
Author: VFryer
The following code retrieves all panel names from PanelApp, with current panel versions, gene symbols and gene status
Usage: python panels_genes_curr.py <output file location>
"""

import requests, json, csv, datetime, sys, os

out_path = sys.argv[1]

# save today's date to use in the filename to record a snapshot of panel versions on a weekly basis
todays_date = datetime.datetime.now().strftime("%Y%m%d")

# retrieve a list of all panel names
r = requests.get('https://bioinfo.extge.co.uk/crowdsourcing/WebServices/list_panels')
panel_data = r.json()

panel_list = panel_data["result"]

filename = os.path.join(out_path, 'panel_versions_list_' + todays_date + '.csv')

csv_file = open(filename, 'w')
writer = csv.writer(csv_file, delimiter=",")

writer.writerow(['Panel Name', 'Panel ID', 'Version Number', 'Gene Name', 'Gene Status'])

for panel in panel_list:
    panel_id = panel["Panel_Id"]
    panel_name = panel["Name"]
    version_num = panel["Version"]

    try:
        url = 'https://bioinfo.extge.co.uk/crowdsourcing/WebServices/get_panel/' + panel_id + '/?version=' + version_num
        # print(url)
        r = requests.get(url)

        panel_data = r.json()

        # retrieve gene name and status for each version
        gene_info = panel_data['result']['Genes']

        # get all genes and their status
        for gene in gene_info:
            gene_symbol = gene["GeneSymbol"]
            gene_confidence = gene["LevelOfConfidence"]
            # print(gene_symbol, gene_confidence)
            if gene_confidence == "LowEvidence":
                gene_status = "Red"
            elif gene_confidence == "HighEvidence":
                gene_status = "Green"
            elif gene_confidence == "ModerateEvidence":
                gene_status = "Amber"
            else:
                gene_status = "Unknown"
                # print(panel_name,panel_version,gene_symbol,gene_status)
    except:
        print("Panel not found")

    # write the panel name, id and version number to a csv file
    row = [panel_name, panel_id, version_num, gene_symbol, gene_status]
    writer.writerow(row)
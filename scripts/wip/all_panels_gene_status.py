"""
Retrieve the status of all genes in all panels for a given panel list

For each panel in a given list (.csv file):
 - Retrieve the status of all genes within that panel
 - Export this information as a list

Input is an .csv file containing panel name, panel id and version number.
Usage python all_panels_gene_status.py <composite list of panels>
"""

import json, requests, datetime, csv, sys, pandas as pd

# if this were to be another function calling from an earlier function then previous variables would need to be captured
# panel_id = get_panel_id()
# version_num = get_version_num()

todays_date = datetime.datetime.now().strftime("%Y%m%d")
# print(todays_date)

def panel_info(panel_version, version):
    
    try:
        url = 'https://bioinfo.extge.co.uk/crowdsourcing/WebServices/get_panel/' + panel_id + '/?version=' + panel_version
        # print(url)
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
    except:
        pass

# create a dataframe instead of a csv for both previous version and current version searches.


# then merge these dataframes on panel_id and version number
'''
# export this into a csv or Excel file.
            with open('gene_status_' + version + '_' + todays_date + '.csv', 'a') as outfile:
                writer = csv.writer(outfile)
                writer.writerow([panel_name, gene_symbol, gene_status])
                
'''

with open(sys.argv[1], 'r') as csvfile:
    panel_list = csv.reader(csvfile)
    # csvfile.readline() # remove header line

    for panel in panel_list:

        panel_name = (panel[0])
        panel_id = (panel[1])
        curr_version = (panel[2])
        try:
            prev_version = (panel[3])
        except:
            prev_version = "N/A"

        print("Checking " + panel_name + "...")
        print(panel_name + ' ' + panel_id + ' ' + curr_version + ' ' + prev_version)
        d = [{'Panel Name':panel_name, 'Panel ID':panel_id, 'Current Version':curr_version, 'Previous Version':prev_version}]
        df = pd.DataFrame(d)

        print(df)

        panel_info(curr_version, 'current')
        panel_info(prev_version, 'previous')


'''
#    calculated_gene_tot = (green_count + red_count + amber_count + unknown_count)


# print("Green genes: " + str(green_count) + "\nRed genes: " + str(red_count) + "\nAmber genes: " + str(amber_count) + "\nUnknown genes: " + str(unknown_count))
# print("Calculated gene total: " +str(calculated_gene_tot))
'''


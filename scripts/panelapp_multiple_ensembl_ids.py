import requests, json

# get list of all panel names currently in panelApp

r = requests.get('https://bioinfo.extge.co.uk/crowdsourcing/WebServices/list_panels')
panel_data = r.json()

# store data as a list of dictionaries (the current JSON format contains a dictionary of a list of dictionaries)
panel_list = panel_data['result']

# iterate through the list of dictionaries, printing out only the values associated with the "Name" key
for dict in panel_list:
    if "Name" in dict:
        panel_name = dict["Name"]

        panel_name_amend = panel_name.replace(" ","%20")

        r = requests.get('https://bioinfo.extge.co.uk/crowdsourcing/WebServices/search_genes/all/?panel_name=' + panel_name_amend + '&format=json')
        data = r.json()

        gene_info = data['results']

        # print all the Ensembl Ids for every gene within the panel
        gene_count = 0
        for dict in gene_info:
            if "GeneSymbol" in dict:
                gene_count = gene_count+1
                gene_symbol = (dict["GeneSymbol"])
                ensembl_id_dict = (dict["EnsembleGeneIds"])
                ensembl_id_count = 0
                for ensembl_id in ensembl_id_dict:
                    if "ENSG" in ensembl_id:
                        ensembl_id_count = ensembl_id_count+1
                    else:
                        pass
                if ensembl_id_count >1:
                    print(gene_symbol, ensembl_id_count)

# print total number of genes in the panel

        print("Number of genes in panel " + panel_name + ": " + str(gene_count))

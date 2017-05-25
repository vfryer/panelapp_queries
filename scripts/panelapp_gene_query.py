import requests, json

panel_name = 'Epileptic encephalopathy'

if ' ' in panel_name:
    panel_name_amend = panel_name.replace(' ','%20')
else:
    panel_name_amend = panel_name

r = requests.get('https://bioinfo.extge.co.uk/crowdsourcing/WebServices/get_panel/' + panel_name_amend)
panel_data = r.json()

print(panel_data)

gene_info = panel_data['result']['Genes']
print(gene_info)

'''
# print all fields for each gene
for dict in gene_info:
    for key, value in dict.items():
        print(key, value)
'''


# to print the gene name for each gene and the evidence level
for dict in gene_info:
    if "GeneSymbol" in dict:
        gene_symbol = (dict["GeneSymbol"])
        gene_confidence = (dict["LevelOfConfidence"])
        print(gene_symbol, gene_confidence)

#        if gene_symbol == "DSE":
#            print(gene_confidence)

'''
# print all the Ensembl Ids for every gene
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
'''
#        print(gene_symbol, ensembl_id_dict, str(len(ensembl_id)))

# print total number of genes in the panel
#print("Number of genes in panel " + panel_name + ": " + str(gene_count))

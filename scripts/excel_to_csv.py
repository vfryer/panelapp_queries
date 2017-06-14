"""
Convert an Excel file into a csv file.
Author: VFryer (verity.fryer@nhs.net)
Release: 1.0
usage: python excel_to_csv.py <Excel file to be converted>
"""
import sys, os
import pandas as pd

# enable code to be used with any Excel file input by user
excel_file = sys.argv[1]

# split the name of the input file to remove the extension and the subsequent .csv will also have this name
excel_filename = os.path.splitext(excel_file)[0]


# use pandas to read Excel file and convert the file to a csv
def excel_to_csv():
    excel_data = pd.read_excel(excel_file)
    excel_data.to_csv(excel_filename + '.csv')
    
excel_to_csv()

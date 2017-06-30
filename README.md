# panelapp_queries
Coding project to query data in PanelApp.

Documentation

*****Scripts and usage******
Script title:
 - panels_genes_to_csv.py
Description:
 - Standalone script that can be run at any time to retrieve a list of all current panels and associated genes with gene status.
Usage:
 - python panels_genes_to_csv.py <output file location>
Inputs/Outputs:
 - Inputs = Location for file output in the command line request
 - Output = .csv file with headers (Panel Name, Panel ID, Current Panel Version Number, Gene Name, Gene Status).
            Lists all genes in panels and their gene status.


Current aims (24/05/17):

1. PanelApp Query (panelapp_panels_curr_version.py) to return all current versions of panels within PanelApp and status of all genes within each panel
  - output as MS Excel file
  - this will then be used to create a pie chart for all green/amber/red/unknown status genes currently
  - documentation for script
 
2. Python script that will compare the current PanelApp versions with a previous version (specified output from panelapp_panels_curr_version.py) and output an Excel file for each panel of:
  - total red/amber/green/unknown genes
  - ?status unchanged
  - red -> green genes
  - green -> red genes (?arguably green -> anything other than green)
  - new genes
  - documentation for script (ensure the user can input the two scripts to be compared using sys.argv)

3. PanelApp Query that will compare the status of genes in v0.0 panel (if it exists) with current panel. If a v0.0 doesn't exist, compare current version with first version that does contain data.
  - total red/amber/green/unknown genes
  - ?status unchanged
  - red -> green genes
  - green -> red genes (?arguably green -> anything other than green)
  - new genes
  - documentation for script (ensure the user can input the two scripts to be compared using sys.argv)

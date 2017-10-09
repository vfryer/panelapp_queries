# panelapp_queries
Created by Verity Fryer verity.fryer@nhs.net

Coding project to query data in PanelApp.

This code was developed as part of a coding project during an elective at Genomics England. This code is designed to retrieve current data from PanelApp (https://bioinfo.extge.co.uk/crowdsourcing/PanelApp/) using the webservices API (https://bioinfo.extge.co.uk/crowdsourcing/PanelApp/#!HowTo) and store this data into a SQLite database (PanelApp_data.db). The data retrieved includes panel name, panel id, current panel version and the all of the genes listed in each panel plus the current status of the gene in each panel.The code will also generate some figures and summary tables of the data and compare one data capture against another, thereby alerting the user to what changes have occurred to which genes/panels over a particular time period. 

## Prerequisites:
* python 3
* pandas
* matplotlib
* requests, sys, json, csv, datetime, os, sqlite3, time
N.B. all of these can be imported using the virtual environement packaged here by activating the virtual environment using command source panelapp_queries/bin/activate.

*Scripts and usage*


**__Script title: panels_summary.py__**
Standalone script that can be run at any time to retrieve a list of all current panels, version numbers and total number of panels and total numbers of v0/v1/v2 panels.

## Usage:
Run from in panelapp_queries directory:

    python3 scripts/panels_summary.py outputs/

## Inputs/Outputs:
 - Inputs
   - Location for file output in the command line request (outputs/ directory recommended as in usage example)
 - Outputs (all saved in panelapp_queries/outputs)
   - panelapp_summary table in PanelApp_data.db including total number of panels, number of v0 and v1 panels
   - summary table printed to screen
   - panel_summary.png graph
   - backup .csv file containing Panel Name, Panel ID, Current Panel Version Number
 
 
**__Script title: gene_status_summary.py__**
Standalone script that can be run at any time to retrieve a list of all panel names from PanelApp, with current panel versions, gene symbols, gene status and mode of inheritance (MOI).

## Usage
Run from in panelapp_queries directory:

    python3 scripts/gene_status_summary.py outputs/

## Inputs/Outputs
 - Inputs
   - Location for file output in the command line request (outputs/ directory recommended as in usage example)
 - Outputs (all saved in panelapp_queries/outputs)
   - panelapp_info table in PanelApp_data.db including Datestamp, Panel Name, Panel ID, Version Number, Gene Symbol, current Gene Status and mode of inheritance (MOI)
   - gene_status_summary table in PanelApp_data.db including counts of all genes according to status (red, green, amber or no list) for each panel
   - gene_status_summary.png graph
   - backup .csv file containing data as in panelapp_info table
 

**__Script title: panels_comparison.py__**
Script that can be run at any time, however, for the most recent data available, this should be run immdeiately after both panels_summary.py and gene_status_summary.py. This will allow you to select two dates for which panel and gene status information is stored within the PanelApp.db database and compare the two datasets, returning an Excel file containing the difference between these two dates.

## Usage
Run from in panelapp_queries directory:

    python3 scripts/panels_comparison.py outputs/
    
User is prompted to select dates for comparison as the program is running.

## Inputs/Outputs
 - Inputs
   - Location for file output in the command line request (outputs/ directory recommended as in usage example)
 - Outputs (all saved in panelapp_queries/outputs)
   - panels_genes_comp_<datestamp1>_to_<datestamp2>.xlsx summary file of all differences between the two data sets (see below for details)
   
Categories (and the selection criteria) included within the comparison Excel file are:
	New v1 panels (did not exist in previous month)
	New v0 panels (did not exist in previous month)
	Removed panels (existed in previous month, no longer exists)
	Promoted panels (previously v0 but now v1+)
	Updated v1 panels (previously v1+, curently a different v1+)
	Updated v0 panels (previously v0+, currently a different v0+)
	Panels with a name change
	New genes (Green status, new to a v1 panel since previous query)
	New genes (Not green, new to a v1 panel since previous query)
	Removed genes (Previously green status, but no longer on panel)
	Removed genes (Previously not green status, no longer on panel)
	Promoted genes (Green in v1 panels not green previously)
	Promoted genes (Green in v0 panels not green previously)
	Demoted genes (Previously green in v1 panel, no longer green)
	Amended mode of inheritance (for green genes in v1 panels only)


It is recommended that each month, or whenever these scripts are run, the previous outputs are moved from outputs/directory into the archive or deleted.

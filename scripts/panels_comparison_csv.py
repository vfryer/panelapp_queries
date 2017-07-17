"""
Ttle: panels_comparison.py
Version: 1.0
Release Date: 19/06/2017
Author: VFryer
This program compares the current and previous panel versions lists (.csv files)
Output will be count of panels updated/unchanged/retired/created
Usage: python panels_comparison.py <current_panels_file> <previous_panels_file>
"""

import pandas as pd
import datetime

todays_date = datetime.datetime.now().strftime("%Y%m%d")

new_panel_count = 0
unchanged_count = 0
updated_count = 0

# convert the current version file and previous panel versions file into dataframes to be compared

df_curr = pd.read_csv(sys.argv[1], dtype='str')
df_prev = pd.read_csv(sys.argv[2], dtype='str')

df = pd.merge(df_curr,df_prev, on=["Panel ID", "Panel Name"], how="outer", suffixes=[' Current',' Previous'], indicator=True)

writer = pd.ExcelWriter('panels_status_' + todays_date + '.xlsx', engine='xlsxwriter')

# create dataframe of panels that are in both lists
existing_panels = df[df['_merge'].str.contains("both")]

# create dataframe and worksheet of panels that have not been updated
unchanged_panels = existing_panels.loc[existing_panels['Version Number Current'] == existing_panels['Version Number Previous']]
unchanged_panels = unchanged_panels.drop('_merge', 1)
unchanged_panels = unchanged_panels.drop('Version Number Previous', 1)
unchanged_panels.set_index('Panel Name', inplace=True)
unchanged_panels.to_excel(writer,sheet_name='Unchanged Panels')

unchanged_panels_count = len(unchanged_panels.index)
print("Number of unchanged panels: " + str(unchanged_panels_count))

# create dataframe and worksheet of panels that have been updated
updated_panels = existing_panels.loc[existing_panels['Version Number Current'] != existing_panels['Version Number Previous']]
updated_panels = updated_panels.drop('_merge', 1)
updated_panels.set_index('Panel Name', inplace=True)
updated_panels.to_excel(writer,sheet_name='Updated Panels')

updated_panels_count = len(updated_panels.index)
print("Number of updated panels: " + str(updated_panels_count))

# create a dataframe of panels only in previous list but not current (i.e. retired/obsolete)
retired_panels = df[df['_merge'].str.contains("right_only")]
retired_panels = retired_panels.drop('_merge', 1)
retired_panels = retired_panels.drop('Version Number Current', 1)
retired_panels.set_index('Panel Name', inplace=True)
retired_panels.to_excel(writer,sheet_name='Retired Panels')

retired_panels_count = len(retired_panels.index)
print("Number of retired panels: " + str(retired_panels_count))

# create a dataframe of panels in current list but not previous list (i.e. new panels)
new_panels = df[df['_merge'].str.contains("left_only")]
new_panels = new_panels.drop('_merge', 1)
new_panels = new_panels.drop('Version Number Previous', 1)
new_panels.set_index('Panel Name', inplace=True)
new_panels.to_excel(writer,sheet_name='New Panels')

new_panels_count = len(new_panels.index)
print("Number of new panels: " + str(new_panels_count))

writer.save()

# create .csv of all existing and new panels for further data gathering purposes
existing_panels = existing_panels.drop('_merge', 1)
existing_panels.set_index('Panel Name', inplace=True)
existing_panels = pd.DataFrame(existing_panels, dtype='str')
existing_panels.to_csv('panels_list_composite_'+todays_date+'.csv',mode='a',header=False)
new_panels.to_csv('panels_list_composite_'+todays_date+'.csv',mode='a',header=False)


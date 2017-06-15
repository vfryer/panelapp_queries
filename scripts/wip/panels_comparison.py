"""
Ttle: panels_comparison.py
Version: 
Release Date: 
Author: VFryer
This program compares the current and previous panel versions lists (.csv files)
Output will be count of panels updated/unchanged/retired/created
"""

import pandas as pd
import datetime, sys, xlsxwriter

todays_date = datetime.datetime.now().strftime("%Y%m%d")

new_panel_count = 0
unchanged_count = 0
updated_count = 0

# convert the current version file and previous panel versions file into dataframes to be compared

df_curr = pd.read_csv(sys.argv[1])
df_prev = pd.read_csv(sys.argv[2])

df = pd.merge(df_curr,df_prev, on=["Panel ID", "Panel Name"], how="outer", suffixes=[' Current',' Previous'], indicator=True)

writer = pd.ExcelWriter('panels_status_' + todays_date + '.xlsx', engine='xlsxwriter')

# create dataframe of panels that are in both lists
existing_panels = df[df['_merge'].str.contains("both")]

# need to add ability to split existing_panels list into two lists:
unchanged_panels = existing_panels.loc[existing_panels['Version Number Current'] == existing_panels['Version Number Previous']]
unchanged_panels = unchanged_panels.drop('_merge', 1)
unchanged_panels.set_index('Panel Name', inplace=True)
unchanged_panels.to_excel(writer,sheet_name='Unchanged Panels')

unchanged_panels_count = len(unchanged_panels.index)
print(unchanged_panels_count)

updated_panels = existing_panels.loc[existing_panels['Version Number Current'] != existing_panels['Version Number Previous']]
updated_panels = updated_panels.drop('_merge', 1)
updated_panels.set_index('Panel Name', inplace=True)
updated_panels.to_excel(writer,sheet_name='Updated Panels')

updated_panels_count = len(updated_panels.index)
print(updated_panels_count)

existing_panels = existing_panels.drop('_merge', 1)
existing_panels.set_index('Panel Name', inplace=True)
existing_panels.to_excel(writer,sheet_name='Existing Panels')

existing_panels_count = len(existing_panels.index)
print(existing_panels_count)

# create a dataframe of panels only in previous list but not current
retired_panels = df[df['_merge'].str.contains("right_only")]
retired_panels = retired_panels.drop('_merge', 1)
retired_panels = retired_panels.drop('Version Number Current', 1)
retired_panels.set_index('Panel Name', inplace=True)
retired_panels.to_excel(writer,sheet_name='Retired Panels')

retired_panels_count = len(retired_panels.index)
print(retired_panels_count)

# create a dataframe of panels in current list but not previous list
new_panels = df[df['_merge'].str.contains("left_only")]
new_panels = new_panels.drop('_merge', 1)
new_panels = new_panels.drop('Version Number Previous', 1)
new_panels.set_index('Panel Name', inplace=True)
new_panels.to_excel(writer,sheet_name='New Panels')

new_panels_count = len(new_panels.index)
print(new_panels_count)

writer.save()

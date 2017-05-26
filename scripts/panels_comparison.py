import pandas as pd
import datetime

todays_date = datetime.datetime.now().strftime("%Y%m%d")

# open the file
prev_panels = pd.read_excel(r"C:\Users\Verity Fryer\PyCharmProjects\panelapp_queries\outputs\panel_versions_list_20170523_test.xlsx")
curr_panels = pd.read_excel(r"C:\Users\Verity Fryer\PyCharmProjects\panelapp_queries\outputs\panel_versions_list_20170525_test.xlsx")

df_inner = pd.merge(curr_panels,prev_panels,on=['Panel Id'], how='inner')
df_inner = df_inner.drop(['Panel Name_y'],axis=1)
print(df_inner)

df_left_if_null = pd.merge(curr_panels,prev_panels,on=['Panel Id'], how='left')
df_left_if_null = df_left_if_null[df_left_if_null['Panel Name_y'].isnull()]
df_left_if_null = df_left_if_null.drop(['Panel Name_y','Version Number_y'],axis=1)
print(df_left_if_null)

df_right_if_null = pd.merge(curr_panels,prev_panels,on=['Panel Id'], how='right')
df_right_if_null = df_right_if_null[df_right_if_null['Panel Name_x'].isnull()]
df_right_if_null = df_right_if_null.drop(['Panel Name_x','Version Number_x'],axis=1)
print(df_right_if_null)

writer = pd.ExcelWriter('output_' + todays_date + '.xlsx')
df_inner.to_excel(writer,'Existing panels')
df_left_if_null.to_excel(writer,'Obsolete panels')
df_right_if_null.to_excel(writer,'New panels')
writer.save()




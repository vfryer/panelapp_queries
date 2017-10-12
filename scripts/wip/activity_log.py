'''
# Author Verity Fryer verity.fryer@nhs.net
Usage: python scripts/activity_log.py <output file location>
'''

import pandas as pd, requests, sqlite3, sys
from bs4 import BeautifulSoup

# create a connection to the specified SQlite database
conn = sqlite3.connect("outputs/PanelApp_Data.db")
cur = conn.cursor()

outpath = sys.argv[1]


#try:
#    cur.execute(
#        "CREATE TABLE IF NOT EXISTS panelapp_activity (Date TEXT, Panel TEXT, Gene TEXT, Activity TEXT)") 
#except:
#    print("Cannot create table. It may already exist. Program will now end.") 
#    sys.exit()

# Capture data from activity page of PanelApp
url = 'https://panelapp.extge.co.uk/crowdsourcing/PanelApp/Activity'

r = requests.get(url)
data = r.text
soup = BeautifulSoup(data, 'lxml')

# find the first table in the webpage
table = soup.find_all('table')[0]

# find the first rows (skip the first two rows which are table filters and contain no data)
rows = table.find_all('tr')[2:]

data = {'Date':[],'Panel':[],'Gene':[],'Activity':[]}

# Create a dataframe of the activity captured from the activity page
for row in rows:
    cols = row.find_all('td')
    data['Date'].append(cols[0].get_text().strip('\n'))
    data['Panel'].append(cols[1].get_text().strip('\n'))
    data['Gene'].append(cols[2].get_text().strip('\n'))
    data['Activity'].append(cols[3].get_text().strip('\n').strip())

df = pd.DataFrame(data)

# Create a dataframe of the existing activity from the database
df2 = pd.read_sql("SELECT * FROM panelapp_activity", conn)
#remove any duplicates from existing dataframe
df2 = df2.drop_duplicates()
#strip trailing and leading whitespace from 'Activity' data
df2['Activity'] = df2['Activity'].str.strip()

# Add new dataframe to existing datframe
# Keep only values in new dataframe that are not duplicates
new_entries_df = df.append(df2, ignore_index=True).drop_duplicates(keep=False)

# Save only new data to database
new_entries_df.to_sql('panelapp_activity',conn,index=False,if_exists='append')

# Input date range of interest

# return all activity from 15 Aug 2017
df3 = pd.read_sql("SELECT * FROM panelapp_activity WHERE Date LIKE '15 Aug 2017'", conn) #(str(date) + '%',))
df3 = df3.set_index('Date')
print(df3)
df3 = df3.to_csv(outpath+"activity_15-08-17",header=['Panel','Gene','Activity'])

# Return number of reviewers within date range
# Return number of reviews per reviewer within date range
# Plot graph of number of reviews per reviewer within date range

# Close cursor and database connection to store data to database
cur.close()
conn.close()

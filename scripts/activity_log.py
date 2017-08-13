# Author Verity Fryer verity.fryer@nhs.net

import pandas as pd, requests, sqlite3
from bs4 import BeautifulSoup

# create a connection to the specified SQlite database
conn = sqlite3.connect("outputs/PanelApp_Data_test.db")
cur = conn.cursor()

try: 
    cur.execute( 
        "CREATE TABLE IF NOT EXISTS panelapp_activity (Date TEXT,Panel_Name TEXT, Gene_Name TEXT, Activity TEXT)") 
except: 
    print("Cannot create table. It may already exist. Program will now end.") 
    sys.exit() 

# Capture data from activity page of PanelApp
url = 'https://panelapp.extge.co.uk/crowdsourcing/PanelApp/Activity'
r = requests.get(url)
soup = BeautifulSoup(r.content,'lxml')

table = soup.find_all('table')[0]
df = pd.read_html(str(table))

activity_df = pd.concat(df)

activity_df.columns.values[0] = 'Date'
activity_df.columns.values[1] = 'Panel'
activity_df.columns.values[2] = 'Gene'
activity_df.columns.values[3] = 'Activity'
print(activity_df)

for df in activity_df:
    cur.execute("INSERT INTO panelapp_activity VALUES (?,?,?,?)", ("Date","Panel","Gene","Activity"))


# Save data to database
# Remove any duplicate entries
# Input date range of interest
# Return number of reviewers within date range
# Return number of reviews per reviewer within date range
# Plot graph of number of reviews per reviewer within date range

# Close cursor and database connection to store data to database

cur.close()
conn.close()
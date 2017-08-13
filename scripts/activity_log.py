# Author Verity Fryer verity.fryer@nhs.net

import pandas as pd, requests, sqlite3
from bs4 import BeautifulSoup

# create a connection to the specified SQlite database
conn = sqlite3.connect("outputs/PanelApp_Data_test.db")
cur = conn.cursor()

try:
    cur.execute(
        "CREATE TABLE IF NOT EXISTS panelapp_activity (Date TEXT, Panel TEXT, Gene TEXT, Activity TEXT)") 
except:
    print("Cannot create table. It may already exist. Program will now end.") 
    sys.exit()

# Capture data from activity page of PanelApp
url = 'https://panelapp.extge.co.uk/crowdsourcing/PanelApp/Activity'

r = requests.get(url)
data = r.text
soup = BeautifulSoup(data, 'lxml')

table = soup.find_all('table')[0]

rows = table.find_all('tr')[2:]

data = {'Date':[],'Panel':[],'Gene':[],'Activity':[]}

for row in rows:
    cols = row.find_all('td')
    data['Date'].append(cols[0].get_text().strip('\n'))
    data['Panel'].append(cols[1].get_text().strip('\n'))
    data['Gene'].append(cols[2].get_text().strip('\n'))
    data['Activity'].append(cols[3].get_text().strip('\n'))

df = pd.DataFrame(data)
print(df)

# Save data to database

df.to_sql('panelapp_activity',conn,index=False,if_exists='append')

# Remove any duplicate entries
# Input date range of interest
# Return number of reviewers within date range
# Return number of reviews per reviewer within date range
# Plot graph of number of reviews per reviewer within date range

# Close cursor and database connection to store data to database
cur.close()
conn.close()

import requests, csv, datetime, sys, os
import sqlite3, time, pandas as pd

# create a connection to the specified SQLite database
conn = sqlite3.connect("outputs/PanelApp_Data.db")
cur = conn.cursor()


def update_data():
    # N.B. *** N.B. Data amended in SQLite database cannot be restored!***
    cur.execute("SELECT * from panelapp_info WHERE Datestamp LIKE '201705%'")
    data = cur.fetchall()

    cur.execute("UPDATE panelapp_info SET Datestamp = '2017-05-23 01:00:00' WHERE Datestamp = '20170523 01:00:00'")
    conn.commit()
    
    cur.execute("SELECT * from panelapp_info WHERE Datestamp LIKE '201705%'")
    data = cur.fetchall()

def delete_data():
    # ***N.B. data deleted from SQLite DB cannot be restored!***
    cur.execute("SELECT DISTINCT Datestamp from panelapp_info")
    data = cur.fetchall()
    for row in data:
        print(row)

    cur.execute("DELETE FROM panelapp_info WHERE Datestamp LIKE '2017-07-17%'")
    conn.commit()

# Add a step to copy existing database into a back-up folder?

cur.close()
conn.close()


import sqlite3, datetime, time

conn = sqlite3.connect('PanelApp.db')
cur = conn.cursor()

def create_table():
    cur.execute('CREATE TABLE IF NOT EXISTS panelapp_info(name TEXT, id TEXT, version TEXT, datestamp TEXT, gene TEXT, status TEXT)')

def data_entry():
    t = time.time()
    date = str(datetime.datetime.fromtimestamp(t).strftime('%Y-%m-%d %H:%M:%S'))


    cur.execute('INSERT INTO panels VALUES(datestamp, name, id, version, gene, status)')
    conn.commit()

create_table()
data_entry()

# cur.close()
# conn.close()
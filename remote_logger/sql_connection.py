import sqlite3

def init():
    con = sqlite3.connect('LOG_DB.db')
    cur = con.cursor()
    print('Initializing connection...')
    listOfTables = cur.execute("""SELECT name FROM sqlite_master WHERE type='table' AND name='LOGS'; """).fetchall()
 
    if listOfTables == []:
            cur.execute("""CREATE TABLE LOGS(DATE CHAR(10),TIME VARCHAR(12), TYPE VARCHAR(10), MESSAGE VARCHAR (100));""")
            print('Connection with database initialized')
    else:  
            print('Connection with database initialized')
    con.commit()
    con.close()

def insert_log(full_date, type, message):
    con = sqlite3.connect('LOG_DB.db')
    cur = con.cursor()
    date = full_date.split(' ')[0]
    time = full_date.split(' ')[1]
    data = (date, time, type, message)
    statement = """INSERT INTO LOGS(DATE, TIME, TYPE, MESSAGE) VALUES(?, ?, ?, ?)"""
    cur.execute(statement, data)
    con.commit()
    con.close()

def get_logs():
    con = sqlite3.connect('LOG_DB.db')
    cur = con.cursor()
    statement = """SELECT * FROM LOGS"""
    cur.execute(statement)
    output = cur.fetchall()
    items = []
    for row in output:
        items.append({'date':row[0], 'time':row[1], 'type':row[2], 'message':row[3]})
    con.commit()
    con.close()
    return items
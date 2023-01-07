import sqlite3

def init():
    con = sqlite3.connect('ALERT_DB.db')
    cur = con.cursor()
    print('Initializing connection...')
    listOfTables = cur.execute("""SELECT name FROM sqlite_master WHERE type='table' AND name='ALERTS'; """).fetchall()
    if listOfTables == []:
            cur.execute("""CREATE TABLE ALERTS(TIMESTAMP DATETIME, RULE_NAME VARCHAR(20), MESSAGE VARCHAR(250));""")
            print('Connection with database initialized')
    else:  
            print('Connection with database initialized')
    con.commit()
    con.close()

def insert_log(timestamp, rule_name, message):
    con = sqlite3.connect('ALERT_DB.db')
    cur = con.cursor()
    data = (timestamp, rule_name, message)
    statement = """INSERT INTO ALERTS(TIMESTAMP, RULE_NAME, MESSAGE) VALUES(?, ?, ?)"""
    cur.execute(statement, data)
    con.commit()
    con.close()

def get_logs():
    con = sqlite3.connect('ALERT_DB.db')
    cur = con.cursor()
    statement = """SELECT * FROM ALERTS"""
    cur.execute(statement)
    output = cur.fetchall()
    items = []
    for row in output:
        items.append({'timestamp':row[0],'rule_name':row[1],'message':row[2]})
    con.commit()
    con.close()
    return items

def get_specific_logs(filter):
    con = sqlite3.connect('ALERT_DB.db')
    cur = con.cursor()
    statement = """SELECT * FROM ALERTS WHERE """ + filter
    print(statement)
    cur.execute(statement)
    output = cur.fetchall()
    items = []
    for row in output:
        items.append({'timestamp':row[0],'rule_name':row[1],'message':row[2]})
    con.commit()
    con.close()
    return items
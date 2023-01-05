import sqlite3

def init():
    con = sqlite3.connect('ALERT_DB.db')
    cur = con.cursor()
    print('Initializing connection...')
    listOfTables = cur.execute("""SELECT name FROM sqlite_master WHERE type='table' AND name='ALERTS'; """).fetchall()
    if listOfTables == []:
            cur.execute("""CREATE TABLE ALERTS(DATE CHAR(10),TIME VARCHAR(12), RULE_NAME VARCHAR(20), MESSAGE VARCHAR(250));""")
            print('Connection with database initialized')
    else:  
            print('Connection with database initialized')
    con.commit()
    con.close()

def insert_log(date, time, rule_name, message):
    con = sqlite3.connect('ALERT_DB.db')
    cur = con.cursor()
    data = (date, time, rule_name, message)
    statement = """INSERT INTO ALERTS(DATE, TIME, RULE_NAME, MESSAGE) VALUES(?, ?, ?, ?)"""
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
        items.append({'date':row[0], 'time':row[1],'rule_name':row[2],'message':row[3]})
    con.commit()
    con.close()
    return items

def get_specific_logs(filter):
    con = sqlite3.connect('ALERT_DB.db')
    cur = con.cursor()
    statement = """SELECT * FROM ALERTS WHERE """ + filter
    cur.execute(statement)
    output = cur.fetchall()
    items = []
    for row in output:
        items.append({'date':row[0], 'time':row[1],'rule_name':row[2],'message':row[3]})
    con.commit()
    con.close()
    return items
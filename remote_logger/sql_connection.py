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

def insert_log(type, date, time, logger, module, message):
    con = sqlite3.connect('ALERT_DB.db')
    cur = con.cursor()
    data = (type, date, time, logger,module, message)
    statement = """INSERT INTO ALERTS(TYPE, DATE, TIME, LOGGER, MODULE, MESSAGE) VALUES(?, ?, ?, ?, ?, ?)"""
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
        items.append({'type':row[0], 'date':row[1], 'time':row[2],'logger':row[3],'module':row[4], 'message':row[5]})
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
        items.append({'type':row[0], 'date':row[1], 'time':row[2],'logger':row[3],'module':row[4], 'message':row[5]})
    con.commit()
    con.close()
    return items
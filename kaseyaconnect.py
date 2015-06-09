#kaseyaconnect.py
#Reusable module for connecting to the Kaseya ksubscribers database
#Kevin Greene
#Kevin@360itpartners.com
#Version 1.1
#Last revision 6/8/2015: Added configparser support

import pyodbc
import configparser

def ResultIter(cursor, arraysize=1):
    #An iterator that uses fetchmany to keep memory usage down
    while True:
        results = cursor.fetchmany(arraysize)
        if not results:
            break
        for result in results:
            yield result

config = configparser.RawConfigParser()
config.read(r'config\settings.cfg')
un = config.get("Settings", "username")
pw = config.get("Settings", "password")
dbsvr = config.get("Settings", "kserver")
db = config.get("Settings", "database")

cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=%s;DATABASE=%s;UID=%s;PWD=%s' % (dbsvr,db,un,pw)) #Connect to the Kaseya SQL DB
cursor = cnxn.cursor()

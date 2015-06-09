#getguids.py
#Get server names and GUIDs for Kaseya backupse
#Kevin Greene
#Kevin@360itpartners.com
#Version 1.0
#Last revision 6/5/2015

from kaseyaconnect import *

#SQL Query against Kaseya's vBackuplog view in the ksubscribers database         
cursor.execute("select DISTINCT Machine_GroupID, agentGuid from vBackupLog order by Machine_GroupID asc")

f = open(r'output\agentguids.csv','w')
f.write("Machine_GroupID,agentGuid\n")
for result in ResultIter(cursor):
    f.write(result[0] + "," + str(result[1]) + "\n")
f.close()

#24hrlogs.py
#Get last 24hrs of backup logs from Kaseya
#Kevin Greene
#kevin@360itpartners.com
#Version 1.0
#Last Revision 6/5/2015

from kaseyaconnect import *
import datetime
#SQL Query against Kaseya's vBackuplog view in the ksubscribers database
cursor.execute("select * from vBackupLog where EventTime > DateAdd(DAY, -1, GETDATE()) order by EventTime desc")

logfile = "output\KaseyaBackupLogs-Last 24hrs-%s.html" % datetime.datetime.now().strftime("(%m-%d-%Y %H-%M)")
f = open(logfile ,'w')
f.write("<head><script src=\"sorttable.js\"></script></head>")
f.write("<table class=\"sortable\" style=\"width:100%\">")
f.write("<tr><th>Machine_GroupID</th><th>agentGuid</th><th>machName</th><th>groupName</th><th>EventTime</th><th>description</th><th>durationSece</th><th>statusType</th><th>result</th><th>imageSize</th></r>")

for result in ResultIter(cursor):
    f.write("<tr>")
    f.write("<td>%s</td>" % result[0])
    f.write("<td>%s</td>" % result[1])
    f.write("<td>%s</td>" % result[2])
    f.write("<td>%s</td>" % result[3])
    f.write("<td>%s</td>" % result[4])
    f.write("<td>%s</td>" % result[5])
    f.write("<td>%s</td>" % result[6])
    f.write("<td>%s</td>" % result[7])
    f.write("<td>%s</td>" % result[8])

f.write("</table>")    
f.close()

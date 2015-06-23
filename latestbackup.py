#latestbackup.py
#Get latest backup for each server
#Kevin Greene
#kevin@360itpartners.com
#Version 1.0
#Last Revision 6/8/2015

from kaseyaconnect import *
import datetime

count=0
#SQL Query against Kaseya's vBackuplog view in the ksubscribers database
cursor.execute("select Machine_Groupid, EventTime, description, imageSize, durationSec, result from vBackuplog as t1 where EventTime = (select max(EventTime) from vBackupLog where t1.Machine_groupid =vBackuplog.Machine_groupid) AND result = 1 order by EventTime desc")
logfile = "output\Latest Backup Check\KaseyaLatestBackup-%s.html" % datetime.datetime.now().strftime("(%m-%d-%Y %H-%M)")
f = open(logfile ,'w')
f.write("<head><script src=\"..\sorttable.js\"></script></head>")
f.write("<table class=\"sortable\" style=\"width:100%\">")
f.write("<tr><th>Machine_GroupID</th><th>EventTime</th><th>description</th><th>imageSize</th><th>durationSec</th><th>result</th></r>")

for result in ResultIter(cursor):
    f.write("<tr>")
    f.write("<td>%s</td>" % result[0])
    f.write("<td>%s</td>" % result[1])
    f.write("<td>%s</td>" % result[2])
    f.write("<td>%s</td>" % result[3])
    f.write("<td>%s</td>" % result[4])
    f.write("<td>%s</td>" % result[5])
    count = count + 1

print "Count is %s" % count



f.write("</table>")    
f.close()

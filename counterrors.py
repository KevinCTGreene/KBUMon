#counterrors.py
#Count the number of backup failures per endpoint
#Kevin Greene
#kevin@360itpartners.com
#Version 1.0
#Last Revision 6/11/2015

from kaseyaconnect import *
import datetime

count=0
#SQL Query against Kaseya's vBackuplog view in the ksubscribers database
cursor.execute("select Machine_Groupid, count(result) from vBackuplog where result = 0 AND eventtime > '2015/04/01' group by Machine_Groupid order by count(result) desc")
logfile = "output\Failures Per Endpoint\FailuresPerEndpoint-%s.html" % datetime.datetime.now().strftime("(%m-%d-%Y %H-%M)")
f = open(logfile ,'w')
f.write("<head><script src=\"sorttable.js\"></script></head>")
f.write("<table class=\"..\sortable\" style=\"width:100%\">")
f.write("<tr><th>Machine_GroupID</th><th>Total Failures</th>")

for result in ResultIter(cursor):
    f.write("<tr>")
    f.write("<td>%s</td>" % result[0])
    f.write("<td>%s</td>" % result[1])
f.write("</table>")    
f.close()

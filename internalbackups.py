#internalbackups.py
#Get last week of internal backup logs from Kaseya
#Kevin Greene
#kevin@360itpartners.com
#Version 1.0
#Last Revision 6/9/2015

from kaseyaconnect import *
import datetime
import os
import csv
from collections import defaultdict
import operator

class backedupserver():
        def __init__(self, guid, name, setlist, path, ):
            self.g = guid
            self.n = name
            self.s = setlist
            self.p = path
            self.newestbackup = "Newest backup not processed."
            self.newest()
        def info(self):
            o.write("Name: %s" % self.n)
            o.write("     GUID: %s" % self.g)
            o.write("     Path is: %s" % self.p)
            o.write("sets are:")
            for x in self.s: #go through list. list consists of dictionaries
                    for key in x: #each key is a set name, value is a list.
                            o.write( "set %s" % key) #set name
                            for y in x[key]: #list consists of dicts which represent TIB files.
                                    o.write("tib name is %s last modified %s" % (y["filename"],y["timestamp"]))                                  
        def newest(self):
            self.newestbackup = datetime.datetime(1900,1,1)  
            for x in self.s: #go through list. list consists of dictionaries
                    for key in x: #each key is a set name, value is a list.
                            #o.write( "set %s" % key #set name
                            for y in x[key]: #list consists of dicts which represent TIB files.
                                    #print "time stamp is %s" % y["timestamp"]
                                    #print "newestbackup is %s" % self.newestbackup
                                    if y["timestamp"] > self.newestbackup:
                                            self.newestbackup = y["timestamp"]

#SQL Query against Kaseya's vBackuplog view in the ksubscribers database
cursor.execute("select * from vBackupLog where EventTime > DateAdd(DAY, -7, GETDATE()) AND (groupname LIKE '%360%' OR Machine_GroupID LIKE '%kaseya%') order by EventTime desc")
#cursor.execute("select machine_groupid, avg(imagesize) from vBackupLog group by machine_groupid order by avg(imagesize)")

oldestserver = ""
serverlist = []
full_list=[]
names_and_guids = []
servers=[]
count=0
logfile = "output\InternalBackupLogs-Last7Days-%s.html" % datetime.datetime.now().strftime("(%m-%d-%Y %H-%M)")
o = open(logfile ,'w')
o.write("<head><script src=\"sorttable.js\"></script></head>")
o.write("<table class=\"sortable\" style=\"width:100%\">")
o.write("<tr><th>Machine_GroupID</th><th>agentGuid</th><th>EventTime</th><th>description</th><th>duration(sec)</th><th>statusType</th><th>result</th><th>imageSize</th></r>")

for result in ResultIter(cursor):
    o.write("<tr>")
    o.write("<td>%s</td>" % result[0])
    o.write("<td>%s</td>" % result[1])
    o.write("<td>%s</td>" % result[4])
    o.write("<td>%s</td>" % result[5])
    o.write("<td>%s</td>" % result[6])
    o.write("<td>%s</td>" % result[7])
    o.write("<td>%s</td>" % result[8])
    o.write("<td>%s</td>" % result[9])

o.write("</table>")    
             
o.write("<div align=center><h1>Offsite Backup Check</h1><h2>%s</h2></div>" % datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
o.write("<head><script src=\"sorttable.js\"></script></head>")

with open(r'output\agentguids.csv','r') as csvfile:
        spamreader = csv.reader(csvfile)
        for row in spamreader:
                        full_list.append(row[0])
                        names_and_guids.append(row)
                                            
with open('config\internalpaths.csv', 'rb') as f:
    reader = csv.reader(f)
    o.write("<h2>Backup location check:</h2>")
    for l in reader:
                if os.path.isdir(l[0]):
                    servers.append(l[0])
                    o.write("%s is accessible<br>" % l[0])
                else:
                    o.write("%s is not accessible<br>" % l[0])
                    servers.append(l[0])

for l in servers:
      for root, dirs, files in os.walk(l):        
        if os.path.basename(root) == "VolBackup" or os.path.basename(root) == "FldrBackup" :
            sID = os.path.basename(os.path.dirname(root))
            path = os.path.dirname(os.path.dirname(root))
            servername = [x[0] for x in names_and_guids if x[1] == sID][0]
               
            setlist=[]
            for d in dirs:
                backupset = defaultdict()
                backupset[d]=[]
                
                for a,b,c in os.walk(os.path.join(root,d)):
                        #print "Walking through %s" % a
                        #a=root
                        #b=dirs
                        #c=files
                        
                        for f in c:
                                if os.path.splitext(f)[1] == ".TIB":

                                        stamp = datetime.datetime.fromtimestamp(os.path.getctime(os.path.join(a, f)))
                                        tibfile=defaultdict()
                                        tibfile["filename"] = f
                                        tibfile["timestamp"] = stamp
                                        backupset[d].append(tibfile)

                setlist.append(backupset)
            serverlist.append(backedupserver(sID[:-2], servername, setlist, path))
            
dest = ("",datetime.datetime.today())
serverlist.sort(key=operator.attrgetter("newest"), reverse=False)

#Comparison section
#Checks offsite servers found against a list of all servers. Reports those which are missing.
o.write("<br><h2>Number of servers processed: %s</h2><br>" % len(serverlist))
o.write("<table class=\"sortable\" style=\"width:100%\">")
o.write("<tr><th>Server Name</th><th>Path</th><th>Newest Backup</th></r>")

for s in serverlist:
     if s.n in full_list:
             full_list.remove(s.n)
     o.write("<tr>")
     o.write("<td>%s</td>" % s.n)
     o.write("<td>%s</td>" % s.p)
     o.write("<td>%s</td>" % s.newestbackup)   
     o.write("</tr>")

o.write("</table>")

o.close()

        

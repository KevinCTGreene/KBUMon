#offsitecheck.py
#Look through Kaseya backup directories and produce a report
#Kevin Greene
#kevin@360itpartners.com
#Version 2.0
#Last Revision 6/8/2015 - Changed logfile logation

import os
import datetime
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
                        
oldestserver = ""
serverlist = [] 
servers=[]
count=0
logfile = "output\KaseyaBackupLogs-Offsite Backups-%s.html" % datetime.datetime.now().strftime("(%m-%d-%Y %H-%M)")
o = open(logfile ,'w')
o.write("<div align=center><h1>Offsite Backup Check</h1><h2>%s</h2></div>" % datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
o.write("<head><script src=\"sorttable.js\"></script></head>")
                                            
with open('config\paths.csv', 'rb') as f:
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
#if True:
     #print l
     #for root, dirs, files in os.walk(r'C:\Users\kevin.360ITPARTNERS\Dropbox\Programming\Python\_tests\UNC'):
     for root, dirs, files in os.walk(l):        
        if os.path.basename(root) == "VolBackup":
            path = os.path.dirname(os.path.dirname(root))
            sID = os.path.basename(path) + " ="

            for h, j ,k in os.walk(os.path.dirname(path)):
                #h=root   
                #j=dirs
                #k=files
                for v in j: 
                        if sID in v:
                            i = sID.find("=") 
                            servername = v[i+2:]

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

o.write("<br><h2>Number of servers processed: %s</h2><br>" % len(serverlist))
o.write("<table class=\"sortable\" style=\"width:100%\">")
o.write("<tr><th>Server Name</th><th>Path</th><th>Newest Backup</th></r>")

full_list= []
with open(r'output\agentguids.csv','r') as csvfile:
        spamreader = csv.reader(csvfile)
        for row in spamreader:
                        full_list.append(row[0])
                        

for s in serverlist:
     if s.n in full_list:
             full_list.remove(s.n)
     o.write("<tr>")
     o.write("<td>%s</td>" % s.n)
     o.write("<td>%s</td>" % s.p)
     o.write("<td>%s</td>" % s.newestbackup)   
     o.write("</tr>")

o.write("</table>")
o.write("<h1>")
o.write("Number of servers found: %s<br>" % len(serverlist))
o.write("Number of server missing: %s<br>" % len(full_list))
o.write("List of missing servers:<br>")
o.write("</h1>")
o.write("<i>Servers could be missing because the client has their own offsite backup location, offsite misconfiguration, error when scanning backup directories, it is a backup server, or they are not using offsite backups.</i><br>")
for srv in full_list:
        o.write("%s<br>" % srv)
o.close()

        



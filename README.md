# KBUMon
A set of tools to monitor Kaseya Backups (KBU).

This is a set of Python tools to monitor Kaseya Backups. I found the backup logging facility within Kaseya to be labor intensive and lacking in certain monitoring functions. There are several conditions which the basic alerting falls short, including not alerting skipped backups and not alerting when backups have not occurred for X number of days. The ultimate goal is to simplify the life of a KBU administrator and identify silent failures of the backup and offsite replication system.

Kaseya provides a special Database View called vBackuplogs which can be used to directly pull backup logs. 
Once the logs are accessible there are several Python scripts to do various things with them.

Here is an article from Kaseya on how to configure access to the DB: http://help.kaseya.com/webhelp/en/vsa/6010000/index.htm?toc.htm?532.htm

There is also a script to scan UNC paths on the network which house offsite backups (in an MSP datacenter environment).



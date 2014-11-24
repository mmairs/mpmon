#!/usr/bin/python
import socket
import cgi
print "Content-type: text/html\n\n"
print """
<html><head>
<link rel="stylesheet" type="text/css" href="/css/main.css">
<title>MPythonMon</title></head><body>
"""
with open ("SVCs") as f:
  c=f.readlines()
  for t in c:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s=t.partition(',')
    h=s[0]
    p=int(s[2])
    result = sock.connect_ex((h,p))
    if result == 0:
      print "<span class='goodstat'> {} {}</span><br>".format(h,p)
    else:
      print "<span class='badstat'> {} {}</span><br>".format(h,p)
    sock.close()
f.close()
print "</body></html>"

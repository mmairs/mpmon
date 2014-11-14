#!/usr/bin/python
import socket;
print "Content-type: text/html\n\n"
print "<html><head><title>MPythonMon</title></head><body>"
with open ("SVCs") as f:
  c=f.readlines()
  for t in c:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s=t.partition(',')
    h=s[0]
    p=int(s[2])
    print h,p
    result = sock.connect_ex((h,p))
    if result == 0:
      print " is open<br>"
    else:
      print " is not open<br>"
    sock.close()
f.close()
print "</body></html>"

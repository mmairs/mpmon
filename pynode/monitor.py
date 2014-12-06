#!/usr/bin/python
import socket
import requests
import cgi
import timeit

print "Content-type: text/html\n\n"
print """
<html><head>
<link rel="stylesheet" type="text/css" href="/css/main.css">
<title>MPythonMon</title></head><body>
<h2 style='text-align:center'>New York</h2>
"""

def rdr(fn):
  with open (fn) as f:
    c=f.readlines()
    return c
  f.close

def S():
  print """
<div style='width:50%;float:left'>
<h3>Services</h3>
"""
  c=rdr ("SVCs")
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
  print "</div>"

def U():
  print """
<div style='width:50%;float:right'>
<h3>Sites</h3>
"""
  c=rdr ("URLs")
  for l in c:
    s=l.partition(',')
    u='http://'+s[0]
    m=s[2]
    r = requests.get(u)
    r.encoding = 'utf-8'
    t = r.elapsed.total_seconds()
    if r.status_code == 200:
      if r.text.find(m):
        print("<span class='goodstat'> {0}:{1:1.1f}s</span><br>".format(s[0],t))
      else:
        print "<span class='misstat'> {}!~{}</span><br>".format(u,m)
    else:
      print "<span class='badstat'> {} {}</span><br>".format(u,r.status_code)
  print "</div>"

def main():
  S()
  U()

main()
print "</body></html>"

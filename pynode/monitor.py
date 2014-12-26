#!/usr/bin/python
import socket
import requests
import cgi
import timeit
import re

print "Content-type: text/html\n\n"
print """
<html><head>
<link rel="stylesheet" type="text/css" href="/node/css/main.css">
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
    result = -1
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s=t.partition(',')
    h=s[0]
    p=int(s[2])
    try:
      result = sock.connect_ex((h,p))
      sock.close()
    except:
      print "<span style='text-decoration:line-through' class='badstat'> {}</span><br>".format(h)
      continue
    if result == 0:
      print "<span class='goodstat'> {} {}</span><br>".format(h,p)
    else:
      print "<span class='badstat'> {} {}</span><br>".format(h,p)
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
    try:
      r = requests.get(u)
      r.encoding = 'utf-8'
      t = r.elapsed.total_seconds()
    except:
      print "<span style='text-decoration:line-through' class='badstat'> {}</span><br>".format(u)
      continue
    if r.status_code == 200:
      x = r.text
#      print m in x
      #if m in r.text:
      #if r.text.find(m)>0:
      if re.search(m,x):
        print "<a class='goodstat' href='{0}'>{1}:{2:1.1f}s</a><br>".format(u,s[0],t)
      else:
        print "<a class='misstat' href={0}>{1}!~{2}</a><br>".format(u,s[0],m)
    else:
      print ("<a class='badstat' href={0}> {1} {2}</a><br>".format(u,s[0],r.status_code))
  print "</div>"

def main():
  S()
  U()

main()
print "</body></html>"

#!/usr/bin/python
import socket
import requests
import cgi
import timeit
import re

print "Content-type: text/html\n\n"
print """
<html><head>
<link rel="stylesheet" type="text/css" href="http://www.mpmon.com/node/css/main.css">
<title>MPythonMon</title></head><body>
<h2 style='text-align:center'>New York</h2>
"""

def rdr(fn):
  r = requests.get('http://www.mpmon.com/node/'+fn,headers={'User-Agent':'mpmon'})
  c = r.text.split('\n')
  return c

def S():
  print """
<h3>Services</h3>
"""
  c=rdr ("SVCs")
  for t in c:
    result = -1
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s=t.partition(',')
    h=s[0]
    try:
      p=int(s[2])
    except:
      continue
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

def U():
  print """
<h3>Sites</h3>
"""
  c=rdr ("URLs")
  for l in c:
    if len(l) == 0:
      break
    s=l.partition(',')
    u='http://'+s[0]
    m=s[2]
    try:
      r = requests.get(u,headers={'User-Agent':'mpmon'})
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
        print "<a class='misstat' href='{0}'>{1}!~{2}</a><br>".format(u,s[0],m)
    else:
      print ("<a class='badstat' href='{0}'> {1} {2}</a><br>".format(u,s[0],r.status_code))

def main():
  S()
  U()

main()
print "</body></html>"

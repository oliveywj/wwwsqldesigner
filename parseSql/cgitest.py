#!/usr/bin/env python

import cgi
import cgitb    #show error on webbrowser when error occurs
cgitb.enable()

print("Content-type: text/html\n")    #\n : unless, Internal Server Error!

print('<html>')
print('<head>')
print('<title>Hello Word - First CGI Program</title>')
print('</head>')
print('<body>')

form = cgi.FieldStorage()

print("success!")

print('</body>')
print('</html>')
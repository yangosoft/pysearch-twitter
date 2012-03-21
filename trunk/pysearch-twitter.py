#!/usr/bin/python

import urllib
import json
import sys


search="android"
if (len(sys.argv) != 1):
  search = urllib.quote(sys.argv[1])


url="http://search.twitter.com/search.json?q="+search

webFile = urllib.urlopen(url)
response=webFile.read()
webFile.close()

#print response
tw = json.loads(response)


print "Twitts: " + urllib.unquote(search)
print ""
for i in tw['results']:
 print i['from_user_name']+":\t" + i['text']
 print ""


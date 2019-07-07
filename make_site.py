#!/usr/bin/python

import urllib2
import json
import sys
import re

url = sys.argv[1]

p = re.compile(".*/card/([^/]*/[0-9]*).*")
id = p.match(url).group(1)
api_url = "https://api.scryfall.com/cards/" + id

print api_url

response = json.loads(urllib2.urlopen(api_url).read())

name = response["name"]
img = response["image_uris"]["normal"]

print name
print img

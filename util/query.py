#!/bin/env python2

import requests
import json
import time
from datetime import datetime

INDEX_URL = 'https://seidenstrasse.sebastians-site.de/index.json'

def parse_remote_json(url):
	resp = requests.get(url=url,verify=False)
	print "Getting %s" % url
	#print resp.content
	try:
		return json.loads(resp.content)
	except Exception, e:
		print "Can't parse !"
		return []


def print_event(event):
	print "%s -> %s %s %s" % (event['start'], event['end'], event['velocity'], str(datetime.fromtimestamp(event['time']))) 


index = parse_remote_json(INDEX_URL)

print index


data = []
for url in index:
	data += parse_remote_json(url)

data = filter(lambda x: x['velocity'] < 12, data)

fastest = sorted(data, key=lambda x: x['velocity'], reverse=True)[0:20]
slowest = sorted(data, key=lambda x: x['velocity'])[0:20]

print "fastest:"
for event in fastest:
	print_event(event)

print "slowest:"
for event in slowest:
	print_event(event)

print "average:"
avg = 0
for event in data:
	avg += event['velocity'] / len(data)

print avg

print "Cbase in: %d"  % len(filter(lambda x: x['end'] == "Cbase", data))
print "Cbase out: %d" % len(filter(lambda x: x['start'] == "Cbase", data))



#!/bin/env python2
import json
import os
from datetime import datetime

from dbmanager import DBManager

def print_event(event):
	print "%s -> %s %s %s" % (event['start'], event['end'], event['velocity'], str(datetime.fromtimestamp(event['time'])))


dbman = DBManager("dbname=zaehlrohr user=zaehlrohr", "30C3")


for subdir, _, files in os.walk("./old_data"):
	for filename in files:
		filepath = os.path.join(subdir, filename)
		print "Reading file %s" % filepath
		json_file = open(filepath)
		for event in json.load(json_file):
			print_event(event)
			new_event = {
				'origin' : event['start'], 
				'destination' : event['end'], 
				'velocity' : event['velocity'],
				'time' : event['time']}
			dbman.insert_event(new_event)

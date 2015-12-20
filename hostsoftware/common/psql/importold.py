#!/bin/env python2
import json
import os
from datetime import datetime

from dbmanager import DBManager

def print_event(event):
	print "%s -> %s %s %s" % (event['origin'], event['destination'], event['velocity'], str(datetime.fromtimestamp(event['time'])))

OLD_PATH = "./old_data"

for filename in os.listdir(OLD_PATH):
	filepath = os.path.join(OLD_PATH, filename)
	if os.path.isfile(filepath):
		dbman = None
		print "Reading file %s" % filepath
		json_file = open(filepath)
		for event in json.load(json_file):
			print_event(event)

			if dbman == None:
				dbman = DBManager("dbname=zaehlrohr user=zaehlrohr", event['event'])

			new_event = {
				'origin' : event['origin'],
				'destination' : event['destination'],
				'velocity' : event['velocity'],
				'time' : event['time']}
			dbman.insert_event(new_event)

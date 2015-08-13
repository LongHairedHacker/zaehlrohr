#!/bin/env python2

class Config(object):
	serialdevice = "/dev/zaehlrohr"
	baudrate = 38400
	timeout = 0.100 	#100ms
	resync_threshold = 5

	eventname = "CCCAMP2015"
	connection_string = "dbname=zaehlrohr user=zaehlrohr"

	distance = 0.5
	tubes = [('CentralNode', 'FoodHackingVillage'), 
				('CentralNode', 'metalab'),
				('CentralNode', 'Roadside'),
				('CentralNode', 'Milliways')]






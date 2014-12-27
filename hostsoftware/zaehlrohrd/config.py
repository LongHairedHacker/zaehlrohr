#!/bin/env python2

class Config(object):
	serialdevice = "/dev/ttyUSB0"
	baudrate = 38400
	timeout = 0.100 	#100ms
	resync_threshold = 5

	eventname = "31C3"
	connection_string = "dbname=zaehlrohr user=zaehlrohr"

	distance = 0.5
	tubes = [('CentralNode', 'HardwareHackingArea'), 
				('CentralNode', 'SoftwareAndOpenSource'),
				('CentralNode', 'Comix'),
				('CentralNode', 'Milliways'),
				('CentralNode', 'fail0verflow'),
				('CentralNode', 'BallPit')]






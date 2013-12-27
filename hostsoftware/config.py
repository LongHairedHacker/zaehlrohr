#!/bin/env python2

class Config(object):
	serialdevice = "/dev/ttyUSB0"
	baudrate = 38400
	timeout = 0.100 	#100ms
	resync_threshold = 5

	json_log = "Dummy"

	distance = 0.5
	tubes = [('Test1','Test2'), ('Test1','Test3')]
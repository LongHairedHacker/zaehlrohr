#!/bin/env python2

class Config(object):
	serialdevice = "/dev/ttyUSB0"
	baudrate = 38400
	timeout = 0.100 	#100ms
	resync_threshold = 5

	eventname = "31C3"
	connection_string = "dbname=zaehlrohr user=zaehlrohr"

	distance = 0.5
	tubes = [('Test1','Test2'), ('Test1','Test3')]

	flipdot_hosts = [("2001:67c:20a1:1063:ba27:ebff:fe86:8697",2323),
					("2001:67c:20a1:1063:ba27:ebff:fe23:60d7", 2323),
					("2001:67c:20a1:1063:ba27:ebff:fe71:dd32", 2323)]
	flipdot_size=(144, 120)
	flipdot_transposed = True







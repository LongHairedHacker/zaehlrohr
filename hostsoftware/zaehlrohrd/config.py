#!/bin/env python2


SERIAL_DEVICE = "/dev/ttyUSB1"

EVENT_NAME = "33C3_Test"
CONNECTION_STRING = "dbname=zaehlrohr user=zaehlrohr"



NODE_NAMES = {
	1 : "Seidenstrasse",
	2 : "Spacestation",
	3 : "Eingang",
	4 : "Sendezentrum",
	5 : "Wizzard",
	6 : "Kidspace",
	7 : "Coffeenerds",
	8 : "Lounge",
	9 : "Foodhacker",
	10 : "Monolith",

	11 : "Alice",
	12 : "Betty",
	13 : "Caty"
}

NODE_DISTANCES = [
	(11, 1, 0.0),
	(11, 2, 0.0),
	(11, 12, 50.0),
	(12, 4, 3.0),
	(12, 3, 50.0),
	(12, 13, 80.0),
	(13, 5, 30.0),
	(13, 6, 150.0),
	(13, 7, 200.0),
	(13, 8, 120.0),
	(13, 9, 150),
	(13, 10, 0.0),
]

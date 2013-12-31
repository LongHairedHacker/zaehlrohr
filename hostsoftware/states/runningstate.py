#!/bin/env python2

import time
import json

from flipdot.FlipdotMatrix import FlipdotMatrix
from state import State
from config import Config

class RunningState(State):
	name = "running"

	def __init__(self, logfile):
		logfile = "%s_%d.json" % (logfile, int(time.time()))
		self.json_log = open(logfile,'w', 0)
		self.first_log_entry = True

		self.flipdot = FlipdotMatrix(Config.flipdot_hosts, Config.flipdot_size, Config.flipdot_transposed)

	def switch_to(self):
		pass

	def _send_to_flipdot(self,event):
    	text =  " Seidenstrasse update\n"
    	text += "======================\n"
    	text += "Capsule meta data:\n"
    	text += "  from: %s\n" % str(event['start'])
    	text += "  to: %s\n" % str(event['end'])
    	text += "  velocity: %s\n" % str(event['velocity'])
    	text += "  timestamp: %s\n" % str(event['time'])
    	text += "\n\n"
    	text += "Brought to you by:\n"
    	text += "ChoasInKL and muCCC\n"

		self.flipdot.showText(text)
		print "Send to flipdot"


	def execute(self):
		line = self.serial.readline().strip()
		if line != "" :
			print "Running received: %s" % line
			if line.startswith("Capsule"):
				self.serial.write("Ack\n")
				parts = line.split(" ")

				event = {}

				event["time"] = int(parts[2])

				tube = Config.tubes[int(parts[1])]
				if parts[3] == "OneToTwo":
					event["start"] = tube[0]
					event["end"] = tube[1]
				else:
					event["start"] = tube[1]
					event["end"] = tube[0]

				
				event["velocity"] = Config.distance / int(parts[4]) * 1000

				if abs(event["time"] - int(time.time())) > Config.resync_threshold:
					self.statemachine.switch_state("outofsync")

				self._send_to_flipdot(event)

				event_json = json.dumps(event)
				if self.first_log_entry:
					self.json_log.write("[\n%s,\n]" % event_json)
					self.first_log_entry = False
				else:
					self.json_log.seek(-1,2)
					self.json_log.write("%s,\n]" % event_json)

#!/bin/env python2

import time
import json

from state import State
from config import Config

class RunningState(State):
	name = "running"

	def __init__(self, outputs):
		self.outputs = outputs

	def switch_to(self):
		pass

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
					event["origin"] = tube[0]
					event["destination"] = tube[1]
				else:
					event["origin"] = tube[1]
					event["destination"] = tube[0]

				
				event["velocity"] = Config.distance / int(parts[4]) * 1000

				if abs(event["time"] - int(time.time())) > Config.resync_threshold:
					self.statemachine.switch_state("outofsync")

				for output in self.outputs:
					output.process_event(event)

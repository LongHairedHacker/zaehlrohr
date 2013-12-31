#!/bin/env python2

import time

from state import State

class OutOfSyncState(State):
	name = "outofsync"

	def switch_to(self):
		self.serial.write("Set %s\n" % str(int(time.time())))


	def execute(self):
		line = self.serial.readline().strip()
		print "Sync received: %s" % line

		if line == "Sync ack":
			self.statemachine.switch_state("running")
		else:
			self.serial.write("Set %s\n" % str(int(time.time())))
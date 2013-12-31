#!/bin/env python2

from state import State

class ResetState(State):
	name = "reset"

	def switch_to(self):
		self.serial.write("Reset\n")


	def execute(self):
		line = self.serial.readline().strip()

		print "Reset received: %s" % line

		if line == "Reset ack":
			self.statemachine.switch_state("outofsync")
		else:
			self.serial.write("Reset\n")
#!/bin/env python2

class State(object):
	name = "BasicState"

	def switch_to(self):
		pass

	def execute(self):
		pass

	def set_serial(self,serial):
		self.serial = serial

	def set_statemachine(self, statemachine):
		self.statemachine = statemachine

	def set_config(self, config):
		self.config = config

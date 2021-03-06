#!/bin/env python2

class StateMachine(object):
	def __init__(self,serial):
		self.serial = serial
		self.states = {}
		self.current_state = None

	def register_state(self, state):
		state.set_statemachine(self)
		state.set_serial(self.serial)
		self.states[state.name] = state

	def execute(self):
		return self.states[self.current_state].execute()

	def switch_state(self, statename):
		self.current_state = statename
		self.states[self.current_state].switch_to()


		
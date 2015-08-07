#!/usr/bin/env python2

from flipdot import FlipdotMatrix

from config import Config

class Flipdot(object):
	def __init__(self):
		self.flipdot = FlipdotMatrix(Config.flipdot_hosts, Config.flipdot_size, Config.flipdot_transposed)

	def process_event(self, event):
		text =  "Seidenstrasse update\n"
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

		





#!/usr/bin/env python2

import sys
sys.path.append('../common/psql')

from config import Config
from dbmanager import DBManager

class PsqlOutput(object):
	def __init__(self):
		self.dbman = DBManager(Config.connection_string, Config.eventname)
	
	def process_event(self, event):
		self.dbman.insert_event(event, Config.eventname)
		





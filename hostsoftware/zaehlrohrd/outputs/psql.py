#!/usr/bin/env python2

import sys
sys.path.append('../common/psql')

from config import Config
from dbmanager import DBManager

class PsqlOutput(object):
	def __init__(self):
		dbman = DBManager(Config.connection_string, Config.eventname)
	
	def process_event(self, event):
		dbman.insert(event, Config.eventname)
		





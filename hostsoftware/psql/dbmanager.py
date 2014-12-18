#!/bin/env python2
import psycopg2
from datetime import datetime

class DBManager(object):
	STATEMENTS = {
		'insert_event' : "INSERT INTO capsules (event, origin, destination, time, velocity) "
		 				+ "VALUES ($1,$2,$3,$4,$5)"
	}

	def __init__(self, connectionString, eventname):
		self.conn = psycopg2.connect(connectionString)
		self.default_eventname = eventname
		
		cur = self.conn.cursor()
		for name, query in self.STATEMENTS.items():
			cur.execute("PREPARE %s AS %s" % (name, query))

	def insert_event(self, event, eventname=None):
		if not eventname:
			eventname = self.default_eventname

		time = datetime.fromtimestamp(event['time'])
		cur = self.conn.cursor()
		cur.execute("execute insert_event (%s, %s, %s, %s, %s)",
					(eventname, event['origin'], event['destination'], time, event['velocity']))
		self.conn.commit()
		

		
	
	


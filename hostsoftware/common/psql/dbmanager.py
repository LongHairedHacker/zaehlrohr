#!/bin/env python2
import psycopg2
from datetime import datetime

class DBManager(object):
	STATEMENTS = {
		'insert_event' : "INSERT INTO capsules (event, origin, destination, time, velocity) "
		 				+ "VALUES ($1,$2,$3,$4,$5)",
		
		'get_hourly_summaries' : "SELECT * FROM hourly_summary WHERE event = $1 ORDER BY time",
		'get_hourly_node_summaries' : "SELECT * FROM hourly_summary WHERE event = $1 AND node = $2 ORDER BY time",
		'get_hourly_interval_summaries' : "SELECT * FROM hourly_summary WHERE event = $1 AND time = date_trunc('hour', $2::timestamp) ORDER BY time",
		'get_hourly_summary' : "SELECT * FROM hourly_summary WHERE event = $1 AND node = $2 AND time = date_trunc('hour', $3::timestamp)",
		
		'get_daily_summaries' : "SELECT * FROM daily_summary WHERE event = $1 ORDER BY time",
		'get_daily_node_summaries' : "SELECT * FROM daily_summary WHERE event = $1 AND node = $2 ORDER BY time",
		'get_daily_interval_summaries' : "SELECT * FROM daily_summary WHERE event = $1 AND time = date_trunc('day', $2::timestamp) ORDER BY time",
		'get_daily_summary' : "SELECT * FROM daily_summary WHERE event = $1 AND node = $2 AND time = date_trunc('day', $3::timestamp)",

		'get_node_capsules' : "SELECT * FROM capsules WHERE event = $1 AND (origin = $2 OR destination = $2) ORDER BY time",
		'get_all_capsules' : "SELECT * FROM capsules WHERE event = $1 ORDER BY time",
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
		cur.execute("EXECUTE insert_event (%s, %s, %s, %s, %s)",
					(eventname, event['origin'], event['destination'], time, event['velocity']))
		self.conn.commit()


	def _summary_to_dictionary(self, summary):
		keys = ['event', 'time', 'node', 
				'incoming', 'outgoing', 'overall', 
				'in_avg_velocity', 'out_avg_velocity', 'avg_velocity',
				'in_min_velocity', 'out_min_velocity', 'min_velocity',
				'in_max_velocity', 'out_max_velocity', 'max_velocity']

		result = {}
		for i in range(0,len(keys)):
			result[keys[i]] = summary[i]

		result['time'] = int(result['time'].strftime("%s"))

		return result


	def get_summary(self, interval='hourly', node=None, timestamp=None, eventname=None):
		if not eventname:
			eventname = self.default_eventname

		if interval <> 'hourly' and interval <> 'daily' :
			raise ValueError("interval has to 'daily' or 'hourly'")

		time = None
		if timestamp :
			time = datetime.fromtimestamp(timestamp)

		query = "execute get_%s_summaries (%%s)" % interval
		values = (eventname,)
		if node and not time:
			query = "EXECUTE get_%s_node_summaries (%%s, %%s)" % interval
			values = (eventname, node)
		elif not node and time:
			query = "EXECUTE get_%s_interval_summaries (%%s, %%s)" % interval
			values = (eventname, time)
		elif node and time:
			query = "EXECUTE get_%s_summary (%%s, %%s, %%s)" % interval
			values = (eventname, node, time)

		#print query
		#print values

		cursor = self.conn.cursor()
		cursor.execute(query,values)	
		data = cursor.fetchall()
		#print "Query returned %d rows" % len(data)

		return map(self._summary_to_dictionary, data)



	def _capsule_to_dictionary(self, capsule):
		keys = ['id', 'event', 'origin', 'destination', 
				'time', 'velocity']

		result = {}
		for i in range(0,len(keys)):
			result[keys[i]] = capsule[i]

		result['time'] = int(result['time'].strftime("%s"))

		return result


	def get_capsules(self, node=None, eventname=None):
		if not eventname:
			eventname = self.default_eventname
		
		cursor = self.conn.cursor()

		if node :
			cursor.execute("EXECUTE get_node_capsules (%s, %s)", (eventname, node))
		else:
			cursor.execute("EXECUTE get_all_capsules (%s)", (eventname,))

		data = cursor.fetchall()
		return map(self._capsule_to_dictionary, data)



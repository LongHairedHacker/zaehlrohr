import sys
sys.path.append('../common/psql')

import json

from flask import Flask, abort, redirect, url_for
app = Flask(__name__)

from dbmanager import DBManager

from config import *

@app.route('/')
def index_redirect():
    return redirect(url_for('node_chart', eventname=CURRENT_EVENT, node=DEFAULT_NODE)) 


@app.route('/charts/<eventname>/<node>/')
def node_chart(eventname, node):
	return "Foobla"

@app.route('/json/<eventname>/nodes/')
@app.route('/json/<eventname>/nodes/<node>')
@app.route('/json/<eventname>/nodes/<node>/<interval>')
@app.route('/json/<eventname>/nodes/<node>/<interval>/<int:timestamp>')
def node_summaries(eventname, node=None, interval='hourly', timestamp=None):
	try:
		data = json.dumps(dbman.get_summary(interval,node,timestamp,eventname))
		return data
	except ValueError, e:
		abort(404)


@app.route('/json/<eventname>/raw/')
@app.route('/json/<eventname>/raw/<node>')
def capsules(eventname, node=None):
	data = json.dumps(dbman.get_capsules(node,eventname))
	return data



if __name__ == '__main__':
	dbman = DBManager("dbname=zaehlrohr user=zaehlrohr", CURRENT_EVENT)
	app.debug = True
	app.run()

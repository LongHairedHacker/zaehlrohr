import sys
sys.path.append('../common/psql')

import os
import json

from flask import Flask, abort, redirect, url_for, render_template
from flask_headers import headers

app = Flask(__name__)

app.static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")

from dbmanager import DBManager

from config import *

@app.route('/')
@headers({'Cache-Control':'public, max-age=360'})
def index_redirect():
    return redirect(url_for('node_chart', eventname=CURRENT_EVENT, node=DEFAULT_NODE))

@app.route('/charts/<eventname>/')
def event_redirect(eventname):
    if not eventname in NODES.keys():
        abort(404)

    return redirect(url_for('node_chart', eventname=eventname, node=NODES[eventname][0]))


@app.route('/charts/<eventname>/<node>/')
@headers({'Cache-Control':'public, max-age=360'})
def node_chart(eventname, node):
	if not eventname in NODES.keys() or not node in NODES[eventname]:
		abort(404)

	events = reversed(NODES.keys())
	return render_template('base.html', eventname=eventname, node=node, events=events, nodes=NODES)


# Json stuff
@app.route('/json/<eventname>/nodes/')
@app.route('/json/<eventname>/nodes/<node>')
@app.route('/json/<eventname>/nodes/<node>/<interval>')
@app.route('/json/<eventname>/nodes/<node>/<interval>/<int:timestamp>')
@headers({'Cache-Control':'public, max-age=60'})
def node_summaries(eventname, node=None, interval='hourly', timestamp=None):
	try:
		data = json.dumps(dbman.get_summary(interval,node,timestamp,eventname))
		return data
	except ValueError, e:
		abort(404)


@app.route('/json/<eventname>/raw/')
@app.route('/json/<eventname>/raw/<node>')
@headers({'Cache-Control':'public, max-age=60'})
def capsules(eventname, node=None):
	data = json.dumps(dbman.get_capsules(node,eventname))
	return data


if __name__ == '__main__':
	dbman = DBManager(connectionString, CURRENT_EVENT)
	app.debug = True
	app.run()

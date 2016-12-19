#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import os
import sys


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

sys.stdout = sys.stderr
# Add the virtual Python environment site-packages directory to the path
import site
site.addsitedir(os.path.join(BASE_DIR,'virtenv/lib/python2.7/site-packages'))
sys.path.insert(0,os.path.join(BASE_DIR,'virtenv/lib/python2.7/site-packages'))

from flup.server.fcgi import WSGIServer
from werkzeug.contrib.fixers import CGIRootFix
from zaehlrohr_web import app

app = CGIRootFix(app, app_root='/')
WSGIServer(app).run()

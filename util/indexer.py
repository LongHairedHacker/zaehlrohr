#!/bin/env python

import os
import json
import sys

INDEX_FOLDER = '/tmp/htdocs/'
OUTPUT_FOLDER = INDEX_FOLDER
PREFIX_URL = 'https://seidenstrasse.sebastians-site.de/'

json_files = []

for path,dirs,files in os.walk(INDEX_FOLDER):
	relpath = os.path.relpath(path,INDEX_FOLDER)
	if files != [] :
		for curfile in files:
			name, extension = os.path.splitext(curfile)
			if name != "index" and extension == ".json":
				json_files.append(PREFIX_URL + os.path.join(relpath,curfile))

json = json.dumps(json_files)
index = open(os.path.join(OUTPUT_FOLDER, 'index.json'),'w+')
if not index:
	sys.exit(1)

index.write(json)


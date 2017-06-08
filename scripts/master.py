#!/usr/bin/env python
import subprocess as sub
import requests
import json
import time
import sys
import os

BASE = "http://localhost:5000"
API_PATH = "%s/api/script_update" % BASE
API_KEY = os.environ['API_KEY']
HEADER = {'Content-Type': 'application/json'}

# First and only argument to script is the session id
SID = sys.argv[1]

def make_header(s):
    return "=" * 10 + s.upper() + "=" * 10

def update_script(progress, text):
    data = {}
    # Populate the data
    data['session_id'] = SID
    data['progress'] = progress
    data['text'] = text
    data['auth_token'] = API_KEY

    # Send post request
    resp = requests.post(API_PATH, data=json.dumps(data), headers=HEADER)

def update_progress(progress, text):
    print(text)
    update_script(progress, text)

# INITIALIZATION
update_progress(0, make_header('initializing'))

update_progress(2, 'Starting on %s' % SID)
time.sleep(10)

# CSV CONVERSION
update_progress(5, make_header('converting csv to arff'))

# TODO
time.sleep(10)

# RUNNING WEKA
update_progress(20, make_header('running weka'))

# TODO
time.sleep(10)

# WEKA RESULT PARSING
update_progress(80, make_header('parsing weka results'))

# TODO
time.sleep(10)

# RESULT GENERATION
update_progress(95, make_header('generating results'))

# TODO
time.sleep(10)

# FINISHED!
update_progress(100, make_header('finished'))


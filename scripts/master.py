#!/usr/bin/env python
import subprocess as sub
import requests
import glob
import json
import sys
import os

BASE = os.environ['BASE_URL']
API_PATH = BASE + "/api/script_update"
API_KEY = os.environ['API_KEY']
HEADER = {'Content-Type': 'application/json'}
RESULTS_DIR = 'results/'

# Initialize things that have to do with the passed-in variables
SID = sys.argv[1]
TRAINING_ABBRV = sys.argv[2]
UPLOAD_FOLDER = os.environ['UPLOAD_FOLDER']
SESSION_FOLDER = os.path.join(UPLOAD_FOLDER, SID)
SCRIPTS_FOLDER = os.environ['SCRIPTS_FOLDER']
TESTING_FN = os.environ['TESTING_FN']
TRAINING_FN = os.environ['TRAINING_FN']

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
    requests.post(API_PATH, data=json.dumps(data), headers=HEADER)

def update_progress(progress, text):
    print(text)
    update_script(progress, text)

def update_progress_wrapper(progress, p):
    update_progress(progress, str(p.stderr + b'\n' + p.stdout, 'utf-8'))

def process_return_code(p):
    if p.returncode != 0:
        update_progress(100, "Aborting...")
        sys.exit(0)

# INITIALIZATION
update_progress(0, make_header('initializing'))

update_progress(2, 'Starting on %s with %s' % (SID, TRAINING_ABBRV))

# CSV CONVERSION
update_progress(20, make_header('converting csv to arff'))

csv_script = os.path.join(SCRIPTS_FOLDER, 'toarff.py')
g = glob.glob(os.path.join(SESSION_FOLDER, '*.csv'))
starting = 20
interval = len(g) / 20.0
for f in g:
    # Convert for every csv file
    f = os.path.basename(f)
    arff_file = f.replace('.csv', '.arff')
    p = sub.run(['python', csv_script, f, '-o', arff_file],
                    stdout=sub.PIPE, stderr=sub.PIPE, cwd=SESSION_FOLDER)
    update_progress_wrapper(starting, p)
    starting += interval

    process_return_code(p)

# RUNNING WEKA
update_progress(40, make_header('running weka'))

weka_script = os.path.join(SCRIPTS_FOLDER, 'run_weka.py')

# Get training and testing filename
training = ''
testing = os.path.join(SESSION_FOLDER, TESTING_FN.replace('.csv', '.arff'))
training = os.path.join(SESSION_FOLDER, TRAINING_FN.replace('.csv', '.arff'))

# Make results directory
r_dir = os.path.join(SESSION_FOLDER, RESULTS_DIR)
os.mkdir(r_dir)

p = sub.run(['python', weka_script, training, testing, '-d', r_dir],
                stdout=sub.PIPE, stderr=sub.PIPE)
update_progress_wrapper(50, p)

process_return_code(p)

# WEKA RESULT PARSING
update_progress(60, make_header('parsing weka results'))

predict_script = os.path.join(SCRIPTS_FOLDER, 'prediction_fixer.py')
g = glob.glob(os.path.join(SESSION_FOLDER, RESULTS_DIR, '*.out.csv'))
starting = 80
interval = 10.0 / len(g)
for f in g:
    # Iterate over every single predictions file
    fn = training.replace('.arff', '.csv')
    if 'Testing' in f:
        fn = testing.replace('.arff', '.csv')
    p = sub.run(['python', predict_script, fn, f, f + '.new'],
                stdout=sub.PIPE, stderr=sub.PIPE)
    # Rename the .new file
    os.rename(f + '.new', f)
    update_progress_wrapper(starting, p)
    starting += interval

    process_return_code(p)

# RESULT GENERATION
update_progress(90, make_header('generating results'))

# Pack entire results folder into a zip
zip_out = os.path.join(SESSION_FOLDER, 'results.zip')
p = sub.run(['zip', '-r', zip_out, RESULTS_DIR],
            stdout=sub.PIPE, stderr=sub.PIPE, cwd=SESSION_FOLDER)
update_progress_wrapper(95, p)

process_return_code(p)

# FINISHED!
update_progress(100, make_header('finished'))

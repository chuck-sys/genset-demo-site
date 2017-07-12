from flask import Flask
import pyrebase
import json
from glob import glob
from os.path import join, basename

app = Flask(__name__)

try:
    app.config.from_object('config')
except ImportError:
    app.config.from_object('test_config')

# JSON firebase authentication
def firebase_init():
    config = {
        "apiKey": "AIzaSyBjM8SOL5rGiUq9gEF6NvBOMAWDO6Vfoqo",
        "authDomain": "genset-demo-website.firebaseapp.com",
        "databaseURL": "https://genset-demo-website.firebaseio.com",
        "storageBucket": "genset-demo-website.appspot.com",
        "serviceAccount": app.config["FIREBASE_AUTH_FILE"]
    }

    # Remove if it is a testing build
    if app.config['FIREBASE_AUTH_FILE'] == '':
        del config['serviceAccount']

    return pyrebase.initialize_app(config)

firebase = firebase_init()
auth = firebase.auth()
fbdb = firebase.database()

from . import utils
from . import views

# Populate VALID_TEMPS array
utils.VALID_TEMPS = list(map(basename, glob(join(app.config['UPLOAD_FOLDER'], '*'))))

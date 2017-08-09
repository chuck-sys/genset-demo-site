from flask import Flask
from flask_assets import Environment, Bundle
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
    '''
    Helps set up firebase. Returns the firebase initialization object.
    '''
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

def gen_assets():
    '''
    Generates minified assets for the site to use. Returns the environment
    that the assets live in, if we ever need to use'm.
    '''
    assets = Environment(app)
    expjs = Bundle("experiment.js", filters="jsmin", output="gen/experiment.js")
    viewjs = Bundle("view.js", filters="jsmin", output="gen/view.js")
    css = Bundle("override.css", "style.css", "widgets.css", filters="cssutils", output="gen/assets.css")

    assets.auto_build = True

    assets.register('experiment.js', expjs)
    assets.register('view.js', viewjs)
    assets.register('css_all', css)

    # Build all assets
    for bundle in assets:
        bundle.build()

    return assets

firebase = firebase_init()
auth = firebase.auth()
fbdb = firebase.database()

assets = gen_assets()

from . import utils
from . import views

# Populate VALID_TEMPS array
utils.VALID_TEMPS = list(map(basename, glob(join(app.config['UPLOAD_FOLDER'], '*'))))

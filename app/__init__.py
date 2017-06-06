from flask import Flask
import pyrebase
import json

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
        #"serviceAccount": app.config["FIREBASE_AUTH_FILE"]
    }
    return pyrebase.initialize_app(config)

firebase = firebase_init()
auth = firebase.auth()
user = auth.sign_in_with_email_and_password(app.config['FIREBASE_USER_NAME'],
                                            app.config['FIREBASE_USER_PWD'])
fbdb = firebase.database()

from . import views

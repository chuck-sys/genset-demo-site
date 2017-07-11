import os

# Change this to change the environment from dev to production (non-testing)
TESTING = False
# Part of CSRF token - I actually don't know
SECRET_KEY = 'P7rcW6Kn1cKXvKc'

UPLOAD_FOLDER = os.environ['UPLOAD_FOLDER']
TRAINING_FOLDER = os.environ['TRAINING_FOLDER']
LOG_FILE = 'logs.txt'

G_CAPTCHA_VERIFY = 'https://www.google.com/recaptcha/api/siteverify'
G_CAPTCHA_SITEKEY = os.environ.get('G_CAPTCHA_SITEKEY', '')
G_CAPTCHA_SECRET = os.environ.get('G_CAPTCHA_SECRET', '')

if TESTING:
    # These are keys and secrets that allow us to bypass reCAPTCHA
    G_CAPTCHA_SITEKEY = '6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI'
    G_CAPTCHA_SECRET = '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe'

FIREBASE_AUTH_FILE = os.environ.get('FIREBASE_AUTH_FILE', '')
# Set to True if you are using firebase
FIREBASE = True

API_KEY = os.environ.get('API_KEY', '')
UPLOADED_CSVS_DEST = UPLOAD_FOLDER
RESULTS_ZIP = "results.zip"
TESTING_FN = os.environ['TESTING_FN']
TRAINING_FN = os.environ['TRAINING_FN']
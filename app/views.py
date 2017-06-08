from flask import render_template, redirect, url_for, request, flash, abort, Markup, send_file
from werkzeug.utils import secure_filename
from app import app, fbdb
from .forms import ProcessingForm
from shutil import rmtree
import os
import tempfile
import requests
import subprocess as sub

@app.route('/')
@app.route('/about')
def index():
    return render_template('index.html',
                            title="GenSET")

@app.route('/experiment', methods=['GET'])
def experiment():
    form = ProcessingForm(request.form)
    return render_template('experiment.html',
                            title="Try it Out!",
                            sitekey=app.config['G_CAPTCHA_SITEKEY'],
                            form=form)

@app.route('/upload', methods=['POST'])
def upload():
    # Check Google reCAPTCHA v2
    data = {
        'secret': app.config['G_CAPTCHA_SECRET'],
        'response': request.form['g-recaptcha-response'],
        'remoteip': request.remote_addr
    }
    resp = requests.post(app.config['G_CAPTCHA_VERIFY'],
                        data=data).json()

    # Check to see if user is a bot
    if resp['success']:
        # Check to see if it is a valid submission
        form = ProcessingForm()
        if not form.validate_on_submit():
            # Invalid submissions get flashed
            for field, errors in form.errors.items():
                for e in errors:
                    flash('Error in %s: %s' % (getattr(form, field).label.text, e))
        else:
            path = tempfile.mkdtemp(dir=app.config['UPLOAD_FOLDER'], prefix='')
            session_id = os.path.basename(path)

            # Save the files
            for k, v in request.files.items():
                # Sanity checking
                if v.filename == '': continue

                sfn = secure_filename(v.filename)
                if sfn == '':
                    sfn = v.filename
                fn = os.path.join(path, sfn)
                v.save(fn)

            link = '<a href="%s" class="alert-link">view page</a>' % url_for('view', sid=session_id)
            success_txt = 'Success! To view progress, go to the %s' % link
            flash(Markup(success_txt))

            # If the path exists, render the view
            f = open(os.path.join(path, 'logs.txt'), 'w')
            env = os.environ.copy()
            env['API_KEY'] = app.config['API_KEY']
            sub.Popen(['python', 'scripts/master.py', session_id], stdout=f, stderr=f, env=env)
            return redirect(url_for('view', sid=session_id))
    else:
        # Show all authentication errors
        flash('Error: %s' % ', '.join(resp['error-codes']))

    return redirect(url_for('experiment',
                            title="Try it Out!",
                            sitekey=app.config['G_CAPTCHA_SITEKEY'],
                            form=form))

@app.route('/view/<sid>')
def view(sid):
    if '/' not in sid:
        path = os.path.join(app.config['UPLOAD_FOLDER'], sid)
        if os.path.isdir(path):
            return render_template('view.html', sid=sid, title="Progress for %s" % sid)
        else:
            abort(404)
    else:
        abort(403)

@app.route('/api/script_update', methods=['POST'])
def script_update():
    if request.json is None:
        abort(400)
    if request.json['auth_token'] != app.config['API_KEY']:
        abort(403)

    try:
        sid = request.json['session_id']
        progress = int(request.json['progress'])
        text = request.json['text']
    except ValueError:
        # If progress isn't an int, or if any of the fields are missing, abort.
        abort(400)

    # Actually upload the data
    data = { "progress": progress, "text": text }
    fbdb.child('sessions').child(sid).set(data)
    return '', 200

@app.route('/api/logs')
def get_logs():
    if '/' not in request.args['sid']:
        path = os.path.join(app.config['UPLOAD_FOLDER'], request.args['sid'],
                            app.config['LOG_FILE'])
        if os.path.isfile(path):
            return send_file(path)
        else:
            abort(404)
    else:
        abort(403)

@app.route('/api/upload', methods=['DELETE'])
def delete_upload():
    if request.json is None:
        abort(400)

    if request.json['auth_token'] != app.config['API_KEY']:
        abort(403)

    if '/' in request.json['sid']:
        abort(403)

    # FIXME: Only works for SIDs with length < 10
    if len(request.json['sid']) >= 10:
        abort(403)

    # Remove the entire upload
    path = os.path.join(app.config['UPLOAD_FOLDER'], request.json['sid'])
    rmtree(path)

    # Remove from firebase
    fbdb.child('sessions').child(request.json['sid']).remove()

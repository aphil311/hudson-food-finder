#!/usr/bin/env python

#-----------------------------------------------------------------------
# app.py
# Authors: Aidan Phillips
# Main file for generating views for the admin panel web app
#-----------------------------------------------------------------------
import flask
import os
import database

#-----------------------------------------------------------------------
app = flask.Flask(__name__, template_folder='templates',
    static_folder='static')
#-----------------------------------------------------------------------

#-----------------------------------------------------------------------
# index()
# Parameters: none
# Returns: the rendered index.html template
#-----------------------------------------------------------------------
@app.route('/')
def index():
    # only show offerings from the logged in organization
    offerings = database.find_offerings(('%'))
    html_code = flask.render_template('index.html',
        offerings=offerings)
    return flask.make_response(html_code)

@app.route('/upload')
def upload():
    html_code = flask.render_template('upload.html', message='')
    return flask.make_response(html_code)

@app.route('/upload', methods=['POST'])
def upload_confirmation():
    file = flask.request.files['file']
    file.save('static/files/' + file.filename)
    status = database.bulk_update('static/files/' + file.filename)
    if status == 0:
        message = 'file successfully uploaded'
    else:
        message = 'file failed to upload'
    os.remove('static/files/' + file.filename)
    html_code = flask.render_template('upload.html', message=message)
    return flask.make_response(html_code)
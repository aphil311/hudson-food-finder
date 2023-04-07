#!/usr/bin/env python

#-----------------------------------------------------------------------
# app.py
# Authors: Aidan Phillips
# Main file for generating views for the admin panel web app
#-----------------------------------------------------------------------

import os
import flask
import database

#-----------------------------------------------------------------------
app = flask.Flask(__name__, template_folder='templates',
    static_folder='static')
#-----------------------------------------------------------------------

#-----------------------------------------------------------------------
# index()
# Home page for the admin panel - shows all offerings in a table with
# a few buttons to sort, filter, and edit offerings
#-----------------------------------------------------------------------
@app.route('/')
def index():
    offerings = database.find_offerings(('%'))
    html_code = flask.render_template('index.html',
        offerings=offerings)
    return flask.make_response(html_code)


@app.route('/search', methods=['GET'])
def search():
    search_query = flask.request.args.get('search')
    search_query = '%' + search_query + '%'
    offerings = database.find_offerings((search_query,))
    html_code = flask.render_template('admin-table.html',
        offerings=offerings)
    return flask.make_response(html_code)

#-----------------------------------------------------------------------
# upload()
# Page for uploading a csv file to update the database
#-----------------------------------------------------------------------
@app.route('/upload')
def upload():
    html_code = flask.render_template('upload.html', message='')
    return flask.make_response(html_code)

#-----------------------------------------------------------------------
# upload_confirmation()
# Page for confirming the upload of a csv file to update the database
#-----------------------------------------------------------------------
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

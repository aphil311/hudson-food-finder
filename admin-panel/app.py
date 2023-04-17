#!/usr/bin/env python

#-----------------------------------------------------------------------
# app.py
# Authors: Aidan Phillips
# Main file for generating views for the admin panel web app
#-----------------------------------------------------------------------

import os
import flask
import database
import init

#-----------------------------------------------------------------------
app = init.app
#-----------------------------------------------------------------------

#-----------------------------------------------------------------------
# index()
# Home page for the admin panel - shows all offerings in a table with
# a few buttons to sort, filter, and edit offerings
#-----------------------------------------------------------------------
@app.route('/')
def index():
    html_code = flask.render_template('offerings.html',
        offerings=None)
    return flask.make_response(html_code)

#-----------------------------------------------------------------------
# search()
# Searches offerings and returns a table of offerings that match the
# search query
#-----------------------------------------------------------------------
@app.route('/organizations', methods=['GET'])
def searchOrganizations():
    organizations = database.find_organizations()
    html_code = flask.render_template('organizations.html', organizations=organizations)
    return flask.make_response(html_code)

@app.route('/offerings')
def offerings():
    html_code = flask.render_template('offerings.html',
        offerings=None)
    return flask.make_response(html_code)

#-----------------------------------------------------------------------
# search()
# Searches offerings and returns a table of offerings that match the
# search query
#-----------------------------------------------------------------------
@app.route('/search_offerings', methods=['GET'])
def searchOfferings():
    search_query = flask.request.args.get('search')
    search_query = '%' + search_query + '%'
    # must have a comma at the end of the tuple
    offerings = database.find_offerings((search_query,))
    html_code = flask.render_template('offering-table.html',
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
# download()
# Page for downloading a csv file from the database
#-----------------------------------------------------------------------
@app.route('/download')
def download():
    html_code = flask.render_template('download.html')
    return flask.make_response(html_code)

#-----------------------------------------------------------------------
# upload_confirmation()
# Page for confirming the upload of a csv file to update the database
#-----------------------------------------------------------------------
@app.route('/upload-offerings', methods=['POST'])
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

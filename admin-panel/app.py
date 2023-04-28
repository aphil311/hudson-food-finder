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

@app.route('/edit-offering', methods=['GET'])
def edit():
    offering_id = flask.request.args.get('id')
    offering = database.get_offering(offering_id)
    html_code = flask.render_template('edit-offering.html', offering=offering)
    return flask.make_response(html_code)

@app.route('/send-update', methods=['POST'])
def send_update():
    new_data = {}
    new_data['title'] = flask.request.form.get('title')
    days_array = [False, False, False, False, False, False, False]
    days_open = flask.request.form.getlist('days-open')
    for day in days_open:
        days_array[int(day)] = True
    days_open_str = ''
    for day in days_array:
        if day:
            days_open_str += 'T-'
        else:
            days_open_str += 'F-'
    days_open_str = days_open_str[:-1]
    new_data['days_open'] = days_open_str
    new_data['start_time'] = flask.request.form.get('start-time')
    new_data['end_time'] = flask.request.form.get('end-time')
    new_data['start_date'] = flask.request.form.get('start-date')
    new_data['end_date'] = flask.request.form.get('end-date')
    new_data['service'] = flask.request.form.get('service')
    new_data['group'] = flask.request.form.get('group')
    new_data['description'] = flask.request.form.get('description')

    offering_id = flask.request.form.get('id')
    database.update_row(offering_id, new_data)
    return flask.redirect('/offerings')

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
    status, messages = database.bulk_update('static/files/' + file.filename)
    if status != 0:
        print('cry')
    elif status != 1:
        print('cry more')
    elif status != 2:
        print('cry even more')
    os.remove('static/files/' + file.filename)
    html_code = flask.render_template('upload.html', messages=messages)
    return flask.make_response(html_code)

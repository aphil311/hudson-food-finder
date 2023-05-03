#!/usr/bin/env python

#-----------------------------------------------------------------------
# app.py
# Authors: Aidan Phillips
# Main file for generating views for the admin panel web app
#-----------------------------------------------------------------------

import os
import flask
import database
import config.init as init
import auth
from config.definitions import ROOT_DIR
from flask_talisman import Talisman
from decouple import config
import flask_wtf.csrf
import re

#-----------------------------------------------------------------------
app = init.app
app.secret_key = config('APP_KEY')
flask_wtf.csrf.CSRFProtect(app)

csp = {
    'default-src': [
        '\'self\'',
        '\'unsafe-inline\'',
        'stackpath.bootstrapcdn.com',
        'code.jquery.com',
        'cdn.jsdelivr.net',
        'cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css',
        'cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.min.js',
        'cdnjs.cloudflare.com/ajax/libs/bootstrap-icons/1.10.2/font/bootstrap-icons.css',
        'cdnjs.cloudflare.com/ajax/libs/jquery/3.6.0/jquery.min.js',
        'cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css',
        '/static/styles.css',
        'cdnjs.cloudflare.com/',
        'https://lh3.googleusercontent.com/a/'
    ]
}
talisman = Talisman(app, content_security_policy=csp)
# Talisman(app)
#-----------------------------------------------------------------------

# Routes for authentication 

@app.route('/login', methods=['GET'])
def login():
    return auth.login()


@app.route('/login/callback', methods=['GET'])
def callback():
    return auth.callback()


def authorize(username):
    if not database.is_authorized(username):
        html_code = 'You are not authorized to use this application.'
        response = flask.make_response(html_code)
        flask.abort(response)

#-----------------------------------------------------------------------
# index()
# Home page for the admin panel - shows all offerings in a table with
# a few buttons to sort, filter, and edit offerings
#-----------------------------------------------------------------------
@app.route('/')
def index():
    # authenticate user
    username = auth.authenticate()
    authorize(username)

    picture = flask.session.get('picture')

    html_code = flask.render_template('offerings.html',
        offerings=None, picture = picture)
    return flask.make_response(html_code)

#-----------------------------------------------------------------------
# search()
# Searches offerings and returns a table of offerings that match the
# search query
#-----------------------------------------------------------------------
@app.route('/organizations', methods=['GET'])
def searchOrganizations():
    # authenticate user
    username = auth.authenticate()
    authorize(username)
    organizations = database.find_organizations()
    picture = flask.session.get('picture')
    html_code = flask.render_template('organizations.html', organizations=organizations, picture = picture)
    return flask.make_response(html_code)

@app.route('/offerings')
def offerings():
    # authenticate user
    username = auth.authenticate()
    authorize(username)
    picture = flask.session.get('picture')
    html_code = flask.render_template('offerings.html',
        offerings=None, picture = picture)

    return flask.make_response(html_code)

#-----------------------------------------------------------------------
# search()
# Searches offerings and returns a table of offerings that match the
# search query
#-----------------------------------------------------------------------
@app.route('/search_offerings', methods=['GET'])
def searchOfferings():
    # authenticate user
    username = auth.authenticate()
    authorize(username)
    search_query = flask.request.args.get('search')
    search_query = '%' + search_query + '%'
    # must have a comma at the end of the tuple
    offerings = database.find_offerings((search_query,))
    html_code = flask.render_template('offering-table.html',
        offerings=offerings)
    return flask.make_response(html_code)

@app.route('/edit-offering', methods=['GET'])
def edit():
    # authenticate user
    username = auth.authenticate()
    authorize(username)
    offering_id = flask.request.args.get('id')
    offering = database.get_offering(offering_id)
    html_code = flask.render_template('edit-offering.html', offering=offering)
    return flask.make_response(html_code)

@app.route('/send-update', methods=['POST'])
def send_update():
    # authenticate user
    username = auth.authenticate()
    authorize(username)
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
    # authenticate user
    username = auth.authenticate()
    authorize(username)

    picture = flask.session.get('picture')
    html_code = flask.render_template('upload.html', message='', picture = picture)
    return flask.make_response(html_code)

#-----------------------------------------------------------------------
# download()
# Page for downloading a csv file from the database
#-----------------------------------------------------------------------
@app.route('/download')
def download():
    # authenticate user
    username = auth.authenticate()
    authorize(username)
    picture = flask.session.get('picture')
    html_code = flask.render_template('download.html', picture = picture)
    return flask.make_response(html_code)

@app.route('/download-csv')
def download_csv():
    # authenticate user
    username = auth.authenticate()
    authorize(username)
    # makes the file
    status = database.get_csv()
    if status == 0:
        file_path = os.path.join(ROOT_DIR, 'static',
            'files', 'output.csv')
        # success : return csv in static/files
        csv = open(file_path).read()
        os.remove(file_path)
        return flask.Response(
            csv,
            mimetype="text/csv",
            headers={"Content-disposition":
                    "attachment; filename=offerings.csv"})
    else:
        # failure : return error message
        return flask.Response(
            'Error: could not download csv',
            mimetype="text/html")

#-----------------------------------------------------------------------
# upload_confirmation()
# Page for confirming the upload of a csv file to update the database
#-----------------------------------------------------------------------
@app.route('/upload-offerings', methods=['POST'])
def upload_confirmation():
    # authenticate user
    username = auth.authenticate()
    authorize(username)
    file = flask.request.files['file']
    file_path = os.path.join(ROOT_DIR, 'static', 'files', 'input.csv')
    print(file_path)
    file.save(file_path)
    status, messages = database.bulk_update(file_path)
    if status != 0:
        print('cry')
    picture = flask.session.get('picture')
    html_code = flask.render_template('upload.html', messages=messages, picture = picture)
    return flask.make_response(html_code)

#-----------------------------------------------------------------------
# upload_confirmation()
# Page for confirming the upload of a csv file to update the database
#-----------------------------------------------------------------------
@app.route('/authorize-users', methods = ['GET'])
def auth_panel():
    username = auth.authenticate()
    authorize(username)
    emails = database.get_emails()
    picture = flask.session.get('picture')
    html_code = flask.render_template('auth-users.html', picture = picture, emails = emails)
    return flask.make_response(html_code)

@app.route('/auth-finished', methods = ['POST'])
def auth_complete():
    username = auth.authenticate()
    authorize(username)

    email = flask.request.form.get('email')

    # Faulty email submitted
    if not re.match("[^@]+@[^@]+\.[^@]+", email):
        completion_string = 'Invalid email submitted, please enter a valid email address \
        email: ' + email
    # Email is in database already
    elif database.is_authorized(email):
        completion_string = 'User ' + email + ' is already authorized'
    # Email is not in database and is valid - needs to be authorized
    else: 
        database.authorize_email(email)
        print(email)
        completion_string = 'User ' + email + ' has successfully been authorized'
    
    picture = flask.session.get('picture')
    html_code = flask.render_template('auth-finished.html', 
                                        completion_string = completion_string, picture = picture)
    return flask.make_response(html_code)


@app.route('/auth-removed', methods = ['POST'])
def auth_removed():
    username = auth.authenticate()
    authorize(username)

    email = flask.request.form.get('email')

    # Faulty email submitted
    if not re.match("[^@]+@[^@]+\.[^@]+", email):
        completion_string = 'Invalid email submitted, please enter a valid email address \
        email: ' + email
    # Email is not in database already
    elif (database.is_authorized(email) == False):
        completion_string = 'User ' + email + ' is not  authorized'
    # Email is in database and is valid - and needs to be DE-AUTHORIZED
    else: 
        database.deauthorize_email(email)
        completion_string = 'User ' + email + ' has successfully been de-authorized'
    
    picture = flask.session.get('picture')
    html_code = flask.render_template('auth-finished.html', 
                                        completion_string = completion_string, picture = picture)
    return flask.make_response(html_code)









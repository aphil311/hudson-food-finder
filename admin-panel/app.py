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
import sys

#-----------------------------------------------------------------------
app = init.app

# security stuff -------------------------------------------------------
app.secret_key = config('APP_KEY')
flask_wtf.csrf.CSRFProtect(app)
csp = {
    'default-src': [
        '\'self\'',
        '\'unsafe-inline\'',
        'stackpath.bootstrapcdn.com',
        'code.jquery.com',
        'cdn.jsdelivr.net',
        'cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/'
            'bootstrap.min.css',
        'cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.min.js',
        'cdnjs.cloudflare.com/ajax/libs/bootstrap-icons/1.10.2/font/'
            'bootstrap-icons.css',
        'cdnjs.cloudflare.com/ajax/libs/jquery/3.6.0/jquery.min.js',
        'cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/'
            'font-awesome.min.css',
        '/static/styles.css',
        'cdnjs.cloudflare.com/',
        'https://lh3.googleusercontent.com/a/'
    ]
}
talisman = Talisman(app, content_security_policy=csp)

#-----------------------------------------------------------------------
# authorize()
# Checks if the user is authorized to use the admin panel
#-----------------------------------------------------------------------
def authorize(username=None):
    username = auth.authenticate()
    if not database.is_authorized(username):
        html_code = 'You are not authorized to use this application.'
        response = flask.make_response(html_code)
        flask.abort(response)
    else:
        return flask.session.get('picture')

# routes for login -----------------------------------------------------
@app.route('/login', methods=['GET'])
def login():
    return auth.login()

@app.route('/login/callback', methods=['GET'])
def callback():
    return auth.callback()

@app.route('/logoutapp', methods=['GET'])
def logoutapp():
    return auth.logoutapp()

#-----------------------------------------------------------------------
# index()
# Home page for the admin panel - shows all offerings in a table with
# a few buttons to sort, filter, and edit offerings
#-----------------------------------------------------------------------
@app.route('/')
def index():
    # authenticate user and get picture
    picture = authorize()

    # get all offerings from the database
    organizations = database.find_organizations()

    html_code = flask.render_template('offerings.html',
        offerings=None, picture = picture, organizations=organizations)
    return flask.make_response(html_code)

#-----------------------------------------------------------------------
# search()
# Searches offerings and returns a table of offerings that match the
# search query
#-----------------------------------------------------------------------
@app.route('/organizations', methods=['GET'])
def searchOrganizations():
    # authenticate user
    picture = authorize()

    organizations = database.find_organizations()
    html_code = flask.render_template('organizations.html', organizations=organizations, picture = picture)
    return flask.make_response(html_code)

@app.route('/offerings')
def offerings():
    # authenticate user
    picture = authorize()

    # get all offerings from the database
    organizations = database.find_organizations()

    html_code = flask.render_template('offerings.html',
        offerings=None, picture = picture, organizations=organizations)

    return flask.make_response(html_code)

#-----------------------------------------------------------------------
# search()
# Searches offerings and returns a table of offerings that match the
# search query
#-----------------------------------------------------------------------
@app.route('/search_offerings', methods=['GET'])
def searchOfferings():
    # authenticate user
    authorize()

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
    picture = authorize()

    offering_id = flask.request.args.get('id')
    offering = database.get_offering(offering_id)
    html_code = flask.render_template('edit-offering.html', offering=offering,
        picture=picture)
    return flask.make_response(html_code)

@app.route('/send-update', methods=['POST'])
def send_update():
    # authenticate user
    authorize()

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
    picture = authorize()

    html_code = flask.render_template('upload.html', message='', picture = picture)
    return flask.make_response(html_code)

#-----------------------------------------------------------------------
# download()
# Page for downloading a csv file from the database
#-----------------------------------------------------------------------
@app.route('/download')
def download():
    # authenticate user
    picture = authorize()

    html_code = flask.render_template('download.html', picture = picture)
    return flask.make_response(html_code)

@app.route('/download-csv')
def download_csv():
    # authenticate user
    authorize()

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
    picture = authorize()

    file = flask.request.files.get('file')
    if file:
        file_path = os.path.join(ROOT_DIR, 'static', 'files', 'input.csv')
        file.save(file_path)
        status, messages = database.bulk_update(file_path)
        if status != 0:
            print('cry')
    else:
        messages = ['Error: no file uploaded']
    html_code = flask.render_template('upload.html', messages=messages, picture = picture)
    return flask.make_response(html_code)

#-----------------------------------------------------------------------
# authorize_users()
# Page for authorizing users to access the database or de-authorizing
#-----------------------------------------------------------------------
@app.route('/authorize-users', methods = ['GET'])
def authorize_users():
    # verify user is authorized
    picture = authorize()

    # get the emails and picture to render the page
    emails = database.get_emails()

    # render the page
    html_code = flask.render_template('auth-users.html',
        picture=picture, emails=emails)
    return flask.make_response(html_code)

#-----------------------------------------------------------------------
# auth_finished()
# Confirmation page for authorizing users to access the database
#-----------------------------------------------------------------------
@app.route('/auth-finished', methods = ['POST'])
def auth_finished():
    # verify user is authorized
    picture = authorize()

    # get the email we are authorizing
    email = flask.request.form.get('email')
    status = 1      # 1 = success, 2 = failure
    # Faulty email submitted
    if not re.match("[^@]+@[^@]+\.[^@]+", email):
        message = 'Invalid email submitted, please enter a valid email address \
        email: ' + email
        status = 2
    # Email is in database already
    elif database.is_authorized(email):
        message = 'User ' + email + ' is already authorized'
        status = 2
    # Email is not in database and is valid - needs to be authorized
    else: 
        database.authorize_email(email)
        message = 'User ' + email + ' has successfully been authorized'

    # get the emails and picture to render the page
    emails = database.get_emails()

    # render the page
    html_code = flask.render_template('auth-finished.html', status=status,
        message=message, emails=emails, picture=picture)
    return flask.make_response(html_code)

#-----------------------------------------------------------------------
# auth_removed()
# Confirmation page for de-authorizing users to access the database
#-----------------------------------------------------------------------
@app.route('/auth-removed', methods = ['POST'])
def auth_removed():
    # verify user is authorized
    picture = authorize()

    # get the email we are de-authorizing
    email = flask.request.form.get('email')
    status = 3      # 3 = success, 4 = failure
    # Faulty email submitted
    if not re.match("[^@]+@[^@]+\.[^@]+", email):
        message = 'Invalid email submitted, please enter a valid email address \
        email: ' + email
        status = 4
    # Email is not in database already
    elif (database.is_authorized(email) == False):
        message = 'User ' + email + ' is not  authorized'
        status = 4
    # Can't deauthorize yourself
    elif(email == flask.session.get('email')):
        message = 'Cannot deauthorize youself'
        status = 4
    # Can't deathorize admin
    elif(email == 'cgrandin@hcnj.us' or email == 'delma.yorimoto@rutgers.edu'
        or email == 'cadams-griffin@hcnj.us' or email == 'yousefamin800@gmail.com'
        or email == 'zainahmed1956@gmail.com' or email == 'aidantphil21@gmail.com'):
        message = 'Cannot deauthorize admin'
        status = 4
    # Email is in database and is valid - and needs to be DE-AUTHORIZED
    else: 
        database.deauthorize_email(email)
        message = 'User ' + email + ' has successfully been de-authorized'
    
    # get the emails and picture to render the page
    emails = database.get_emails()


    # render the page
    html_code = flask.render_template('auth-finished.html', 
        message=message, picture=picture,
        emails=emails, status=status)
    return flask.make_response(html_code)

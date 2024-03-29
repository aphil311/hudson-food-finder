#!/usr/bin/env python

#-----------------------------------------------------------------------
# app.py
# Authors: Aidan Phillips
# Main file for generating views for the admin panel web app
#-----------------------------------------------------------------------

from datetime import date
import os
import re
import sys
import flask
from flask_talisman import Talisman
from decouple import config
import flask_wtf.csrf
import auth
import database
from config import init
from config.definitions import ROOT_DIR

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
# define superadmins and developers
superadmins = [
    'cgrandin@hcnj.us',
    'delma.yorimoto@rutgers.edu',
    'cadams-griffin@hcnj.us',
]
developers = [
    'yousefamin800@gmail.com',
    'zainahmed1956@gmail.com',
    'aidantphil21@gmail.com'
]
#-----------------------------------------------------------------------

#-----------------------------------------------------------------------
# authorize()
# Checks if the user is authorized to use the admin panel
#-----------------------------------------------------------------------
def authorize(username=None):
    username = auth.authenticate()
    if not database.is_authorized(username):
        html_code = flask.render_template('unauthorized.html')
        response = flask.make_response(html_code)
        flask.abort(response)

#-----------------------------------------------------------------------
# auth_super()
# Checks if the user is a super admin
#-----------------------------------------------------------------------
def auth_super():
    username = auth.authenticate()
    if not database.is_super_authorized(username):
        html_code = 'You are not authorized to use this part of the '
        html_code += 'application.'
        html_code += '<br><a href="/">Return to home page</a>'
        response = flask.make_response(html_code)
        flask.abort(response)

#-----------------------------------------------------------------------
# auth_off()
# Checks if the user is an admin of an organization
#-----------------------------------------------------------------------
def auth_off(offering):
    # ensure the user is authorized to edit offerings for that
    # organization
    email = flask.session.get('email')
    # organizations the user has acess to
    organizations = database.get_access(email)
    if '%' in organizations:
        return
    if not offering.get_org() in organizations:
        html_code = 'You are not authorized to edit this offering.'
        response = flask.make_response(html_code)
        flask.abort(response)

#-----------------------------------------------------------------------
# auth_org()
# Checks if the user is an admin of an organization
#-----------------------------------------------------------------------
def auth_org(organization):
    # ensure the user is authorized to edit offerings for that
    # organization
    email = flask.session.get('email')
    # organizations the user has acess to
    organizations = database.get_access(email)
    if '%' in organizations:
        return
    if not organization.get_org_name() in organizations:
        html_code = 'You are not authorized to edit this organization.'
        response = flask.make_response(html_code)
        flask.abort(response)

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

# not_found_error() ----------------------------------------------------
# Error handler for 404 errors
@app.errorhandler(404)
def not_found_error(ex):
    # note that we set the 500 status explicitly
    print(str(ex))
    return flask.render_template('404.html'), 404

# index() --------------------------------------------------------------
# Home page for the admin panel - shows all offerings in a table with
# a few buttons to sort, filter, and edit offerings
@app.route('/')
def index():
    # authenticate user and get picture
    authorize()
    email = flask.session.get('email')
    super_admin = database.is_super_authorized(email)
    picture = flask.session.get('picture')

    # get all offerings from the database
    organizations = database.find_organizations(email)

    html_code = flask.render_template('offerings.html',
        offerings=None, picture=picture, organizations=organizations,
        super=super_admin)
    return flask.make_response(html_code)

#-----------------------------------------------------------------------
# OFFERINGS ROUTES
#-----------------------------------------------------------------------

# get_offerings() ------------------------------------------------------
# Gets all offerings from the database and displays them in a table
# with a dropdown of all organizations
@app.route('/offerings')
def get_offerings():
    # authenticate user
    authorize()
    email = flask.session.get('email')
    picture = flask.session.get('picture')
    super_admin = database.is_super_authorized(email)

    # get all organizations from the database
    organizations = database.find_organizations(email)

    # render the template
    html_code = flask.render_template('offerings.html',
        offerings=None, picture = picture, organizations=organizations,
        super=super_admin)
    return flask.make_response(html_code)

# search_offerings() ---------------------------------------------------
# Searches offerings and returns a table of offerings that match the
# search query
@app.route('/search_offerings', methods=['GET'])
def search_offerings():
    # authenticate user
    authorize()
    email = flask.session.get('email')
    organizations = database.get_access(email)

    # form the search query and get offerings from the database
    search_query = flask.request.args.get('search')
    search_query = '%' + search_query + '%'
    offerings, expired = [], []
    for org in organizations:
        off, exp = database.find_offerings((search_query, org))
        offerings.extend(off)
        expired.extend(exp)

    # get all organizations from the database
    organizations = database.find_organizations(email)

    # render the template
    html_code = flask.render_template('offering-table.html',
        offerings=offerings, expired=expired,
        organizations=organizations)
    return flask.make_response(html_code)

# filter_offerings() ---------------------------------------------------
# Filters offerings and returns a table of offerings that match the
# filter query
@app.route('/filter_offerings', methods=['GET'])
def filter_offerings():
    # authenticate user
    authorize()

    # get the filter query from the form
    filter_query = flask.request.args.get('filter')

    # get offerings from the database
    offerings, expired = database.find_offerings(('%', filter_query))

    # render the template
    html_code = flask.render_template('raw-table.html',
        offerings=offerings, expired=expired)
    return flask.make_response(html_code)

# edit_offering() ------------------------------------------------------
# Gets the offering with the specified id and displays it in a form
# for editing
@app.route('/edit-offering', methods=['GET'])
def edit_offering():
    # authenticate user
    authorize()
    email = flask.session.get('email')
    super_admin = database.is_super_authorized(email)
    picture = flask.session.get('picture')

    # get the specific offering we want to edit
    offering_id = flask.request.args.get('id')
    offering = database.get_offering(offering_id)
    if not offering:
        flask.abort(404)

    # ensure the user is authorized to edit offerings for that
    # organization
    auth_off(offering)

    # render the template
    html_code = flask.render_template('edit-offering.html',
        offering=offering, picture=picture, super=super_admin)
    return flask.make_response(html_code)

# send_update_off() ----------------------------------------------------
# Updates the offering with the specified id with the data from the
# form
@app.route('/send-update-off', methods=['POST'])
def send_update_off():
    # authenticate user
    authorize()

    # create a dictionary for the new data
    new_data = {}
    new_data['title'] = flask.request.form.get('title')

    # get the days open from the form and convert it to a string
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

    # add the rest of the data to the dictionary
    new_data['days_open'] = days_open_str
    new_data['days_desc'] = flask.request.form.get('days-desc')
    new_data['start_time'] = flask.request.form.get('start-time')
    new_data['end_time'] = flask.request.form.get('end-time')
    new_data['start_date'] = flask.request.form.get('start-date')
    if not new_data['start_date']:
        new_data['start_date'] = date(1970, 1, 1)
    new_data['end_date'] = flask.request.form.get('end-date')
    if not new_data['end_date']:
        new_data['end_date'] = date(9999, 12, 31)
    new_data['service'] = flask.request.form.get('service')
    new_data['group'] = flask.request.form.get('group')
    new_data['description'] = flask.request.form.get('description')

    # get the offering id and update the offering
    offering_id = flask.request.form.get('id')

    # ensure the user is authorized to edit offerings for that
    # organization
    auth_off(database.get_offering(offering_id))

    database.update_off(offering_id, new_data)

    # redirect to the offerings page
    return flask.redirect('/offerings')

#-----------------------------------------------------------------------
# ORGANIZATION ROUTES
#-----------------------------------------------------------------------

# search_organizations() -----------------------------------------------
# Gets all organizations from the database and displays them in a table
@app.route('/organizations', methods=['GET'])
def search_organizations():
    # authenticate user
    authorize()
    email = flask.session.get('email')
    picture = flask.session.get('picture')
    super_admin = database.is_super_authorized(email)

    # get organizations from the database
    organizations = database.find_organizations(email)

    # render the template
    html_code = flask.render_template('organizations.html',
        organizations=organizations, picture=picture,
        super=super_admin)
    return flask.make_response(html_code)

# edit_organization() --------------------------------------------------
# Gets the organization with the specified id and displays it in a form
# for editing
@app.route('/edit-organization', methods=['GET'])
def edit_organization():
    # authenticate user
    authorize()
    email = flask.session.get('email')
    super_admin = database.is_super_authorized(email)
    picture = flask.session.get('picture')

    # get the specific organiation we want to edit
    organization_id = flask.request.args.get('id')
    organization = database.get_organization(organization_id)
    if not organization:
        flask.abort(404)

    # ensure the user is authorized to edit that organization
    auth_org(organization)

    # render the template
    html_code = flask.render_template('edit-organization.html',
        organization=organization, picture=picture,
        super=super_admin)
    return flask.make_response(html_code)

# send_update_org() ----------------------------------------------------
# Updates the organization with the specified id with the data from the
# form
@app.route('/send-update-org', methods=['POST'])
def send_update_org():
    # authenticate user
    authorize()

    # create a dictionary for the new data
    new_data = {}
    # populate the dictionary with the data from the form
    new_data['name'] = flask.request.form.get('name')
    new_data['phone'] = flask.request.form.get('phone')
    new_data['website'] = flask.request.form.get('website')
    new_data['photo_url'] = flask.request.form.get('photo_url')
    new_data['address'] = flask.request.form.get('address')
    new_data['zip_code'] = flask.request.form.get('zip_code')

    # get the organization id and update the organization
    organization_id = flask.request.form.get('id')

    # ensure the user is authorized to edit that organization
    auth_org(database.get_organization(organization_id))

    database.update_org(organization_id, new_data)

    # redirect to the organizations page
    return flask.redirect('/organizations')

#-----------------------------------------------------------------------
# UPLOAD AND DOWNLOAD ROUTES
#-----------------------------------------------------------------------

# upload() -------------------------------------------------------------
# Page for uploading a csv file to update the database
@app.route('/upload')
def upload():
    # authenticate user
    authorize()
    auth_super()
    picture = flask.session.get('picture')

    # render the template
    html_code = flask.render_template('upload.html', message='',
        picture=picture, super=True)
    return flask.make_response(html_code)

# upload_confirmation() ------------------------------------------------
# Page for confirming the upload of a csv file to update the database
@app.route('/upload-offerings', methods=['POST'])
def upload_confirmation():
    # authenticate user
    authorize()
    auth_super()
    picture = flask.session.get('picture')

    # get the file from the form
    file = flask.request.files.get('file')
    if file:
        file_path = os.path.join(ROOT_DIR, 'static', 'files',
            'input.csv')
        file.save(file_path)
        status, messages = database.bulk_update(file_path)
        if status != 0:
            print('some error occurred on the backend', file=sys.stderr)
    else:
        # no file : return error message
        messages = ['Error: no file uploaded']

    # render the template
    html_code = flask.render_template('upload.html', messages=messages,
        picture=picture, super=True)
    return flask.make_response(html_code)

# download() -----------------------------------------------------------
# Page for downloading a csv file from the database
@app.route('/download')
def download():
    # authenticate user
    authorize()
    auth_super()
    picture = flask.session.get('picture')

    # render the template
    html_code = flask.render_template('download.html',
        picture = picture, super=True)
    return flask.make_response(html_code)

# download_csv() -------------------------------------------------------
# Make a csv file from the data in the database and return it to the
# user
@app.route('/download-csv')
def download_csv():
    # authenticate user
    authorize()
    auth_super()

    # makes the file from the database
    status = database.get_csv()

    # if the file was made successfully, return the csv
    if status == 0:
        # success : return csv in static/files
        file_path = os.path.join(ROOT_DIR, 'static',
            'files', 'output.csv')
        with open(file_path, encoding='utf-8') as csv_file:
            csv = csv_file.read()
        os.remove(file_path)
        return flask.Response(
            csv,
            mimetype="text/csv",
            headers={"Content-disposition":
                    "attachment; filename=offerings.csv"})
    # failure : return error message
    return flask.Response(
        'Error: could not download csv',
        mimetype="text/html")

#-----------------------------------------------------------------------
# AUTHORIZATION ROUTES
#-----------------------------------------------------------------------

# get_emails() ---------------------------------------------------------
# Page for getting all the emails in the database from an offering
@app.route('/get-emails', methods = ['GET'])
def get_emails():
    # verify user is authorized
    authorize()
    auth_super()

    # get the offering id from the request
    organization = flask.request.args.get('organization')
    print(organization)

    # get the emails from the database
    emails = database.get_emails(organization)
    for email in emails:
        print(email)

    table = []
    for user in emails:
        orgs = database.get_access(user)
        user_orgs = []
        if '%' in orgs:
            user_orgs = ('ADMIN',)
            if user in superadmins:
                user_orgs = ('SUPER ADMIN',)
            elif user in developers:
                user_orgs = ('DEVELOPER',)
        else:
            user_orgs = orgs
        table.append([user, user_orgs])

    # send the table to the template
    html_code = flask.render_template('email-table.html',
        users=table)
    return flask.make_response(html_code)

# authorize_users() ----------------------------------------------------
# Page for authorizing users to access the database or de-authorizing
@app.route('/authorize-users', methods = ['GET'])
def authorize_users():
    # verify user is authorized
    authorize()
    auth_super()
    email = flask.session.get('email')
    picture = flask.session.get('picture')

    # get all authorized emails and organizations
    emails = database.get_emails()
    organizations = database.find_organizations(email)

    table = []
    for user in emails:
        orgs = database.get_access(user)
        user_orgs = []
        if '%' in orgs:
            user_orgs = ('ADMIN',)
            if user in superadmins:
                user_orgs = ('SUPER ADMIN',)
            elif user in developers:
                user_orgs = ('DEVELOPER',)
        else:
            user_orgs = orgs
        table.append([user, user_orgs])

    # render the page
    html_code = flask.render_template('auth-users.html',
        picture=picture, emails=emails, organizations=organizations,
        users=table, super=True)
    return flask.make_response(html_code)

# auth_finished() ------------------------------------------------------
# Confirmation page for authorizing users to access the database
@app.route('/auth-finished', methods = ['POST'])
def auth_finished():
    # verify user is authorized
    authorize()
    auth_super()
    picture = flask.session.get('picture')

    # get the email we are authorizing
    email = flask.request.form.get('email')
    access = flask.request.form.get('access')

    status = 1      # 1 = success, 2 = failure
    # Faulty email submitted
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        message = 'Invalid email submitted, please enter a valid '
        message += 'email address email: ' + email
        status = 2
    # Email is in database already
    elif access in database.get_access(email) or \
        '%' in database.get_access(email):
        message = 'User ' + email
        message += ' is already authorized for that organization'
        status = 2
    # Email is not in database and is valid - needs to be authorized
    else:
        database.authorize_email(email, access)
        message = 'User ' + email + ' has successfully been authorized'

    # get the emails and picture to render the page
    emails = database.get_emails()
    email = flask.session.get('email')
    organizations = database.find_organizations(email)

    table = []

    for user in emails:
        orgs = database.get_access(user)
        user_orgs = []
        if '%' in orgs:
            user_orgs = ('ADMIN',)
            if user in superadmins:
                user_orgs = ('SUPER ADMIN',)
            elif user in developers:
                user_orgs = ('DEVELOPER',)
        else:
            user_orgs = orgs
        table.append([user, user_orgs])

    # render the page
    html_code = flask.render_template('auth-finished.html',
        status=status, message=message, emails=emails, picture=picture,
        organizations=organizations, super=True, users=table)
    return flask.make_response(html_code)

# auth_removed() -------------------------------------------------------
# Confirmation page for de-authorizing users to access the database
@app.route('/auth-removed', methods = ['POST'])
def auth_removed():
    # verify user is authorized
    authorize()
    auth_super()
    email = flask.session.get('email')
    picture = flask.session.get('picture')

    # get the email we are de-authorizing
    email = flask.request.form.get('email')
    status = 3      # 3 = success, 4 = failure

    # Can't deauthorize yourself
    if email == flask.session.get('email'):
        message = 'Cannot deauthorize yourself'
        status = 4
    # Can't deathorize admin
    elif email in superadmins or email in developers:
        message = 'Cannot deauthorize super admin or developer'
        status = 4
    # Email is in database and is valid - and needs to be DE-AUTHORIZED
    else:
        database.deauthorize_email(email)
        message = 'User ' + email
        message += ' has successfully been de-authorized'

    # get the emails and picture to render the page
    emails = database.get_emails()
    organizations = database.find_organizations(email)

    table = []

    for user in emails:
        orgs = database.get_access(user)
        user_orgs = []
        if '%' in orgs:
            user_orgs = ('ADMIN',)
            if user in superadmins:
                user_orgs = ('SUPER ADMIN',)
            elif user in developers:
                user_orgs = ('DEVELOPER',)
        else:
            user_orgs = orgs
        table.append([user, user_orgs])

    # render the page
    html_code = flask.render_template('auth-finished.html',
        message=message, picture=picture,
        emails=emails, status=status, organizations=organizations,
        super=True, users=table)
    return flask.make_response(html_code)

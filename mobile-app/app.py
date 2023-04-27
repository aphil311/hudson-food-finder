#!/usr/bin/env python

#-----------------------------------------------------------------------
# app.py
# Authors: Aidan Phillips
# Main file for generating views for the mobile web app
#-----------------------------------------------------------------------
import flask
import database
import init

app = init.app

#-----------------------------------------------------------------------
# index()
# Displays offerings in a list
#-----------------------------------------------------------------------
@app.route('/index')
@app.route('/')
def index():
    services = database.get_services()
    if len(services) == 1:
        services = None
    groups = database.get_groups()
    if len(groups) == 1:
        groups = None
    html_code = flask.render_template('index.html', services=services,
        groups=groups)
    return flask.make_response(html_code)

#-----------------------------------------------------------------------
# search_results()
# Displays offerings in a list based on the search query
#-----------------------------------------------------------------------
@app.route('/search', methods=['GET'])
def search_results():
    # Get search term and sort by from query string
    search_term = flask.request.args.get('search')
    sort_by = flask.request.args.get('sort')
    services = flask.request.args.getlist('service')
    groups = flask.request.args.getlist('group')
    # Form query and get offerings from database
    query = (search_term, sort_by, services, groups)
    offerings = database.find_offerings(query)
    # Render template and return response
    html_code = flask.render_template('results.html',
        offerings=offerings)
    return flask.make_response(html_code)

@app.route('/offerings', methods=['GET'])
def offering():
    off_id = flask.request.args.get('id')
    offering = database.get_offering(off_id)
    html_code = flask.render_template('off_details.html', offering=offering)
    return flask.make_response(html_code)

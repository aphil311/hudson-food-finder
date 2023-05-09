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

# not_found_error() ----------------------------------------------
# Error handler for 404 errors
@app.errorhandler(404)
def internal_server_error(e):
    # note that we set the 500 status explicitly
    return flask.render_template('404.html'), 404

#-----------------------------------------------------------------------
# index()
# Displays offerings in a list
#-----------------------------------------------------------------------
@app.route('/index')
@app.route('/')
def index():
    services = database.get_services()
    groups = database.get_groups()
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
    days = flask.request.args.get('days')
    times = (flask.request.args.get('start_time'), 
        flask.request.args.get('end_time'))
    groups = flask.request.args.getlist('group')
    # Form query and get offerings from database
    query = (search_term, sort_by, services, days, times, groups)
    offerings = database.find_offerings(query)
    # Render template and return response
    html_code = flask.render_template('results.html',
        offerings=offerings)
    return flask.make_response(html_code)

@app.route('/offerings', methods=['GET'])
def offering():
    off_id = flask.request.args.get('id')
    offering = database.get_offering(off_id)
    if not offering:
        flask.abort(404)

    html_code = flask.render_template('off_details.html', offering=offering)
    return flask.make_response(html_code)

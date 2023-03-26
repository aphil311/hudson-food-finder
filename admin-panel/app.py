#!/usr/bin/env python

#-----------------------------------------------------------------------
# app.py
# Authors: Aidan Phillips
# Main file for generating views for the admin panel web app
#-----------------------------------------------------------------------
import flask
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
    org_id = '1'
    offerings = database.find_offerings(('%', '%', '%', '%', '%', '%',
        org_id, 'start_time'))
    html_code = flask.render_template('index.html',
        offerings=offerings)
    return flask.make_response(html_code)

#!/usr/bin/env python

#-----------------------------------------------------------------------
# app.py
# Authors: Aidan Phillips
# Main file for generating views for the mobile web app
#-----------------------------------------------------------------------
import flask
import database

app = flask.Flask(__name__, template_folder='templates',
    static_folder='static')

@app.route('/')
def index():
    offerings = database.find_offerings(('%', '%', '%', '%', '%', '%',
        'start_time'))
    html_code = flask.render_template('index.html', offerings=offerings)
    return flask.make_response(html_code)

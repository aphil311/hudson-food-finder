#!/usr/bin/env python

#-----------------------------------------------------------------------
# app.py
# Authors: Aidan Phillips
# Main file for generating views for the mobile web app
#-----------------------------------------------------------------------
import flask
import database

#-----------------------------------------------------------------------
app = flask.Flask(__name__, template_folder='templates',
    static_folder='static')
#-----------------------------------------------------------------------

#-----------------------------------------------------------------------
# index()
# Displays offerings in a list
#-----------------------------------------------------------------------
@app.route('/index')
@app.route('/')
def index():
    offerings = database.find_offerings(('', 'Offering.title'))
    html_code = flask.render_template('index.html', offerings=offerings)
    return flask.make_response(html_code)

#-----------------------------------------------------------------------
# search_results()
# Displays offerings in a list based on the search query
#-----------------------------------------------------------------------
@app.route('/search', methods=['GET'])
def search_results():
    search_term = flask.request.args.get('search')
    sort_by = flask.request.args.get('sort')
    query = (search_term, sort_by)
    offerings = database.find_offerings(query)
    html_code = flask.render_template('results.html', offerings=offerings)
    return flask.make_response(html_code)

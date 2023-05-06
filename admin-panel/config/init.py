#-----------------------------------------------------------------------
# This file is used to initialize the flask app and the database
# engine. It also sets the path to the templates and static folders.
#-----------------------------------------------------------------------

import os
import flask
import sqlalchemy
import psycopg2
from decouple import config
from config.definitions import ROOT_DIR

# get paths
templates = os.path.join(ROOT_DIR, 'templates')
static = os.path.join(ROOT_DIR, 'static')
_DATABASE_URL_ = config('DB_URL')

# initialize flask app and database engine
app = flask.Flask(__name__, template_folder=templates,
        static_folder=static)
engine = sqlalchemy.create_engine('postgresql://',
            creator=lambda: psycopg2.connect(_DATABASE_URL_))

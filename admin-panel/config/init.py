import flask
import os
import sqlalchemy
import psycopg2
from decouple import config
from config.definitions import ROOT_DIR

templates = os.path.join(ROOT_DIR, 'templates')
static = os.path.join(ROOT_DIR, 'static')
_DATABASE_URL_ = config('DB_URL')
app = flask.Flask(__name__, template_folder=templates,
        static_folder=static)
engine = sqlalchemy.create_engine('postgresql://',
            creator=lambda: psycopg2.connect(_DATABASE_URL_))

import flask
import sqlalchemy
import psycopg2
from decouple import config

_DATABASE_URL_ = config('DB_URL')
app = flask.Flask(__name__, template_folder='templates',
        static_folder='static')
engine = sqlalchemy.create_engine('postgresql://',
            creator=lambda: psycopg2.connect(_DATABASE_URL_))


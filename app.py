import flask

app = flask.Flask(__name__, template_folder='templates',
    static_folder='static')

@app.route('/')
def hello_world():
    html_code = flask.render_template('index.html')
    return flask.make_response(html_code)

import flask

app = flask.Flask(__name__)


@app.route('/')
def index():
    return flask.render_template("order.html")


@app.route('/about/')
def order():
    return flask.render_template("index.html")


app.run()

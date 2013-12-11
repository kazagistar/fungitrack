from flask import Flask, render_template, g
app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/test/geolocation')
def geotest():
    return render_template('geolocation_test.html')

app.pages = []

@app.before_request
def prepare_navbar_data():
    g.pages = list(app.pages)

@app.errorhandler(403)
def forbidden(e):
	return render_template("403.html"), 403

@app.errorhandler(404)
def not_found(e):
	return render_template("404.html"), 404
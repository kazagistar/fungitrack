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

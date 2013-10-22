#!python2

from flask import Flask, g, render_template
app = Flask(__name__)

# Database initialization
import sqlite3

@app.before_request
def init_db():
    g.db = sqlite3.connect('data.db')

@app.teardown_request
def close_db(exception):
    if getattr(g, 'db', None):
        g.db.close()


@app.route('/')
def hello():
    return render_template('layout.html')

if __name__ == "__main__":
    app.run(debug=True)

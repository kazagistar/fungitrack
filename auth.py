from flask import render_template, flash, request, session, redirect, g, abort
from routes import app

class User(object):
    def __init__(self, username):
        matches = app.db.execute('SELECT * FROM APP_USER WHERE Username=%s', username)
        self.name, self.id, self.description, self.lat, self.long = matches[0]
        print(self.id)

@app.before_request
def loaduser():
    try:
        g.user = User(session['username'])
    except:
        g.user = None
        session.pop('username', None)

from functools import wraps
def requires_login(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not g.user:
            abort(403)
        return func(*args, **kwargs)
    return wrapper

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    if username:
        session['username'] = username
        # Search for existing username
        matching = app.db.execute('SELECT User_id FROM APP_USER WHERE Username=%s', username)
        if len(matching) == 0:
            # Create new user
            flash('New user "%s" created' % username, 'info')
            app.db.execute('INSERT INTO APP_USER (Username) VALUES (%s)', username)
            return redirect('/profile')
        else:
            flash('Logged in as %s' % username, 'success')
    else:
        flash('No username specified', 'warning')
    return redirect(request.form['next'])

@app.route('/logout')
def logout():
    flash('Logged out', 'success')
    session.pop('username', None)
    return redirect('/')

@app.route('/profile')
@requires_login
def profile():
    flash('Profile page not yet implemented', 'warning')
    return render_template('layout.html')
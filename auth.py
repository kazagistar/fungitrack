from flask import render_template, flash, request, session, redirect, g, abort 

from routes import app


class User(object):
    def __init__(self, username):
        matches = app.db.execute('SELECT * FROM APP_USER WHERE Username=%s', username)
        self.name, self.id, self.description, self.latitude, self.longitude = matches[0]
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

from flask_wtf import Form
from wtforms import TextField, DecimalField
from wtforms.validators import DataRequired, NumberRange

class UserInfo(Form):
    description = TextField(
        label='Description')
    latitude = DecimalField(
        label='Latitude',
        validators=[NumberRange(-90,90)],
        rounding=4)
    longitude = DecimalField(
        label='Longitude',
        validators=[NumberRange(-180,180)],
        rounding=4)

@app.route('/profile', methods=['GET', 'POST'])
@requires_login
def profile():
    form = UserInfo(obj=g.user)
    if form.validate_on_submit():
        flash("User info changed!", 'success')
        print(form.data)
        print(dir(form.data['latitude']))
        return redirect('/profile')
    for field, errors in form.errors.items():
        for error in errors:
            flash('%s: %s' % (field, error), 'danger')
    return render_template('profile.html', form=form, options=["first", "second", "third"])

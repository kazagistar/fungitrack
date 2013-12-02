from flask import render_template, flash, request, session, redirect, g, abort 

from routes import app


class User(object):
    def __init__(self, username): # load
        matches = app.db.execute('SELECT * FROM APP_USER WHERE Username=%s', username)
        self.name, self.id, self.description, self.latitude, self.longitude = matches[0]
        # Fix types, cause mysql just returns everything as strings
        self.id = int(self.id)
        self.latitude = float(self.latitude) if self.latitude else None
        self.longitude = float(self.longitude) if self.longitude else None

    def save(self):
        app.db.execute(
            'UPDATE APP_USER SET User_description=%s, Home_Location_lat=%s, Home_Location_long=%s WHERE User_id=%s',
            self.description, self.latitude, self.longitude, self.id)

@app.before_request
def loaduser():
    try:
        g.user = User(session['username'])
    except (KeyError, IndexError):
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
from wtforms.validators import DataRequired, NumberRange, Optional, Length
from wtforms.widgets import TextArea

class UserInfo(Form):
    description = TextField(
        label='Description',
        validators=[Optional(), Length(min=1)],
        widget=TextArea())
    latitude = DecimalField(
        label='Latitude',
        validators=[Optional(), NumberRange(-90,90)],
        places=4)
    longitude = DecimalField(
        label='Longitude',
        validators=[Optional(), NumberRange(-180,180)],
        places=4)

@app.route('/profile', methods=['GET', 'POST'])
@requires_login
def profile():
    form = UserInfo(obj=g.user)
    if form.validate_on_submit():
        flash('User info changed!', 'success')
        form.populate_obj(g.user)
        g.user.save()
        return redirect('/profile')
    return render_template('profile.html', form=form)

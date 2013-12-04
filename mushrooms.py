# Flask imports
from flask import render_template, flash, request, session, redirect, g, abort 

# WTForms imports
from flask_wtf import Form
from wtforms import TextField, BooleanField, SelectField
from wtforms.validators import Optional, Length, URL
from wtforms.widgets import TextArea

# local imports
from routes import app
from auth import requires_login


app.pages.append(("Mushrooms", '/mushroom'))

@app.route('/mushroom')
def mushroom_list():
    return render_template("mushroom_list.html",
        mushrooms=app.db.execute("SELECT Genus, Species, Variety, Mushroom_id FROM MUSHROOM"),
        current="/mushroom")

class Mushroom:
    """ Data structure to make accessing mushroom data in a semantic way easier """
    def __init__(self, mushroom_id):
        match = app.db.execute(app.db.get_query('lookup_mushroom'), mushroom_id)[0]
        self.genus = match[0]
        self.species = match[1]
        self.variety = match[2]
        self.edible = match[3] > 0
        self.color = match[4]
        self.shape = match[5]
        self.gill = match[6]
        self.surface = match[7]
        self.link = match[8]
        self.description = match[9]

@app.route('/mushroom/<int:mushroom_id>')
def mushroom_details(mushroom_id):
    return render_template('mushroom_details.html',
        mushroom=Mushroom(mushroom_id),
        recipes=app.db.execute(app.db.get_query('lookup_mushroom_recipes'), mushroom_id),
        current="/mushroom")

class MushroomInfo(Form):
    genus = TextField(
        label='Genus',
        validators=[Optional(), Length(min=1, max=20)])
    species = TextField(
        label='Species',
        validators=[Optional(), Length(min=1, max=100)])
    variety = TextField(
        label='Variety',
        validators=[Optional(), Length(min=1, max=100)])
    description = TextField(
        label='Description',
        validators=[Optional(), Length(min=1)],
        widget=TextArea())
    link = TextField(
        label='External link',
        validators=[Optional(), URL()])
    edible = BooleanField(
        label='Edible')
    color = SelectField(
        label="Spore color",
        choices=[('','')],
        validators=[Optional()])
    shape = SelectField(
        label="Cap shape",
        choices=[('','')],
        validators=[Optional()])
    gill = SelectField(
        label="Gill attatchment",
        choices=[('','')],
        validators=[Optional()])
    surface = SelectField(
        label="Spore surface",
        choices=[('','')],
        validators=[Optional()])

@app.route('/mushroom/new', methods=['GET', 'POST'])
@requires_login
def mushroom_create():
    form = MushroomInfo()
    form.color.choices.extend(app.db.execute('SELECT * FROM SPORE_COLOR'))
    form.shape.choices.extend(app.db.execute('SELECT * FROM CAP_SHAPE'))
    form.gill.choices.extend(app.db.execute('SELECT * FROM GILL_ATTATCHMENT'))
    form.surface.choices.extend(app.db.execute('SELECT * FROM SPORE_SURFACE'))
    return render_template('mushroom_new.html', form=form)


app.pages.append(("Recipes", '/recipe'))

@app.route('/recipe')
def recipe_list():
    return render_template("recipe_list.html",
        recipes=app.db.execute("SELECT Recipe_name, Recipe_id FROM RECIPE"),
        current="/recipe")

@app.route('/recipe/<int:recipe_id>')
def recipe_details(recipe_id):
    name, desc = app.db.execute('SELECT Recipe_name, Recipe_desc FROM RECIPE WHERE Recipe_id=%s', recipe_id)[0]
    return render_template('recipe_details.html',
        mushroom=Mushroom(recipe_id),
        name=name,
        ingredients=app.db.execute(app.db.get_query('lookup_recipe_mushrooms'), recipe_id),
        description=desc,
        current="/recipe")

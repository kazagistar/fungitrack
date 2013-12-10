# Flask imports
from flask import render_template, flash, request, session, redirect, g, abort 

# WTForms imports
from flask_wtf import Form
from wtforms import TextField, BooleanField, SelectField, DecimalField, IntegerField, DateField
from wtforms.validators import Optional, Length, URL, NumberRange
from wtforms.widgets import TextArea

# local imports
from routes import app
from auth import requires_login


app.pages.append(("Mushrooms", '/mushroom'))

@app.route('/mushroom')
def mushroom_list():
    return render_template("mushroom_list.html",
        items=app.db.execute("SELECT Genus, Species, Variety, Mushroom_id FROM MUSHROOM"),
        title="Mushroom List",
        newlink="/mushroom/new",
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

    @staticmethod
    def normalize_name(*names):
        return " ".join(name for name in names if name)

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
        validators=[Optional()])
    shape = SelectField(
        label="Cap shape",
        validators=[Optional()])
    gill = SelectField(
        label="Gill attatchment",
        validators=[Optional()])
    surface = SelectField(
        label="Spore surface",
        validators=[Optional()])


def fetch_choices(source, destination):
    results = app.db.execute('SELECT * FROM %s' % source)
    destination.choices = [('','')] + [(str(id), str(text)) for id, text in results]

def fetch_mushroom(destination):
    results = app.db.execute('SELECT Genus, Species, Variety, Mushroom_id from MUSHROOM')
    destination.choices = [(str(id), Mushroom.normalize_name(genus, species, variety)) for genus, species, variety, id in results]

@app.route('/mushroom/new', methods=['GET', 'POST'])
@requires_login
def mushroom_create():
    form = MushroomInfo()
    fetch_choices('SPORE_COLOR', form.color)
    fetch_choices('CAP_SHAPE', form.shape)
    fetch_choices('GILL_ATTATCHMENT', form.gill)
    fetch_choices('SPORE_SURFACE', form.surface)
    if form.validate_on_submit():
        app.db.execute(
            """
                INSERT INTO MUSHROOM 
                (Genus,Species,Variety,Edible,Spore_color_id,Cap_shape_id,Gill_attatchment_id,Spore_surface_id,Link,Description)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """,
            form.genus.data,
            form.species.data,
            form.variety.data,
            form.edible.data,
            form.color.data,
            form.shape.data,
            form.gill.data,
            form.surface.data,
            form.link.data,
            form.description.data)
        flash('Mushroom %s %s added' % (form.genus, form.species), 'success')
        return redirect('/mushroom/{id}'.format(
            id=app.db.execute('SELECT MAX(Mushroom_id) FROM MUSHROOM')[0][0]))
    return render_template('mushroom_new.html',
        form=form,
        current='/mushroom')

class IdInfo(Form):
    color = SelectField(
        label="Spore color",
        validators=[Optional()])
    shape = SelectField(
        label="Cap shape",
        validators=[Optional()])
    gill = SelectField(
        label="Gill attatchment",
        validators=[Optional()])
    surface = SelectField(
        label="Spore surface",
        validators=[Optional()])

app.pages.append(("Identify", '/identify_mushroom'))
@app.route('/identify_mushroom')
def get_id_info():
    form = IdInfo()
    fetch_choices('SPORE_COLOR', form.color)
    fetch_choices('CAP_SHAPE', form.shape)
    fetch_choices('GILL_ATTATCHMENT', form.gill)
    fetch_choices('SPORE_SURFACE', form.surface)
    return render_template('identify_mushroom.html',form=form, current='/identify_mushroom' )


app.pages.append(("Recipes", '/recipe'))
@app.route('/recipe')
def recipe_list():
    return render_template("recipe_list.html",
        items=app.db.execute("SELECT Recipe_name, Recipe_id FROM RECIPE"),
        title="Recipe List",
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

app.pages.append(("Submit a Find", '/mushroom_find_new'))

@app.route('/mushroom_find_new', methods = ['GET', 'POST'])
@requires_login
def make_find():
    form = FindInfo()
    fetch_mushroom(form.mushroom)
    if form.validate_on_submit():
         app.db.execute(
            """
                INSERT INTO MUSHROOM_FIND 
                (User_id, Mushroom_id, Found_lat, Found_long, Found_date, Quantity)
                VALUES (%s,%s,%s,%s,%s,%s)
            """,
            g.user.id,
            form.mushroom.data,
            form.latitude.data,
            form.longitude.data,
            form.date.data,
            form.quantity.data)
         flash('Find added', 'success')
    return render_template('mushroom_find_new.html', form = form, current = '/mushroom_find_new')
    

class FindInfo(Form):    
    mushroom = SelectField(
        label = 'Mushroom',
        validators = [Optional()])
    latitude = DecimalField(
        label='Latitude',
        validators=[Optional(), NumberRange(-90,90)],
        places=4)
    longitude = DecimalField(
        label='Longitude',
        validators=[Optional(), NumberRange(-180,180)],
        places=4)
    date = DateField(
        label = 'Date',
        validators = [Optional()])
    quantity = IntegerField(
        label = 'Quantity',
        validators=[Optional()])


app.pages.append(("Find Nearby", '/find_nearby'))

DISTANCE_CAP = 100

class FindQueryForm(Form):
    latitude = DecimalField(
        label='Latitude',
        validators=[NumberRange(-90,90)],
        places=4)
    longitude = DecimalField(
        label='Longitude',
        validators=[NumberRange(-180,180)],
        places=4)
    distance = DecimalField(
        label='Distance (km)',
        #validators=[NumberRange(0, DISTANCE_CAP)],
        places=4)

def wrap_find_result(find):
    result = dict(zip(('mushroom_id', 'latitude', 'longitude', 'date', 'quantity', 'genus', 'species', 'variety'), find))
    result['name'] = Mushroom.normalize_name(result['genus'], result['species'], result['variety'])
    result['coord'] = str(result['latitude']) + ',' + str(result['longitude'])
    return result

@app.route('/find_nearby', methods = ['GET', 'POST'])
@requires_login
def find_nearby():
    form = FindQueryForm()
    if form.validate_on_submit():
        query = app.db.get_query("get_nearby_finds")
        nearby = app.db.execute(query, form.longitude.data, form.latitude.data, form.latitude.data, form.distance.data)
        nearby = [wrap_find_result(find) for find in nearby]
        return render_template("mushroom_finds.html", nearby = nearby, params = form, current = '/find_nearby')
    return render_template('find_nearby_form.html', form = form, current = '/find_nearby')
    

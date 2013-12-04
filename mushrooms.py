from flask import render_template, flash, request, session, redirect, g, abort 

from routes import app


app.pages.append(("Mushrooms", '/mushroom'))
@app.route('/mushroom')
def mushroom_list():
    return render_template("mushroom_list.html",
        mushrooms=app.db.execute("SELECT Genus, Species, Variety, Mushroom_id FROM MUSHROOM"),
        current = "/mushroom")

class Mushroom:
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
    print "DARTATATATSQDFASDFA"
    print str(app.db.execute(app.db.get_query('lookup_mushroom_recipes'), mushroom_id))
    return render_template('mushroom_details.html',
        mushroom=Mushroom(mushroom_id),
        recipes=app.db.execute(app.db.get_query('lookup_mushroom_recipes'), mushroom_id),
        current="/mushroom")


app.pages.append(("Recipes", '/recipe'))
@app.route('/recipe')
def recipe_list():
    return render_template("recipe_list.html",
        recipes=app.db.execute("SELECT Recipe_name, Recipe_id FROM RECIPE"),
        current="/recipe")

@app.route('/recipe/<int:recipe_id>')
def recipe_details(recipe_id):
    match = app.db.execute('SELECT Recipe_name, Recipe_desc FROM RECIPE WHERE Recipe_id=%s', recipe_id)[0]
    return render_template('recipe_details.html',
        mushroom=Mushroom(recipe_id),
        name=match[0],
        description=match[1],
        current = "/recipe")
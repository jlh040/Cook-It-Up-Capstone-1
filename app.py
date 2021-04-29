from flask import Flask, session, g, flash, render_template, redirect, request
from models import db, connect_db, User, Recipe
from flask_debugtoolbar import DebugToolbarExtension
from secret_keys import API_KEY, SECRET_KEY

import requests
import os

CURR_USER_KEY = 'curr_user'

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql:///cook-it-up-db')
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = SECRET_KEY
debug = DebugToolbarExtension(app)

connect_db(app)

@app.before_request
def add_user_to_global():
    """Add user to the g object."""

    if session.get(CURR_USER_KEY):
        # If the user's id is in the session, put them in the g object
        g.user = User.query.get(session[CURR_USER_KEY])
    else:
        # Otherwise, do not put any user in the g object
        g.user = None

@app.route('/', methods=['GET'])
def show_homepage():
    """Show the site's homepage."""

    if g.user or True:
        # If a user is logged in take them to the main homepage
        return render_template('home.html', cuisines=Recipe.all_cuisines())
    else:
        # Otherwise take them to the anonymous homepage
        return render_template('home_anon.html')

@app.route('/recipes')
def show_recipes():
    """Show a list of recipes."""
    recipe_query = request.args.get('recipe')

    if recipe_query:
        return render_template('recipe-list.html', recipe_query=recipe_query)
    else:
        return render_template('recipe-list.html')

@app.route('/recipes/cuisines/<cuisine_type>', methods=['GET'])
def show_recipes_by_cuisine(cuisine_type):
    """Show recipes by their cuisine type."""
    recipes_by_cuisine = Recipe.get_recipes_by_cuisine(cuisine_type)

    return render_template('cuisine-page.html', recipes=recipes_by_cuisine, cuisine=cuisine_type)

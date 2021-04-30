from flask import Flask, session, g, flash, render_template, redirect, request
from models import db, connect_db, User, Recipe
from flask_debugtoolbar import DebugToolbarExtension
from secret_keys import API_KEY, SECRET_KEY
from helper_funcs import list_of_cuisines

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
        return render_template('home.html', cuisines=list_of_cuisines)
    else:
        # Otherwise take them to the anonymous homepage
        return render_template('home_anon.html')

@app.route('/cuisines/<cuisine_type>', methods=['GET'])
def list_recipes_by_cuisine(cuisine_type):
    """Show a list of recipes by cuisine type."""
    recipes = Recipe.get_recipes_by_cuisine(cuisine_type)
    recipes.sort(key=lambda x: x[1])

    return render_template('recipes_by_cuisine.html', recipes=recipes, cuisine_type=cuisine_type)

@app.route('/recipes', methods=['GET'])
def list_recipes_by_query():
    """List all recipes based upon a search query."""
    # Get the query param from the url
    query = request.args['query']
    # Get all recipes found from that query and then sort
    recipes = Recipe.get_recipes_by_query(query)
    recipes.sort(key=lambda x: x[1])

    # Pass the recipes into the template to display to the user
    return render_template('recipes_by_query.html', recipes=recipes)

@app.route('/recipes/<int:id>', methods=['GET'])
def show_recipe_by_id(id):
    """Show a recipe's nformation."""
    # Get the title, image, and ingredients
    recipe_info = Recipe.get_recipe_info(id)

    # Get the equipement
    recipe_equip = Recipe.get_equipment_for_recipe(id)['equipment']

    # Get the instructions
    recipt_inst = Recipe.get_instructions_for_recipe(id)

    return render_template('single_recipe.html',
                             recipe_info=recipe_info,
                             recipe_equip=recipe_equip,
                             recipe_inst=recipt_inst)
    

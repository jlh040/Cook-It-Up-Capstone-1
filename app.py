from flask import Flask, session, g, flash, render_template, redirect, request
from models import db, connect_db, User, Recipe
from forms import SignupForm, LoginForm, EditUserForm, SearchForm
from flask_debugtoolbar import DebugToolbarExtension
from secret_keys import API_KEY, SECRET_KEY
from helper_funcs import list_of_cuisines, check_for_no_image, heroku_db_url

import requests
import os

CURR_USER_KEY = 'curr_user'

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = heroku_db_url()
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', SECRET_KEY)
debug = DebugToolbarExtension(app)

connect_db(app)

# Add 'cooked-it' table to show if you've cooked something (possibility)

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
    if g.user:
        # If a user is logged in take them to the main homepage
        form = SearchForm()
        return render_template('home.html', form=form, cuisines=list_of_cuisines)
    else:
        # Otherwise take them to the anonymous homepage
        return render_template('home_anon.html')

@app.route('/cuisines/<cuisine_type>', methods=['GET'])
def list_recipes_by_cuisine(cuisine_type):
    """Show a list of recipes by cuisine type."""
    if g.user:
        recipes = Recipe.get_recipes_by_cuisine(cuisine_type)
        recipes.sort(key=lambda x: x[1])

        return render_template('recipes_by_cuisine.html', recipes=recipes, cuisine_type=cuisine_type)
    else:
        flash('Log in or make an account to view this', 'danger')
        return redirect('/')

@app.route('/recipes', methods=['GET', 'POST'])
def list_recipes_by_query():
    """List all recipes based upon a search query
    and number of calories.
    """
    form = SearchForm()

    if not g.user:
        flash('Unauthorized to view this', 'danger')
        return redirect('/')

    if form.validate_on_submit():
        # Get the search query and number of calories
        query = form.recipe_name.data
        num_of_cals = form.num_of_cals.data

        # Get all recipes found using the above data
        recipes = Recipe.get_recipes_by_query_and_cals(query, num_of_cals)
        recipes.sort(key=lambda x: x[1])

        # Pass the recipes into the template to display to the user
        return render_template('recipes_by_query.html', recipes=recipes, query=query)
    else:
        flash('Enter a search term first', 'info')
        return redirect('/')
    
    

@app.route('/recipes/<int:id>', methods=['GET'])
def show_recipe_by_id(id):
    """Show a recipe's nformation."""

    if not g.user:
        flash('Unauthorized to view this', 'danger')
        return redirect('/')

    # Get the title, image, and ingredients
    recipe_info = Recipe.get_recipe_info(id)

    # Get the equipement
    recipe_equip = Recipe.get_equipment_for_recipe(id)['equipment']

    # Get the instructions
    recipt_inst = Recipe.get_instructions_for_recipe(id)

    return render_template('single_recipe.html',
                             recipe_info=recipe_info,
                             recipe_equip=recipe_equip,
                             recipe_inst=recipt_inst,
                             id=id)

@app.route('/signup', methods=['GET', 'POST'])
def user_signup():
    """Sign the user up."""
    form = SignupForm()
    check_for_no_image(form)
    
    if form.validate_on_submit():
        user = User.signup(
            username=form.username.data,
            password=form.password.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            image_url=form.image_url.data,
            email=form.email.data
        )

        db.session.add(user)
        db.session.commit()
        session[CURR_USER_KEY] = user.id

        flash('You successfully signed up!', 'success')
        return redirect('/')
    elif not form.validate_on_submit() and request.method == 'POST':
        flash('Please enter a valid email', 'danger')

    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_user():
    """Log a user in (after authentication)."""
    form = LoginForm()

    if form.validate_on_submit():
        user = User.login(form.username.data, form.password.data)

        if user:
            session[CURR_USER_KEY] = user.id
            flash('Welcome back', 'success')
            return redirect('/')
        else:
            flash('Invalid credentials!', 'danger')
            return redirect('/login')
    elif not form.validate_on_submit() and request.method == 'POST':
        flash('Not authorized to do this', 'danger')

    return render_template('login.html', form=form)

@app.route('/logout', methods=['POST']) #Make this a post route
def logout_user():
    """Clear the session and log the user out."""
    if g.user:
        session.clear()
        flash('See you soon!', 'info')
    else:
        flash('Not authorized to do that')
    return redirect('/')

@app.route('/users/<int:id>', methods=['GET'])
def show_users_page(id):
    """Go to the user's page."""
    # Make sure the user is authenticated
    if not session.get(CURR_USER_KEY):
        flash('Not authorized to go here', 'danger')
        return redirect('/')
    elif session.get(CURR_USER_KEY) != id:
        flash('Not authorized to view this', 'danger')
        return redirect('/')
    
    # Get the user's favorite recipes
    users_fav_recipes = Recipe.get_multiple_recipes(g.user.favorite_recipes)
  
    return render_template('user.html', user=g.user, recipes=users_fav_recipes)

@app.route('/users/<int:id>/edit', methods=['GET', 'POST'])
def edit_user(id):
    """Edit a user's information."""

    if not g.user or not g.user.id == id:
        flash('Not authorized to view this page', 'danger')
        return redirect('/')

    user = User.query.get(id)
    form = EditUserForm(obj=user)

    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        flash('Edit Successful!', 'success')
        return redirect(f'/users/{id}')
    elif not form.validate_on_submit() and request.method == 'POST':
        flash('Please enter valid information', 'danger')
        return redirect(f'/users/{id}/edit')

    return render_template('edit_user.html', user=user, form=form)

@app.route('/recipes/<int:id>/favorite', methods=['POST'])
def add_recipe_to_favorites(id):
    """Add a recipe to a user's favorites."""

    if not g.user:
        flash('Not authorized to do this', 'danger')
        return redirect('/')
    elif id in [obj.id for obj in g.user.favorite_recipes]:
        flash('You already favorited this recipe', 'danger')
        return redirect(f'/recipes/{id}')

    recipe = Recipe.query.filter_by(api_id=id).one()
    g.user.favorite_recipes.append(recipe)

    db.session.commit()

    flash('Added to favorites!', 'success')
    return redirect(f'/recipes/{id}')

@app.route('/recipes/<int:id>/unfavorite', methods=['POST'])
def unfavorite_recipe(id):
    """Remove this recipe from a user's favorites."""

    if not g.user:
        flash('Not authorized to do this', 'danger')
        return redirect('/')
    elif id not in [obj.id for obj in g.user.favorite_recipes]:
        flash('You haven\'t favorited this recipe', 'danger')
        return redirect(f'/recipes/{id}')

    fav_recipe = Recipe.query.get(id)
    g.user.favorite_recipes.remove(fav_recipe)
    db.session.commit()

    flash('Removed from favorites!', 'info')
    return redirect(f'/recipes/{id}')
from flask import Flask, session, g, flash, render_template, redirect
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
    """If a user is logged in, put them in the g object."""

    if session.get(CURR_USER_KEY):
        g.user = User.query.get(session[CURR_USER_KEY])
    else:
        g.user = None

@app.route('/')
def show_homepage():
    """Show the site's homepage."""

    if g.user:
        # If a user is logged in take them to the main homepage
        return render_template('home.html')
    else:
        # Otherwise take them to the anonymous homepage
        return render_template('home_anon.html')

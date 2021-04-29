from flask_sqlalchemy import SQLAlchemy
from secret_keys import API_KEY
from helper_funcs import make_additional_calls
import requests

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    """Represents a user in the database."""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer, 
        autoincrement= True, 
        primary_key = True
    )

    username = db.Column(
        db.String(25), 
        unique = True, 
        nullable = False
    )
    
    password = db.Column(
        db.Text,
        nullable = False
    )

    first_name = db.Column(
        db.String(20), 
        nullable = False
    )

    last_name = db.Column(
        db.String(20)
    )

    image_url = db.Column(
        db.Text, 
        default = 'https://tinyurl.com/profile-default-image'
    )

    email = db.Column(
        db.Text,
        unique = True,
        nullable = False
    )

    favorite_recipes = db.relationship(
        'Recipe', 
        secondary = 'users_recipes'
    )

    def __repr__(self):
        """Create a representation of the user."""
        return f'<User: {self.username}, id: {self.id}>'

class UserRecipe(db.Model):
    """Associates users and their favorite recipes."""

    __tablename__ = 'users_recipes'

    id = db.Column(
        db.Integer, 
        autoincrement = True, 
        primary_key = True
    )

    user_id = db.Column(
        db.Integer, 
        db.ForeignKey('users.id')
    )

    recipe_id = db.Column(
        db.Integer, 
        db.ForeignKey('recipes.id')
    )

class Recipe(db.Model):
    """Represents a recipe in the database."""

    __tablename__ = 'recipes'

    id = db.Column(
        db.Integer, 
        autoincrement = True, 
        primary_key = True
    )

    api_id = db.Column(
        db.Integer, 
        unique = True, 
        nullable = False
    )

    def __repr__(self):
        """Create a representation of a recipe."""
        return f'<id: {self.id}, api_id: {self.api_id}>'

    @classmethod
    def all_cuisines(cls):
        """Return a list of all cuisines."""
        list_of_cuisines = [
            'African',
            'American',
            'British',
            'Cajun',
            'Caribbean',
            'Chinese',
            'Eastern European',
            'European',
            'French',
            'German',
            'Greek',
            'Indian',
            'Irish',
            'Italian',
            'Japanese',
            'Jewish',
            'Korean',
            'Latin American',
            'Mediterranean',
            'Mexican',
            'Middle Eastern',
            'Nordic',
            'Southern',
            'Spanish',
            'Thai',
            'Vietnamese'
        ]
        return list_of_cuisines
    
    @classmethod
    def get_recipes_by_cuisine(self, cuisine_name):
        """Search for a list of recipes by cuisine name."""
        api_endpoint = 'https://api.spoonacular.com/recipes/complexSearch'

        resp = requests.get(api_endpoint, params = {
            'cuisine': cuisine_name,
            'apiKey': API_KEY,
            'number': 100
        })
        list_of_recipe_titles = [(dictt['id'], dictt['title']) for dictt in resp.json()['results']]
        list_of_recipe_titles = make_additional_calls(resp, list_of_recipe_titles, cuisine_name)

        return list_of_recipe_titles


        




    
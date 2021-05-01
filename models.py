from flask_sqlalchemy import SQLAlchemy
from secret_keys import API_KEY
from helper_funcs import make_additional_calls, get_ingredients_from_recipe
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

    favorite_recipes = db.relationship( # Changed to 'cooked-recipes' ?
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
    def get_recipes_by_cuisine(cls, cuisine_name):
        """Search for a list of recipes by cuisine name."""
        api_endpoint = 'https://api.spoonacular.com/recipes/complexSearch'

        resp = requests.get(api_endpoint, params = {
            'cuisine': cuisine_name,
            'apiKey': API_KEY,
            'number': 100,
            'instructionsRequired': True
        })
        list_of_recipe_titles = [(dictt['id'], dictt['title']) for dictt in resp.json()['results']]
        list_of_recipe_titles = make_additional_calls(resp, list_of_recipe_titles, cuisine_name=cuisine_name)

        return list_of_recipe_titles
    
    @classmethod
    def get_recipes_by_query(cls, query):
        """Search for a list of recipes by a query term."""
        api_endpoint = 'https://api.spoonacular.com/recipes/complexSearch'

        resp = requests.get(api_endpoint, params = {
            'query': query,
            'apiKey': API_KEY,
            'number': 100,
            'instructionsRequired': True
        })

        list_of_recipe_titles = [(dictt['id'], dictt['title']) for dictt in resp.json()['results']]
        list_of_recipe_titles = make_additional_calls(resp, list_of_recipe_titles, query=query)

        return list_of_recipe_titles
    
    @classmethod
    def get_recipe_info(cls, id):
        """Return a recipe's meta-info by id."""
        api_endpoint = f'https://api.spoonacular.com/recipes/{id}/information'

        resp = requests.get(api_endpoint, params = {'apiKey': API_KEY})

        title = resp.json()['title']
        image_url = resp.json().get('image', 'https://tinyurl.com/ymxdeb5y')
        ingredients = get_ingredients_from_recipe(resp)

        return (title, image_url, ingredients)
    
    @classmethod
    def get_equipment_for_recipe(cls, id):
        """Get a recipe's equipment."""
        api_endpoint = f'https://api.spoonacular.com/recipes/{id}/equipmentWidget.json'

        resp = requests.get(api_endpoint, params={'apiKey': API_KEY})

        return resp.json()
    
    @classmethod
    def get_instructions_for_recipe(cls, id):
        """Get a recipe's instructions."""
        api_endpoint = f'https://api.spoonacular.com/recipes/{id}/analyzedInstructions'

        resp = requests.get(api_endpoint, params = {
            'apiKey': API_KEY,
        })

        list_of_instructions = [
            (obj['number'], obj['step']) for obj in resp.json()[0]['steps']
        ]

        return list_of_instructions


    







        




    
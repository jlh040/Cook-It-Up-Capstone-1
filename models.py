from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from secret_keys import API_KEY
from helper_funcs import make_additional_calls, get_ingredients_from_recipe
import requests
import json

db = SQLAlchemy()
bcrypt = Bcrypt()

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
    
    @classmethod
    def signup(cls, username, password, first_name, email, last_name=None, image_url=None):
        """Register user w/ hashed password and return the user."""

        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode('utf8')

        return cls(
            username=username,
            password=hashed_utf8,
            first_name=first_name,
            last_name=last_name,
            image_url=image_url,
            email=email
        )
    
    @classmethod
    def login(cls, username, password):
        """Return the user if they can be authenticated,
        otherwise return False.
        """
        user = User.query.filter(User.username == username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False

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
    def get_recipes_by_query_and_cals(cls, query, cals):
        """Search for a list of recipes by a query term."""
        api_endpoint = 'https://api.spoonacular.com/recipes/complexSearch'

        resp = requests.get(api_endpoint, params = {
            'query': query,
            'apiKey': API_KEY,
            'number': 100,
            'maxCalories': cals,
            'instructionsRequired': True
        })
       
        list_of_recipe_titles = [(dictt['id'], dictt['title']) for dictt in resp.json()['results']]
        list_of_recipe_titles = make_additional_calls(resp, list_of_recipe_titles, query=query, cals=cals)

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
    
    @classmethod
    def get_multiple_recipes(cls, list_of_recipe_objs):
        """Get multiple recipes at once."""
        api_endpoint = 'https://api.spoonacular.com/recipes/informationBulk'
        api_ids = [str(obj.api_id) for obj in list_of_recipe_objs]

        resp = requests.get(api_endpoint, params = {
            'apiKey': API_KEY,
            'ids': ','.join(api_ids)
        })
        
        recipe_list = [(obj['id'], obj['title'], obj['image']) for obj in resp.json()]
        return recipe_list



    







        




    
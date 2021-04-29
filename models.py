from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.model):
    """Represents a user in the database."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, autoincrement= True, primary_key = True)
    username = db.Column(db.String(25), unique = True, nullable = False)
    first_name = db.Column(db.String(20), nullable = False)
    last_name = db.Column(db.String(20))
    image_url = db.Column(db.Text, default = 'https://tinyurl.com/profile-default-image')
    email = db.Column(db.Text, nullable = False)

    favorite_recipes = db.relationship('Recipe', secondary = 'UsersRecipes')

class UsersRecipes(db.Model):
    """Associates users and their favorite recipes."""

    __tablename__ = 'favorite_recipes'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))

class Recipe(db.Model):
    """Represents a recipe in the database."""

    __tablename__ = 'recipes'

    id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    api_id = db.Column(db.Integer, unique = True, nullable = False)

    
from app import app
from models import db, User, Recipe, UserRecipe

def fill_recipe_table():
    for num in range(200001, 500000):
        recipe = Recipe(api_id=num)
        db.session.add(recipe)

db.create_all()

fill_recipe_table()

db.session.commit()

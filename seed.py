from app import app
from models import db, User, Recipe, UserRecipe

def fill_recipe_table():
    for num in range(1, 600000):
        recipe = Recipe(api_id=num)
        db.session.add(recipe)
    db.session.commit()

db.drop_all()
db.create_all()


db.session.add_all([test_user_1, test_user_2, test_user_3])
db.session.commit()

fill_recipe_table()

db.session.commit()

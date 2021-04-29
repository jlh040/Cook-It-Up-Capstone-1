from app import app
from models import db, User, Recipe, UserRecipe

db.drop_all()
db.create_all()

test_user_1 = User(
    username = 'chefguy22',
    password = '3mx8z9c',
    first_name = 'Bob',
    last_name = 'Heller',
    email = 'what88@gmail.com'
)

test_user_2 = User(
    username = 'gordon76',
    password = 'very_tedious_password',
    first_name = 'Gordon',
    last_name = 'Ramsay',
    email = '5michelinstars@yahoo.com'
)

test_user_3 = User(
    username = 'emeril_wannabe98',
    password = 'dip676',
    first_name = 'Mike',
    last_name = 'Chino',
    image_url = 'https://tinyurl.com/4trndw4h',
    email = 'some_email@yahoo.com'
)

db.session.add_all([test_user_1, test_user_2, test_user_3])
db.session.commit()

test_recipe_1 = Recipe(
    api_id = 642539
)

test_recipe_2 = Recipe(
    api_id = 663357
)

db.session.add_all([test_recipe_1, test_recipe_2])
db.session.commit()

test_user_2.favorite_recipes.extend([test_recipe_1, test_recipe_2])

db.session.commit()

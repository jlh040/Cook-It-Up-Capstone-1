from app import app
from models import db, User, Recipe

test_user_1 = User(
    username = 'chefguy22',
    first_name = 'Bob',
    last_name = 'Heller',
    email="what88@gmail.com"
)

test_user_2 = User(
    username = 'gordon76',
    password = 'very_tedious_password'
    first_name = 'Gordon',
    last_name = 'Ramsay',
    email="5michelinstars@yahoo.com"
)

test_user_3 = User(
    username = 'emeril_wannabe98',
    password = 'dip676'
    first_name = 'Mike',
    last_name = 'Chino',
    image_url = 'https://tinyurl.com/4trndw4h'
    email="some_email@yahoo.com"
)

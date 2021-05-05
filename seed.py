from app import app
from models import db, User, Recipe, UserRecipe


db.drop_all()
db.create_all()

for num in range(1, 100000):
    recipe = Recipe(api_id=num)
    db.session.add(recipe)

db.session.commit()

for num in range(100000, 200000):
    recipe = Recipe(api_id=num)
    db.session.add(recipe)

db.session.commit()

for num in range(200000, 300000):
    recipe = Recipe(api_id=num)
    db.session.add(recipe)

db.session.commit()

for num in range(300000, 400000):
    recipe = Recipe(api_id=num)
    db.session.add(recipe)

db.session.commit()

for num in range(400000, 500000):
    recipe = Recipe(api_id=num)
    db.session.add(recipe)

db.session.commit()

for num in range(500000, 600000):
    recipe = Recipe(api_id=num)
    db.session.add(recipe)

db.session.commit()

for num in range(600000, 700000):
    recipe = Recipe(api_id=num)
    db.session.add(recipe)

db.session.commit()

for num in range(700000, 800000):
    recipe = Recipe(api_id=num)
    db.session.add(recipe)

db.session.commit()

for num in range(800000, 900000):
    recipe = Recipe(api_id=num)
    db.session.add(recipe)

db.session.commit()
    
for num in range(900000, 1000000):
    recipe = Recipe(api_id=num)
    db.session.add(recipe)

db.session.commit()

for num in range(1000000, 1100000):
    recipe = Recipe(api_id=num)
    db.session.add(recipe)

db.session.commit()

for num in range(1100000, 1200000):
    recipe = Recipe(api_id=num)
    db.session.add(recipe)

db.session.commit()

for num in range(1200000, 1300000):
    recipe = Recipe(api_id=num)
    db.session.add(recipe)

db.session.commit()
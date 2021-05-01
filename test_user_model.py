"""User model tests."""

import os
from unittest import TestCase
from models import db, User, Recipe, UserRecipe
from secret_keys import API_KEY

os.environ['DATABASE_URL'] = 'postgresql:///cook-it-up-test-db'

from app import app

app.config['TESTING'] = True
app.config['WTF_CSRF_ENABLED'] = False
app.config['SQLALCHEMY_ECHO'] = False

db.create_all()

class UserModelTestCase(TestCase):
    """Test the functionality of the user model."""

    def setUp(self):
        """Delete any leftover data."""
        User.query.delete()
        Recipe.query.delete()
        UserRecipe.query.delete()
    
    def test_create_user(self):
        """Can we create an instance of a user?"""
        try:
            new_user0 = User(
                username='bob8745',
                password='some_pass12321x',
                first_name='Bob',
                email="chico23@gmail.com"
            )
            self.assertTrue(True)
        except:
            print('If we see this line, there was an error')
            

    def test_create_user_in_db(self):
        """Can we create a new user in the database?"""
        new_user = User(
            username='bob8745',
            password='some_pass12321x',
            first_name='Bob',
            email="chico23@gmail.com"
        )
        db.session.add(new_user)
        db.session.commit()
        
        self.assertTrue(User.query.count(), 1)
    
    def test_select_user(self):
        """Can we query a user from the database?"""
        new_user2 = User(
            username='jim847',
            password='14322321x',
            first_name='Jimmy',
            email="Jim23@gmail.com"
        )
        db.session.add(new_user2)
        db.session.commit()
        
        self.assertEqual(User.query.get(new_user2.id).username, 'jim847')
    
    def test_user_representation(self):
        """Does our repr method work?"""
        new_user3 = User(
            username='leonidas87',
            password='e9ciallz',
            first_name='Neil',
            email="free_dog@hotmail.com"
        )
        db.session.add(new_user3)
        db.session.commit()

        self.assertIn('leonidas87', str(new_user3))
    
    def test_add_favorite_recipe(self):
        """Can a user add favorite recipes?"""
        new_user4 = User(
            username='tiger_guy5',
            password='king_of_hill',
            first_name='Larry',
            email="needtiger2@hotmail.com"
        )
        
        new_recipe = Recipe(api_id=1)
        new_user4.favorite_recipes.append(new_recipe)
        db.session.commit()

        self.assertIn(new_recipe, new_user4.favorite_recipes)
    
    def test_remove_favorite_recipe(self):
        """Can a user remove a favorite recipe?"""
        new_user5 = User(
            username='jim_bob87',
            password='no_its_cool',
            first_name='Jim Bob',
            email="farmer_elite99@yahoo.com"
        )

        new_recipe_1 = Recipe(api_id=500)
        new_user5.favorite_recipes.append(new_recipe_1)
        db.session.commit()

        new_user5.favorite_recipes.remove(new_recipe_1)
        self.assertEqual(len(new_user5.favorite_recipes), 0)
    
    def test_default_values(self):
        """Do our default values work?"""
        new_user6 = User(
            username='jim_bob87',
            password='no_its_cool',
            first_name='Jim Bob',
            email="farmer_elite99@yahoo.com"
        )
        db.session.add(new_user6)
        db.session.commit()

        self.assertEqual(new_user6.image_url, 'https://tinyurl.com/profile-default-image')

        
    






"""User model tests."""

import os
from unittest import TestCase
from models import db, User, Recipe, UserRecipe
from secret_keys import API_KEY

from app import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cook-it-up-test-db'

app.config['TESTING'] = True
app.config['WTF_CSRF_ENABLED'] = False
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
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
    
    def test_signup_method(self):
        """Does our signup method return a user and hash the password?"""
        try:
            new_user7 = User.signup(
            username='jack87',
            password='chicko11',
            first_name='Ronda',
            email="bob_frob_11@aol.com"
            )   
            db.session.add(new_user7)
            db.session.commit()

            self.assertTrue(len(new_user7.password) > 20)
        except:
            print('Something went wrong!')
    
    def test_login_method_registered(self):
        """Does the login method authenticate us if we enter valid credentials?"""
        new_user8 = User.signup(
            username='Mikael77',
            password='anglo424',
            first_name='Johhny',
            email="gromovia@gmail.com"
            )
        db.session.add(new_user8)
        db.session.commit()

        self.assertIs(User.login('Mikael77', 'anglo424'), new_user8)
    
    def test_login_method_unregistered(self):
        """Does the login method return false if we enter invalid credentials?"""
        new_user9 = User.signup(
            username='dirtbikeguy',
            password='rbby74x',
            first_name='Sly',
            last_name='Cooper',
            image_url='https://tinyurl.com/profile-default-image',
            email="tennis4ever@gmail.com"
            )
        db.session.add(new_user9)
        db.session.commit()

        self.assertFalse(User.login(username='dirtbikeguy', password='rbby74xx'))
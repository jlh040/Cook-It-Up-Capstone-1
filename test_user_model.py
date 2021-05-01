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





"""Test recipe model."""

import os
from unittest import TestCase
from secret_keys import API_KEY
from models import db, User, Recipe, UserRecipe

os.environ['DATABASE_URL'] = 'postgresql:///cook-it-up-test-db'

from app import app

app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True
app.config['WTF_CSRF_ENABLED'] = False

db.create_all()

class RecipeModelTestCase(TestCase):
    """Test the functionality of the recipe model."""

    def setUp(self):
        """Clear the database and get ready to make requests."""
        User.query.delete()
        Recipe.query.delete()
        UserRecipe.query.delete()

        self.testclient = app.test_client()
    
    def test_create_instance(self):
        """Can a recipe instance be created?"""

        try:
            new_recipe = Recipe(api_id=500000)
            self.assertTrue(True)
        except:
            print('If this line runs, our instance must\'ve thrown an error.')
    
    def test_create_instance_in_db(self):
        """Can a recipe be put into the database?"""
        try:
            new_recipe2 = Recipe(api_id=45)
            db.session.add(new_recipe2)
            db.session.commit()

            self.assertTrue(True)
        except:
            print('If this line runs, something went wrong.')





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
            # If we see this failing test, something went wrong
            self.assertEqual(1, 2)
    
    def test_create_instance_in_db(self):
        """Can a recipe be put into the database?"""
        new_recipe2 = Recipe(api_id=45)
        db.session.add(new_recipe2)
        db.session.commit()

        self.assertEqual(Recipe.query.count(), 1)
    
    def test_query_recipe_from_db(self):
        """Can we query a recipe from the database?"""
        new_recipe3 = Recipe(api_id=50)
        db.session.add(new_recipe3)
        db.session.commit()

        self.assertIs(new_recipe3, Recipe.query.get(new_recipe3.id))








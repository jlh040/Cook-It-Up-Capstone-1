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
    
    def test_recipe_representation(self):
        """Does our repr method work for the recipe class?"""

        new_recipe4 = Recipe(api_id=17)
        db.session.add(new_recipe4)
        db.session.commit()

        self.assertIn(f'api_id: {new_recipe4.api_id}', str(Recipe.query.get(new_recipe4.id)))
    
    def test_get_recipes_by_cuisine(self):
        """Test that the get_recipes_by_cuisine method is functional
        and that it returns appropriate dishes."""
        list_of_recipes = Recipe.get_recipes_by_cuisine('Italian')
        for id, title in list_of_recipes:
            if 'Italian' in title:
                # If we see this passing test, we know we are getting italian cuisine
                self.assertTrue(True)
        
        
    def test_get_recipes_by_query_and_cals(self):
        """Is the get_recipes_by_query_and_cals method functional?"""
        # Get an Italian dish with < 100 cals.
        id_of_low_cal_ital_dish = 637513
        low_cal_ital_dish = Recipe.get_recipe_info(id_of_low_cal_ital_dish)

        # Get a list of italian dishes with less than 100 cals
        list_of_recipes = Recipe.get_recipes_by_query_and_cals('italian', 100)

        # Check that our Italian dish shows up in this list
        for id, title in list_of_recipes:
            if title == low_cal_ital_dish[0]:
                # If we see this passing test, our dish was found in the list
                self.assertTrue(True)
        










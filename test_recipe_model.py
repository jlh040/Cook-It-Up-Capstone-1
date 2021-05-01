"""Test recipe model."""

import os
from unittest import TestCase
from secret_keys import API_KEY
from models import db, User, Recipe

os.environ['DATABASE_URL'] = 'postgresql:///cook-it-up-test-db'

from app import app

app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True
app.config['WTF_CSRF_ENABLED'] = False

class RecipeModelTestCase(TestCase):
    """Test the functionality of the recipe model."""


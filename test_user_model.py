"""User model tests."""

import os
from unittest import TestCase
from models import db, User, Recipe
from secret_keys import API_KEY

os.environ['DATABASE_URL'] = 'cook-it-up-test-db'

from app import app

app.config['TESTING'] = True
app.config['WTF_CSRF_ENABLED'] = False


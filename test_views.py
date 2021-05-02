"""Test view functions / routes."""

from unittest import TestCase
from models import db, User, Recipe
from secret_keys import API_KEY
import os

os.environ['DATABASE_URL'] = 'postgresql:///cook-it-up-test-db'

from app import app

app.config['TESTING'] = True
app.config['WTF_CSRF_ENABLED'] = False
app.config['SQLALCHEMY_ECHO'] = True

db.create_all()

class ViewsTestCase(TestCase):
    """Test that view functions are working properly."""

    def setUp(self):
        """Make a test user and set up the test client."""
        User.query.delete()
        Recipe.query.delete()

        self.test_user = User.signup(
            username='some_guy87',
            password='redrobbin87231'
            first_name='Mark',
            last_name='Riano',
            email='flako@gmail.com'
        )
        db.session.commit()

        self.client = app.test_client()
    




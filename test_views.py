"""Test view functions / routes."""

from unittest import TestCase
from models import db, User, Recipe
from secret_keys import API_KEY
import os

os.environ['DATABASE_URL'] = 'postgresql:///cook-it-up-test-db'

from app import app, CURR_USER_KEY

app.config['TESTING'] = True
app.config['WTF_CSRF_ENABLED'] = False
app.config['SQLALCHEMY_ECHO'] = False

db.create_all()

class ViewsTestCase(TestCase):
    """Test that view functions are working properly."""

    def setUp(self):
        """Make a test user and set up the test client."""
        User.query.delete()
        Recipe.query.delete()

        self.test_user = User.signup(
            username='some_guy87',
            password='redrobbin87231',
            first_name='Mark',
            last_name='Riano',
            email='flako@gmail.com'
        )
        db.session.add(self.test_user)
        db.session.commit()

        self.client = app.test_client()
    
    def test_homepage_logged_in(self):
        """Do we see the logged-in homepage, when logged in?"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.test_user.id

            resp = c.get('/')
            html = resp.get_data(as_text=True)

            self.assertIn('<h1>LOGGED-IN HOMEPAGE</h1>', html)







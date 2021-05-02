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

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>LOGGED-IN HOMEPAGE</h1>', html)
    
    def test_homepage_logged_out(self):
        """Do we see the anonymous homepage, when logged out?"""
        with self.client as c:
            resp = c.get('/')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>ANONYMOUS HOMEPAGE</h1>', html)
    
    def test_see_cuisines_logged_in(self):
        """Can we search for a list of cuisines, when logged in?"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.test_user.id

        resp = c.get('/cuisines/nordic')
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('Knekkebrød', html)
    
    def test_not_see_cuisines_logged_out(self):
        """Are we not allowed to view foods of a certain
        cuisine type when logged out?
        """
        with self.client as c:
            resp = c.get('/cuisines/Nordic')
            self.assertEqual(resp.status_code, 302)

            resp = c.get('/cuisines/Nordic', follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertIn('Log in or make an account to view this', html)
    
    def test_search_recipes_logged_in(self):
        """Can we search for recipes when logged in?"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.test_user.id
            
            resp = c.post('/recipes', data={'recipe_name': 'brownie', 'num_of_cals': 199})
            html = resp.get_data(as_text=True)

            self.assertIn('Brownie', html)
    
    def test_cant_search_recipes_logged_out(self):
        """Are we restricted from searching for recipes when logged out?"""
        with self.client as c:
            resp = c.post('/recipes', data={'recipe_name': 'chicken', 'num_of_cals': 399})
            self.assertEqual(resp.status_code, 302)

            resp = c.post('/recipes', data={'recipe_name': 'chicken', 'num_of_cals': 399}, follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertIn('Unauthorized to view this', html)     

    def test_see_recipe_page_logged_in(self):
        """Can we see a recipe's page when logged in?"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.test_user.id
            
            resp = c.get('/recipes/663822')
            html = resp.get_data(as_text=True)

            self.assertIn('Trinidad Callaloo Soup', html)







    






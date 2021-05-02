from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import InputRequired, Optional, Email
from helper_funcs import calorie_choices

calorie_choices = [
        (99, 'Less than 100'),
        (199, 'Less than 200'),
        (299, 'Less than 300'),
        (399, 'Less than 400'),
        (499, 'Less than 500'),
        (599, 'Less than 600'),
        (699, 'Less than 700'),
        (799, 'Less than 800'),
        (899, 'Less than 900'),
        (999, 'Less than 1000')
    ]

class SignupForm(FlaskForm):
    """Represents a form to sign up"""

    username = StringField('Username:', 
                            validators=[InputRequired()])

    password = PasswordField('Password:', 
                            validators=[InputRequired()])

    first_name = StringField('First Name:', 
                            validators=[InputRequired()])

    last_name = StringField('Last Name:', 
                            validators=[Optional()])

    image_url = StringField('Image URL', 
                            validators=[Optional()])
                            
    email = StringField('Email:', 
                            validators=[Email()])

class LoginForm(FlaskForm):
    """Represents a form to log in."""

    username = StringField('Username:', 
                            validators=[InputRequired()])
    
    password = PasswordField('Password:',
                            validators=[InputRequired()])

class EditUserForm(FlaskForm):
    """Represents a form to edit a user."""

    username = StringField('Username:',
                            validators=[InputRequired()])
    
    first_name = StringField('First Name',
                            validators=[InputRequired()])

    last_name = StringField('Last Name',
                            validators=[Optional()])
    
    image_url = StringField('Image URL',
                            validators=[Optional()])

class SearchForm(FlaskForm):
    """Represents a form to search for recipes."""
    recipe_name = StringField('Search Term', validators=[InputRequired()])
    num_of_cals = SelectField('Number of Calories', choices=calorie_choices, coerce=int, default=599)
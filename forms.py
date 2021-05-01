from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Optional, Email

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
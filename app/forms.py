''' Forms for when User has to enter details '''

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, EqualTo
from app.constants import *

class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[InputRequired()])
	password = PasswordField('Password', validators=[InputRequired()])
	confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
	submit = SubmitField('Register')

class LoginForm(FlaskForm):
	username = StringField('Username', validators=[InputRequired()])
	password = PasswordField('Password', validators = [InputRequired()])

''' Forms for when User has to enter details '''

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import InputRequired, EqualTo, Length, Regexp
from app.constants import *

class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[InputRequired(), Length(min=4, max=30)])
	password = PasswordField('Password', validators=[InputRequired(), Length(min=6)])
	confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
	submit = SubmitField('Register')

class LoginForm(FlaskForm):
	username = StringField('Username', validators=[InputRequired(), Length(min=4, max=30)])
	password = PasswordField('Password', validators = [InputRequired()])

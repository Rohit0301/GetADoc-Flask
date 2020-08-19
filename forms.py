from flask_wtf import FlaskForm
from wtforms import Form,validators,StringField,PasswordField,BooleanField,SubmitField
#from wtforms.validators import ValidationError,DataRequired,Email,EqualTo


class RegistrationForm(FlaskForm):
	username=StringField('Username',[validators.DataRequired()])
	email=StringField('Email',[validators.DataRequired(),validators.Email()])
	password=PasswordField('Password',[validators.DataRequired()])
	confirmpassword=PasswordField('Confirm Password',[validators.DataRequired(),validators.EqualTo('password')])
	submit=SubmitField('Sign Up')
    

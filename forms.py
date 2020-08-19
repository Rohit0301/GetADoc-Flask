from flask_wtf import FlaskForm
from wtforms import Form,validators,StringField,PasswordField,BooleanField,SubmitField


class RegistrationForm(FlaskForm):
	username=StringField('Username',[validators.DataRequired(),validators.Length(min=3,max=50)])
	email=StringField('Email',[validators.DataRequired(),validators.Email()])
	password=PasswordField('Password',[validators.DataRequired(),validators.Length(min=8,max=30)])
	confirmpassword=PasswordField('Confirm Password',[validators.DataRequired(),validators.EqualTo('password')])
	submit=SubmitField('Sign Up')
    

class LoginForm(FlaskForm):
    email=StringField('Email',[validators.DataRequired(),validators.Email()])
    password=PasswordField('Password',[validators.DataRequired()])
    remember_me=BooleanField('Remember me')
    submit=SubmitField('Sign In')

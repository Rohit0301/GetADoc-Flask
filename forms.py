from flask_wtf import FlaskForm
from wtforms import Form,validators,StringField,PasswordField,BooleanField,SubmitField,SelectField,IntegerField,TextAreaField,RadioField
from wtforms.widgets import TextArea
from wtforms.fields.html5 import DateField,TimeField,DateTimeLocalField

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
    choice=RadioField('Choose type',choices=[('Doctor','Doctor'),('Patient','Patient')])
    submit=SubmitField('Sign In')


class DoctorForm(FlaskForm):
    fullname=StringField('FullName',[validators.DataRequired()])
    email=StringField('Email',[validators.DataRequired(),validators.Email()])
    password=PasswordField('Password',[validators.DataRequired(),validators.Length(min=8,max=30)])
    confirmpassword=PasswordField('Confirm Password',[validators.DataRequired(),validators.EqualTo('password')])
    city=StringField('City',[validators.DataRequired()])
    qualifications=StringField('Qualifications',[validators.DataRequired()],render_kw={"placeholder": "ex: MBBS,BHMS,BUMS"})
    contact=StringField('Contact',[validators.DataRequired()])
    myChoices = [('Select doctor Type','Select Doctor Type'),('Allergist','Allergist'),('Cardiologist','Cardiologist'),('Audiologist','Audiologist'),('Dentist','Dentist'),('Endocrinologist','Endocrinologist'),('Epidemiologist','Epidemiologist'),('Anesthesiologist','Anesthesiologist'),('Medical Geneticist','Medical Geneticist'),('Gynaecologist','Gynaecologist'),
     ('Physiologist','Physiologist'),('Neurosurgeon','Neurosurgeon'),('Neurologist','Neurologist')]
    doctortype = SelectField(u'Doctor type', choices = myChoices,default=1)
    address = StringField('Address',[validators.Length(min=4)],widget=TextArea())
    home_visit=BooleanField('Home visit available')
    home_charges=IntegerField('Home charges',render_kw={"placeholder": 0})
    clinic_charges=IntegerField('Clinic charges',render_kw={"placeholder": 0})
    submit=SubmitField('Submit Details')

class SearchForm(FlaskForm):
	city=StringField('City',[validators.DataRequired()])
	search=SubmitField('Search Doctor')


class PatientForm(FlaskForm):
    fullname=StringField("Patient's FullName",[validators.DataRequired()])
    contact=StringField("Patient's Contact",[validators.DataRequired()])
    address = StringField("Patient's Address",[validators.Length(min=4)],widget=TextArea())
    age=IntegerField("Patients's Age",[validators.DataRequired()])
    myChoices=[('Year','Year'),('Month','Month')]
    type= SelectField(u'Type', choices = myChoices,default=1)
    choice=RadioField('Choose preference',choices=[('Home Visit','Home Visit'),('Clinic','Clinic')])
    submit=SubmitField('Submit Details')


class Appointments(FlaskForm):
    date=DateField('Allot Date',[validators.DataRequired()], format='%d-%m-%Y')
    #fullname=StringField('FullName',[validators.DataRequired()])
    time = TimeField('Allot Time',[validators.DataRequired()],format='%H:%M:%S')
    submit=SubmitField('Confirm')
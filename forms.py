from flask_wtf import FlaskForm
from wtforms import Form,validators,StringField,PasswordField,BooleanField,SubmitField,SelectField,IntegerField,TextAreaField,RadioField
from wtforms.widgets import TextArea
from wtforms.fields.html5 import DateField,TimeField,DateTimeLocalField

class RegistrationForm(FlaskForm):
	username=StringField('Username',[validators.DataRequired(),validators.Length(min=3,max=50)],render_kw={"placeholder": "Fullname"})
	email=StringField('Email',[validators.DataRequired(),validators.Email()],render_kw={"placeholder": "Email"})
	password=PasswordField('Password',[validators.DataRequired(),validators.Length(min=8,max=30)],render_kw={"placeholder": "Password"})
	confirmpassword=PasswordField('Confirm Password',[validators.DataRequired(),validators.EqualTo('password','Password must be equal')],render_kw={"placeholder": "Confirm Password"})
	submit=SubmitField('Sign Up')

    

class LoginForm(FlaskForm):
    email=StringField('Email',[validators.DataRequired(),validators.Email()],render_kw={"placeholder": "Email"})
    password=PasswordField('Password',[validators.DataRequired()],render_kw={"placeholder": "Password"})
    remember_me=BooleanField('Remember me')
    choice=RadioField('Choose type',[validators.DataRequired('Please select any one option')],choices=[('Doctor','Doctor'),('Patient','Patient')])
    submit=SubmitField('Sign In')


class DoctorForm(FlaskForm):
    fullname=StringField('FullName',[validators.DataRequired()],render_kw={"placeholder": "Fullname"})
    email=StringField('Email',[validators.DataRequired(),validators.Email()],render_kw={"placeholder": "Email"})
    password=PasswordField('Password',[validators.DataRequired(),validators.Length(min=8,max=30)],render_kw={"placeholder": "Password"})
    confirmpassword=PasswordField('Confirm Password',[validators.DataRequired(),validators.EqualTo('password','Password must be equal')],render_kw={"placeholder": "Confirm Password"})
    city=StringField('City',[validators.DataRequired()],render_kw={"placeholder": "City"})
    qualifications=StringField('Qualifications',[validators.DataRequired()],render_kw={"placeholder": "Qualifications ex: MBBS,BHMS"})
    contact=StringField('Contact',[validators.DataRequired()],render_kw={"placeholder": "Contact"})
    myChoices = [('Select Specialisation','Select Specialisation'),('Allergist','Allergist'),('Cardiologist','Cardiologist'),('Audiologist','Audiologist'),('Dentist','Dentist'),('Endocrinologist','Endocrinologist'),('Epidemiologist','Epidemiologist'),('Anesthesiologist','Anesthesiologist'),('Medical Geneticist','Medical Geneticist'),('Gynaecologist','Gynaecologist'),
     ('Physiologist','Physiologist'),('Neurosurgeon','Neurosurgeon'),('Neurologist','Neurologist')]
    doctortype = SelectField(u'Doctor type', choices = myChoices,default=1)
    address = StringField('Address',[validators.Length(min=4)],widget=TextArea(),render_kw={"placeholder": "Addess"})
    home_visit=BooleanField('Home visit available')
    other=BooleanField('Other')
    specialisation=StringField('Enter your Specialisation',render_kw={"placeholder": "Specialisation"})
    home_charges=StringField('Home charges',render_kw={"placeholder": "Home visit charge"})
    clinic_charges=StringField('Clinic charges',render_kw={"placeholder": "Clinic charge"})

    submit=SubmitField('Submit Details')

class SearchForm(FlaskForm):
	city=StringField('City',[validators.DataRequired()],render_kw={"placeholder": "Enter Your City"})
	search=SubmitField('Search Doctor')


class PatientForm(FlaskForm):
    fullname=StringField("Patient's FullName",[validators.DataRequired()],render_kw={"placeholder": " Patient's FullName"})
    contact=StringField("Patient's Contact",[validators.DataRequired()],render_kw={"placeholder": "Patient's Phone No"})
    address = StringField("Patient's Address",[validators.Length(min=4)],widget=TextArea(),render_kw={"placeholder": "Patient's Address"})
    age=IntegerField("Patients's Age",[validators.DataRequired(),validators.Length(min=1)],render_kw={"placeholder": "Patient's Age"})
    myChoices=[('Year','Year'),('Month','Month')]
    type= SelectField(u'Type', choices = myChoices,default=1)
    choice=RadioField('Choose preference',choices=[('Home Visit','Home Visit'),('Clinic','Clinic')])
    gender=RadioField('Gender',choices=[('Male','Male'),('Female','Female')])
    submit=SubmitField('Submit Details')


class Appointments(FlaskForm):
    date=DateField('Allot Date',[validators.DataRequired()], format='%d-%m-%Y')
    #fullname=StringField('FullName',[validators.DataRequired()])
    time = TimeField('Allot Time',[validators.DataRequired()],format='%H:%M:%S')
    submit=SubmitField('Confirm')

class Reason(FlaskForm):
    reason=RadioField('Reasons',[validators.DataRequired('please select any one reason')],choices=[('Busy','Busy'),('Out of station','Out of station'),('All slots are booked','All slots are booked'),('Other','Other')])
    submit=SubmitField('Submit')
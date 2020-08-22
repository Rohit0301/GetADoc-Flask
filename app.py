from flask import Flask, render_template, url_for,request,flash,redirect,session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash    #this class is used for generate and check the hashcode
from forms import RegistrationForm,LoginForm,DoctorForm,SearchForm,PatientForm,Appointments
from flask_login import LoginManager,UserMixin,current_user,login_user,logout_user,login_required  #manages the user logged-in state
#usermixin includes generic implementations that are appropriate for most user model classes like is_authenticated,is_active
from datetime import datetime
import smtplib

import socket
socket.getaddrinfo('localhost', 80)





app = Flask(__name__)
app.config['SECRET_KEY']='1299ed71343a314003fb6cc2df93fb2d'
#protect from modifing cookies and cross site requests
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost/GetADoc'

db=SQLAlchemy(app)
login_manager=LoginManager()

login_manager.init_app(app)

login_manager.login_view = 'login'
s = smtplib.SMTP('smtp.gmail.com', 587) 
s.starttls() 



class Register(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80),nullable=False,)
    email = db.Column(db.String(80),nullable=False)
    password = db.Column(db.String(500),nullable=False)
    def check_password(self, password):
        return check_password_hash(self.password, password)

class DoctorDetails(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(80),nullable=False)
    email = db.Column(db.String(80),nullable=False)
    password = db.Column(db.String(500),nullable=False)
    city = db.Column(db.String(80),nullable=False)
    qualifications = db.Column(db.String(100),nullable=False)
    contact = db.Column(db.String(80),nullable=False)
    doctortype = db.Column(db.String(80),nullable=False)
    address = db.Column(db.String(200),nullable=False)
    clinic_charge = db.Column(db.Integer,nullable=False)
    home_visit_available = db.Column(db.Integer,nullable=False,default=0)
    home_charge = db.Column(db.String(80),nullable=False)
    def check_password(self, password):
        return check_password_hash(self.password, password)


class PatientDetails(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(80),nullable=False)
    contact = db.Column(db.String(80),nullable=False)
    address = db.Column(db.String(200),nullable=False)
    age=db.Column(db.Integer,nullable=False)
    type= db.Column(db.String(80),nullable=False)
    choice= db.Column(db.String(80),nullable=False)
    formfillingdate=db.Column(db.DateTime, nullable=False)
    appointmentdate=db.Column(db.Date)
    appointmenttime=db.Column(db.Time,nullable=True)
    docid=db.Column(db.Integer,nullable=False)
    pid=db.Column(db.Integer,nullable=False)
    status=db.Column(db.String(20),nullable=False)







    

@login_manager.user_loader        #Flask-Login retrieves the ID of the user from the session, and then loads that user into memory. 
def load_user(id):
    return Register.query.get(int(id))

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')



@app.route('/register', methods=['GET', 'POST'])
def register():
    form=RegistrationForm()
    if form.validate_on_submit():
        reg = Register.query.filter_by(email=form.email.data).first()          
        if reg is not None:                             #this if checks that the user is already registered or not
            flash('user already registered!')
        else:                                           
            password=generate_password_hash(form.password.data)      #this will produce a hashcode for any password for privacy
            register = Register(username=form.username.data, email=form.email.data,password=password)
            db.session.add(register)
            db.session.commit()
            reg = Register.query.filter_by(email=form.email.data).first()
            flash('Congratulations, you are registered successfully!')
            return redirect(url_for('searchdoctor',pid=reg.id))
            

    return render_template('register.html',form=form)


@app.route('/login',methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        type=form.choice.data
        if type=="Doctor":
            user = DoctorDetails.query.filter_by(email=form.email.data).first()
        else:
            user = Register.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        if type=="Patient":
            return redirect(url_for('searchdoctor',pid= user.id))
        else:
            return redirect(url_for('doctorpage',id=user.id))

    
    return render_template('login.html',form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/doctorpage/<int:id>')
def doctorpage(id):
    form=Appointments()
    appoints=PatientDetails.query.filter_by(docid=id,status="pending").all()
    if appoints is None:
        flash("No pending appointments are there")
        return redirect('doctorpage',id=id)
    return render_template('doctorpage.html',appoints=appoints,form=form)




##########################################################################################################################
@app.route('/confirmappointment/<int:id>/<int:pid>',methods=['GET','POST'])
def confirmappointment(id,pid):
    form=Appointments()
    appoints=PatientDetails.query.filter_by(docid=id,status="pending",pid=pid).first()
    date="hello"
    time="hi"
    if form.validate_on_submit:
            date=form.date.data
       # date = datetime.strptime(form.date.data, '%d, %m, %Y')
            flash(date)
            return redirect(url_for('home'))
        #return redirect(url_for('doctorpage',id=id))

        #patient=PatientDetails.query.filter_by(docid=id,status="pending",pid=pid).update({status:"appointed"})
       # return redirect(url_for('home'))
    return render_template('confirmappointment.html',appoints=appoints,form=form,date=date)
####################################################################################################################


@app.route('/choice')
def choice():
    return render_template('choice.html')


@app.route('/searchdoctor/<int:pid>',methods=['GET','POST'])
def searchdoctor(pid):
    form=SearchForm()
    doctor = DoctorDetails.query.filter_by(city=form.city.data).all()
    if doctor is None:
        flash('No doctor present in this city')
    return render_template('searchdoctor.html',doctor=doctor,form=form,pid=pid)


@app.route('/doctorform',methods=['GET','POST'])
def doctorform():
    form=DoctorForm()
    if form.validate_on_submit():
        home_visit_available=0
        if form.home_visit.data:
            home_visit_available=1
        reg = Register.query.filter_by(email=form.email.data).first()          
        if reg is not None:                             #this if checks that the user is already registered or not
            flash('user already registered!')
        else:                                           
            password=generate_password_hash(form.password.data)   
            doctor=DoctorDetails(fullname=form.fullname.data,email=form.email.data,password=password,city=form.city.data,qualifications=form.qualifications.data,contact=form.contact.data,doctortype=form.doctortype.data,address=form.address.data,clinic_charge=form.clinic_charges.data,home_visit_available=home_visit_available,home_charge=form.home_charges.data)
            db.session.add(doctor)
            db.session.commit()
        flash('Congratulations, your data submitted successfully!')
        return redirect(url_for('doctorpage',id=reg.id))
    return render_template('doctor.html',form=form)




@app.route('/patientform/<int:id>/<int:visit>/<int:pid>',methods=['GET','POST'])
def patientform(id,visit,pid):
    form=PatientForm()
    if form.validate_on_submit():
        home=form.choice.data
        if visit==0 and home=="Home Visit":
            flash('Sorry !! Doctor is not available for home visit please choose clinic option')
            return redirect(url_for('patientform',id=id,visit=visit,pid=pid))

        appoint = PatientDetails.query.filter_by(docid=id).all()
        for a in appoint:
            if a.pid==pid and a.status=="pending":
                 flash('you have already book an appointment with this doctor')     
                 return redirect(url_for('searchdoctor',pid=pid))      
        

        patient=PatientDetails(fullname=form.fullname.data,contact=form.contact.data,address=form.address.data,age=form.age.data,type=form.type.data,choice=form.choice.data,formfillingdate=datetime.now(),appointmentdate=0,appointmenttime=0,docid=id,pid=pid,status="pending")
        db.session.add(patient)
        db.session.commit()
        return redirect(url_for('home'))# add check histroy form for a patients
        #s.login("arichayjian@gmail.com", "aj03012002aj") 
  
# message to be sent 
       # message = "hello there hi i am arichay jain"
  
# sending the mail 
       # s.sendmail("arichayjian@gmail.com", "rj03012002@gmail.com", message) 
  
# terminating the session 
       # s.quit() 


    return render_template('patientform.html',form=form,visit=visit)


if __name__ == '__main__':
    app.run()

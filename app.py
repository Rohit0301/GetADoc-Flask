from flask import Flask, render_template, url_for,request,flash,redirect,session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash    #this class is used for generate and check the hashcode
from forms import RegistrationForm,LoginForm,DoctorForm,SearchForm,PatientForm,Appointments,Reason
from flask_login import LoginManager,UserMixin,current_user,login_user,logout_user,login_required  #manages the user logged-in state
#usermixin includes generic implementations that are appropriate for most user model classes like is_authenticated,is_active
from datetime import datetime,date

import json
with open('config.json','r') as c:
    params=json.load(c)["params"]




app = Flask(__name__)
app.config['SECRET_KEY']=params["key"]
app.config["MYSQL_HOST"]="127.0.0.1"
app.config["MYSQL_USER"]="root"
#protect from modifing cookies and cross site requests
app.config['SQLALCHEMY_DATABASE_URI']=params["local_uri"]

db=SQLAlchemy(app)
login_manager=LoginManager()

login_manager.init_app(app)

login_manager.login_view = 'login'

 


# table which store patients login details
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
    clinic_charge = db.Column(db.String(200),nullable=False)
    home_visit_available = db.Column(db.Integer,nullable=False,default=0)
    home_charge = db.Column(db.String(200),nullable=False)
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
    reason=db.Column(db.String(50),nullable=True)
    gender = db.Column(db.String(10),nullable=False)






    

@login_manager.user_loader        #Flask-Login retrieves the ID of the user from the session, and then loads that user into memory. 
def load_user(id):
    if int(id)%2==0:
        return DoctorDetails.query.get(int(id))
    else:
         return Register.query.get(int(id))

#home page route
@app.route("/", defaults={'id':0})
@app.route('//<int:id>')
def home(id):
    return render_template('home.html',id=id,params=params)

#about page route
@app.route('/about/<int:id>')
def about(id):
    return render_template('about.html',id=id,params=params)



# patients all appointment history is being seen from this route 
@app.route('/patienthistory/<int:pid>')
def patienthistory(pid):
    patient=PatientDetails.query.filter_by(pid=pid).all()
    lis=[]
    for p in patient:
        d=DoctorDetails.query.filter_by(id=p.docid).first()
        if d is not None:
            lis.append({"docid":d.id,"docname":d.fullname,"contact":d.contact,"address":d.address,"status":p.status,"appointmentdate":p.appointmentdate,"appointmenttime":str(p.appointmenttime)})
    lis.reverse()    

    
    return render_template('patienthistory.html',patient=patient,lis=lis,pid=pid,l=len(lis))







# patiendts sign up route
@app.route('/register/<int:id>', methods=['GET', 'POST'])
def register(id):
    form=RegistrationForm()
    if form.validate_on_submit():
        reg = Register.query.filter_by(email=form.email.data).first()          
        if reg is not None:                             #this if checks that the user is already registered or not
            flash('user already registered!')
        else:                                           
            password=generate_password_hash(form.password.data)      #this will produce a hashcode for any password for privacy
            id1 = db.session.query(db.func.max(Register.id)).scalar()
            if id1==None:
                id1=-1
            register = Register(id=id1+2,username=form.username.data, email=form.email.data,password=password)
            db.session.add(register)
            db.session.commit()
            reg = Register.query.filter_by(email=form.email.data).first()
            flash('Congratulations, you are registered successfully!')
            return redirect(url_for('home',id=reg.id))
            

    return render_template('register.html',form=form,id=id)


#login route for both atient and doctor
@app.route('/login/<int:id>',methods=['GET', 'POST'])
def login(id):
    form = LoginForm()

    if form.validate_on_submit():
        type=form.choice.data
        if type=="Doctor":
            user = DoctorDetails.query.filter_by(email=form.email.data).first()
        else:
            user = Register.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login',id=id))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('home',id=user.id))

    
    return render_template('login.html',form=form,id=id)

#logout route
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


#this is a route for giving the reason why doctor cancelled his/ her appointment
@app.route('/reason/<int:id>/<int:pid>',methods=['GET','POST'])
def reason(id,pid):
    form=Reason()
    patient=PatientDetails.query.filter_by(docid=id,status="pending",pid=pid).first()
    re=request.form.get('reason')
    if form.validate_on_submit():
           patient.status="cancelled"
           patient.reason=re
           db.session.commit()
           flash('Appointment cancelled')
           return redirect(url_for('doctorpage',id=id))
            
    return render_template('reason.html',form=form,id=id)

#this is a route whrere doctor can see all the pending,confirmed and cancelled appointment.
@app.route('/doctorpage/<int:id>')
def doctorpage(id):
    form=Appointments()
    appoints=PatientDetails.query.filter_by(docid=id).all()
    s=len(appoints)    
    return render_template('doctorpage.html',appoints=appoints,form=form,s=s,id=id)


#this route is for alotting paricular slot(date and time) to patients.
@app.route('/confirmappointment/<int:id>/<int:pid>',methods=['GET','POST'])
def confirmappointment(id,pid):
    form=Appointments()
    appoints=PatientDetails.query.filter_by(docid=id,status="pending",pid=pid).first()
    if request.method=="POST":
            date1=request.form.get('date')
            time=request.form.get('time')
            patient=PatientDetails.query.filter_by(docid=id,status="pending",pid=pid).first()
            patient.status="appointed"
            patient.appointmenttime=time
            patient.appointmentdate=date1
            db.session.commit()
           
            return redirect(url_for('doctorpage',id=id))

    return render_template('confirmappointment.html',appoints=appoints,form=form,id=id)

#this route is for choosing the type bw doctoc and patient before registering
@app.route('/choice/<int:id>')
def choice(id):
    return render_template('choice.html',id=id)

#patient will search doctor form this route 
@app.route('/searchdoctor/<int:pid>',methods=['GET','POST'])
def searchdoctor(pid):
    form=SearchForm()
    doctor=None
    i=-1
    if form.validate_on_submit():
          doctor = DoctorDetails.query.filter_by(city=form.city.data).all()
          i=len(doctor) 
    return render_template('searchdoctor.html',doctor=doctor,form=form,pid=pid,i=i)

#this route is sign up page for doctor
@app.route('/doctorform/<int:id>',methods=['GET','POST'])
def doctorform(id):
    form=DoctorForm()
    fl=0
      
    if form.validate_on_submit():
        home_visit_available=0
        specialisation=""
        if request.form.get('Other'):
            if form.doctortype.data=="Select Specialisation":
                flash('Please Enter your Specialisation')
                return redirect(url_for('doctorform',id=id))
            else:
               specialisation=form.doctortype.data
        else:
            if form.specialisation.data==None:
                flash('Please select any Specialisation')
                return redirect(url_for('doctorform',id=id))
            else:
               specialisation=form.specialisation.data


        if form.home_visit.data==True:
            home_visit_available=1
        
        
        reg = DoctorDetails.query.filter_by(email=form.email.data).first()          
        if reg is not None:                             #this if checks that the user is already registered or 
            flash('user already registered!')
            return redirect(url_for('doctorform',id=id))
        else:                                           
            password=generate_password_hash(form.password.data)
            id1 = db.session.query(db.func.max(DoctorDetails.id)).scalar()
            if id1==None:
                id1=0   
            doctor=DoctorDetails(id=id1+2,fullname=form.fullname.data,email=form.email.data,password=password,city=form.city.data,qualifications=form.qualifications.data,contact=form.contact.data,doctortype=specialisation,address=form.address.data,clinic_charge=form.clinic_charges.data,home_visit_available=home_visit_available,home_charge=form.home_charges.data)
            db.session.add(doctor)
            db.session.commit()
        doc = DoctorDetails.query.filter_by(email=form.email.data).first()
        flash('Congratulations, your data submitted successfully!')
        return redirect(url_for('home',id=doc.id))
    return render_template('doctor.html',form=form,id=id,fl=fl)



#this is a patient form route. Patient have to fill the form before takin an apointment
@app.route('/patientform/<int:id>/<int:pid>',methods=['GET','POST'])
def patientform(id,pid):
    form=PatientForm()
    reg = DoctorDetails.query.filter_by(id=id).first()
    fees=0
    visit=reg.home_visit_available          
    if request.method=="POST":
       
        appoint = PatientDetails.query.filter_by(docid=id).all()
        for a in appoint:
            if a.pid==pid and a.status=="pending":
                 flash('you appointment is already under process')    
                 return redirect(url_for('searchdoctor',pid=pid))
        
        patient=PatientDetails(fullname=form.fullname.data,contact=form.contact.data,address=form.address.data,age=form.age.data,type=form.type.data,choice=form.choice.data,formfillingdate=datetime.now(),appointmentdate=0,appointmenttime=0,docid=id,pid=pid,status="pending",reason="none",gender=form.gender.data)
        db.session.add(patient)
        db.session.commit()
        flash('you form is submitted successfully. Please check your notification for your appointment date and time!')
        return redirect(url_for('home',id=pid))
        


    return render_template('patientform.html',form=form,visit=visit,pid=pid)


if __name__ == '__main__':
    app.run()

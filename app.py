from flask import Flask, render_template, url_for,request,flash,redirect,session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash    #this class is used for generate and check the hashcode
from forms import RegistrationForm,LoginForm,DoctorForm,SearchForm,PatientForm,Appointments,Reason
from flask_login import LoginManager,UserMixin,current_user,login_user,logout_user,login_required  #manages the user logged-in state
#usermixin includes generic implementations that are appropriate for most user model classes like is_authenticated,is_active
from datetime import datetime,date
#from SQLAlchemy import ForeignKey
#from sqlalchemy.orm import relationship
import smtplib

import socket
socket.getaddrinfo('localhost', 8080)





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
    reason=db.Column(db.String(50),nullable=True)








    

@login_manager.user_loader        #Flask-Login retrieves the ID of the user from the session, and then loads that user into memory. 
def load_user(id):
    if int(id)%2==0:
        return DoctorDetails.query.get(int(id))
    else:
         return Register.query.get(int(id))

@app.route("/", defaults={'id':0})
@app.route('//<int:id>')
def home(id):
    return render_template('home.html',id=id)


@app.route('/about')
def about():
    return render_template('about.html')




@app.route('/patienthistory/<int:pid>')
def patienthistory(pid):
    patient=PatientDetails.query.filter_by(pid=pid).all()
    lis=[]
    for p in patient:
        d=DoctorDetails.query.filter_by(id=p.docid).first()
        if d is not None:
            lis.append({"doid":d.id,"docname":d.fullname,"contact":d.contact,"address":d.address,"status":p.status,"appointmentdate":p.appointmentdate,"appointmenttime":str(p.appointmenttime)})
    lis.reverse()    

    
    return render_template('patienthistory.html',patient=patient,lis=lis)








@app.route('/register', methods=['GET', 'POST'])
def register():
    form=RegistrationForm()
    if form.validate_on_submit():
        reg = Register.query.filter_by(email=form.email.data).first()          
        if reg is not None:                             #this if checks that the user is already registered or not
            flash('user already registered!')
        else:                                           
            password=generate_password_hash(form.password.data)      #this will produce a hashcode for any password for privacy
            id1 = db.session.query(db.func.max(Register.id)).scalar()
            register = Register(id=id1+2,username=form.username.data, email=form.email.data,password=password)
            db.session.add(register)
            db.session.commit()
            reg = Register.query.filter_by(email=form.email.data).first()
            flash('Congratulations, you are registered successfully!')
            return redirect(url_for('searchdoctor',pid=reg.id))
            

    return render_template('register.html',form=form)


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
        #if type=="Patient":
         #   return redirect(url_for('searchdoctor',pid= user.id))
        #else:
            
           # appoints=PatientDetails.query.filter_by(docid=user.id,status="pending").all()
            #if len(appoints)==0:
             #   flash('no pending appointments yet')
              #  return redirect(url_for('doctorpage',id=user.id))

            #else:
             #   no=len(appoints)
              #  flash('{} appointments are pending'.format(no))
               # return redirect(url_for('doctorpage',id=user.id))

    
    return render_template('login.html',form=form,id=id)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


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

@app.route('/doctorpage/<int:id>')
def doctorpage(id):
    form=Appointments()
    appoints=PatientDetails.query.filter_by(docid=id).all()
    s=len(appoints)    
    return render_template('doctorpage.html',appoints=appoints,form=form,s=s)




##########################################################################################################################
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
        #return redirect(url_for('doctorpage',id=id))

        #patient=PatientDetails.query.filter_by(docid=id,status="pending",pid=pid).update({status:"appointed"})
       # return redirect(url_for('home'))
    return render_template('confirmappointment.html',appoints=appoints,form=form)
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
    else:   
       return render_template('searchdoctor.html',doctor=doctor,form=form,pid=pid)


@app.route('/doctorform',methods=['GET','POST'])
def doctorform():
    form=DoctorForm()
    if form.validate_on_submit():
        home_visit_available=0
        specialisation=""
        if form.home_visit.data:
            home_visit_available=1
        if form.other.data:
               specialisation=form.specialisation.data
        else:
            specialisation=form.doctortype.data

        reg = DoctorDetails.query.filter_by(email=form.email.data).first()          
        if reg is not None:                             #this if checks that the user is already registered or not
            flash('user already registered!')
        else:                                           
            password=generate_password_hash(form.password.data)
            id1 = db.session.query(db.func.max(DoctorDetails.id)).scalar()   
            doctor=DoctorDetails(id=id1+2,fullname=form.fullname.data,email=form.email.data,password=password,city=form.city.data,qualifications=form.qualifications.data,contact=form.contact.data,doctortype=specialisation,address=form.address.data,clinic_charge=form.clinic_charges.data,home_visit_available=home_visit_available,home_charge=form.home_charges.data)
            db.session.add(doctor)
            db.session.commit()
        flash('Congratulations, your data submitted successfully!')
        return redirect(url_for('doctorpage',id=reg.id))
    return render_template('doctor.html',form=form)




@app.route('/patientform/<int:id>/<int:pid>',methods=['GET','POST'])
def patientform(id,pid):
    form=PatientForm()
    reg = DoctorDetails.query.filter_by(id=id).first()
    visit=reg.home_visit_available          
    if request.method=="POST":
        appoint = PatientDetails.query.filter_by(docid=id).all()
        for a in appoint:
            if a.pid==pid and a.status=="pending":
                 flash('you appointment is already under process')     
                 return redirect(url_for('searchdoctor',pid=pid))
        patient=PatientDetails(fullname=form.fullname.data,contact=form.contact.data,address=form.address.data,age=form.age.data,type=form.type.data,choice=form.choice.data,formfillingdate=datetime.now(),appointmentdate=0,appointmenttime=0,docid=id,pid=pid,status="pending",reason="none")
        db.session.add(patient)
        db.session.commit()
        flash('you form is submitted successfully. Please check your notification for your appointment date and time!')
        return redirect(url_for('home',id=pid))# add check histroy form for a patients
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

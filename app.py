from flask import Flask, render_template, url_for,request,flash,redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash    #this class is used for generate and check the hashcode
from forms import RegistrationForm,LoginForm
from flask_login import LoginManager,UserMixin,current_user,login_user,logout_user,login_required  #manages the user logged-in state
#usermixin includes generic implementations that are appropriate for most user model classes like is_authenticated,is_active





app = Flask(__name__)
app.config['SECRET_KEY']='1299ed71343a314003fb6cc2df93fb2d'
#protect from modifing cookies and cross site requests
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost/GetADoc'

db=SQLAlchemy(app)
login_manager=LoginManager()

login_manager.init_app(app)

login_manager.login_view = 'users.login'




class Register(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80),nullable=False,)
    email = db.Column(db.String(80),nullable=False)
    password = db.Column(db.String(500),nullable=False)
    def check_password(self, password):
        return check_password_hash(self.password, password)
    

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
            flash('Congratulations, you are registered successfully!')
            return redirect(url_for('home'))
    return render_template('register.html',form=form)


@app.route('/login',methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Register.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('home'))

    
    return render_template('login.html',form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run()

from flask import Flask, render_template, url_for,request,flash,redirect
from forms import RegistrationForm

app = Flask(__name__)
app.config['SECRET_KEY']='1299ed71343a314003fb6cc2df93fb2d'
#protect from modifing cookies and cross site requests

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
         flash('Congratulations, you are now a registered user!')
         return redirect(url_for('home'))
	return render_template('register.html',form=form)

if __name__ == '__main__':
    app.run()

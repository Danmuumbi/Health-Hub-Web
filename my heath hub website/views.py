""""from flask import Blueprint, render_template, url_for, flash, redirect
from flask_login import login_user, current_user, logout_user, login_required
#from Models.user import db, User
from Utilities.forms import RegistrationForm, LoginForm
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

register = Blueprint('register', __name__)
login = Blueprint('login', __name__)
home = Blueprint('home', __name__)

@register.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in', 'success')
        return redirect(url_for('login.login'))
    return render_template('register.html', title='Register', form=form)

@login.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@home.route("/")
@home.route("/home")
@login_required
def home():
    return render_template('index.html', title='Home')
""

# Views/views.py
from flask import render_template, redirect, url_for, request, flash, session
from . import views
from models import db, User, Appointment, MedicalRecord, Payment
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

@views.route('/')
def index():
    return render_template('index.html')

@views.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        date_of_birth = request.form.get('date_of_birth')
        gender = request.form.get('gender')
        address = request.form.get('address')
        phone_number = request.form.get('phone_number')

        hashed_password = generate_password_hash(password, method='sha256')

        user = User(
            username=username,
            email=email,
            password=hashed_password,
            date_of_birth=date_of_birth,
            gender=gender,
            address=address,
            phone_number=phone_number
        )
        db.session.add(user)
        db.session.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('views.login'))
    return render_template('register.html')

@views.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.user_id
            flash('Login successful!', 'success')
            return redirect(url_for('views.dashboard'))
        else:
            flash('Invalid email or password', 'danger')
    return render_template('login.html')

@views.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('views.login'))
    user = User.query.get(session['user_id'])
    return render_template('dashboard.html', user=user)

@views.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('views.index'))
"""

from flask import render_template, Blueprint
from flask_login import current_user, login_required

views = Blueprint('views', __name__)

@views.route('/')
def index():
    return render_template('index.html')

@views.route('/dashboard')
@login_required
def dashboard():
    user = current_user
    return render_template('dashboard.html', user=user)

# Add more routes if necessary

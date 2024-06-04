from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required
from flask_migrate import Migrate
from config import Config
from models import db, User, MedicalRecord, Appointment, Department, Payment
from forms import RegistrationForm, LoginForm, MedicalRecordForm, AppointmentForm, PaymentForm
import logging
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
migrate = Migrate(app, db)

logging.basicConfig(level=logging.DEBUG)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    date_of_birth = DateField('Date of Birth', format='%Y-%m-%d', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')])
    address = StringField('Address')
    phone_number = StringField('Phone Number')
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        logging.debug("Form validation successful.")
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password,
                    date_of_birth=form.date_of_birth.data, gender=form.gender.data,
                    address=form.address.data, phone_number=form.phone_number.data)

        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            logging.debug("Email already exists.")
            flash('Email already exists. Please use a different email address.', 'danger')
            return render_template('register.html', title='Register', form=form)

        try:
            db.session.add(user)
            db.session.commit()
            flash('Your account has been created!', 'success')
            login_user(user)
            return redirect(url_for('dashboard'))
        except IntegrityError as e:
            logging.error(f"Error occurred during user registration: {e}")
            db.session.rollback()
            flash('An error occurred during registration. Please try again.', 'danger')
    else:
        logging.debug("Form validation failed.")
        logging.debug(form.errors)
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        logging.debug("Login form validation successful.")
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    else:
        logging.debug("Login form validation failed.")
        logging.debug(form.errors)
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/dashboard")
@login_required
def dashboard():
    user_medical_records = MedicalRecord.query.filter_by(user_id=current_user.user_id).all()
    user_appointments = Appointment.query.filter_by(patient_id=current_user.user_id).all()
    user_payments = Payment.query.filter_by(user_id=current_user.user_id).all()

    return render_template('dashboard.html', user=current_user, 
                           medical_records=user_medical_records, 
                           appointments=user_appointments, 
                           payments=user_payments)

@app.route("/add_medical_record", methods=['GET', 'POST'])
@login_required
def add_medical_record():
    form = MedicalRecordForm()
    if form.validate_on_submit():
        new_record = MedicalRecord(
            user_id=current_user.user_id,
            medical_history=form.medical_history.data,
            medications=form.medications.data,
            vaccination_record=form.vaccination_record.data,
            lab_results=form.lab_results.data,
            allergies=form.allergies.data,
            immunizations=form.immunizations.data
        )
        db.session.add(new_record)
        db.session.commit()
        flash('Medical record added successfully', 'success')
        return redirect(url_for('dashboard'))
    return render_template('new_medical_record.html', form=form)

@app.route("/add_appointment", methods=['GET', 'POST'])
@login_required
def add_appointment():
    form = AppointmentForm()
    if form.validate_on_submit():
        new_appointment = Appointment(
            patient_id=current_user.user_id,
            doctor_id=1,  # Replace with actual doctor ID logic
            service_type=form.service_type.data,
            date_time=form.date_time.data,
            status=form.status.data
        )
        db.session.add(new_appointment)
        db.session.commit()
        flash('Appointment booked successfully', 'success')
        return redirect(url_for('dashboard'))
    return render_template('new_appointment.html', form=form)

@app.route("/add_payment", methods=['GET', 'POST'])
@login_required
def add_payment():
    form = PaymentForm()
    if form.validate_on_submit():
        new_payment = Payment(
            user_id=current_user.user_id,
            payment_info=form.payment_info.data
        )
        db.session.add(new_payment)
        db.session.commit()
        flash('Payment made successfully', 'success')
        return redirect(url_for('dashboard'))
    return render_template('new_payment.html', form=form)

@app.route("/about")
def about():
    return render_template('about.html', title='About Us')

@app.route("/services")
def services():
    return render_template('services.html', title='Our Services')

@app.route("/contact")
def contact():
    return render_template('contact.html', title='Contact Us')
@app.route('/news')
def news_page():
    # Your view function logic here
    return render_template('news.html')
@app.route('/update_info')
def update_info():
    # Your view function logic here
    return render_template('update_info.html')



if __name__ == '__main__':
    app.run(debug=True)

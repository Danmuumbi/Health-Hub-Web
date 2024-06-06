from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
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
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from flask_mail import Mail
from itsdangerous import URLSafeTimedSerializer

app = Flask(__name__)
app.config.from_object(Config)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'muumbidaniel0@gmail.com'
app.config['MAIL_PASSWORD'] = 'mmuuo2015'


db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
migrate = Migrate(app, db)

logging.basicConfig(level=logging.DEBUG)
mail = Mail(app)
s = URLSafeTimedSerializer(app.config['SECRET_KEY'])


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
    appointments = Appointment.query.all()
    now = datetime.now()


    return render_template('dashboard.html', user=current_user, 
                           medical_records=user_medical_records, 
                           appointments=user_appointments, 
                           payments=user_payments,
                           now=now)

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
        try:
            new_appointment = Appointment(
                patient_id=current_user.user_id,
                doctor_id=1,
                service_type=form.service_type.data,
                date_time=form.get_date_time(),
                status='Pending'
            )
            db.session.add(new_appointment)
            db.session.commit()
            flash('Appointment booked successfully', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred. Please try again.', 'danger')
            print(f"Error during appointment booking: {e}")
    else:
        print("Form validation failed")
        print(form.errors)
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
    return render_template('news.html')
@app.route('/update_info')
def update_info():
    return render_template('update_info.html')


@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    users = User.query.all()
    pending_appointments = Appointment.query.filter_by(status='Pending').all()
    
    total_billed = db.session.query(db.func.sum(Payment.payment_info)).scalar() or 0
    total_paid = 0
    balance = total_billed - total_paid
    
    return render_template('admin_dashboard.html', 
                           users=users, 
                           pending_appointments=pending_appointments,
                           total_billed=total_billed,
                           total_paid=total_paid,
                           balance=balance)

@app.route('/search_user', methods=['POST'])
@login_required
def search_user():
    email = request.form.get('email')
    phone_number = request.form.get('phone_number')
    user = None
    if email:
        user = User.query.filter_by(email=email).first()
    elif phone_number:
        user = User.query.filter_by(phone_number=phone_number).first()
    
    return render_template('admin_dashboard.html', users=[user] if user else [])

@app.route('/approve_appointment/<int:appointment_id>', methods=['POST'])
@login_required
def approve_appointment(appointment_id):
    appointment = Appointment.query.get(appointment_id)
    if appointment:
        appointment.status = 'Approved'
        db.session.commit()
    return redirect(url_for('admin_dashboard'))

@app.route('/remove_appointment/<int:appointment_id>', methods=['POST'])
@login_required
def remove_appointment(appointment_id):
    appointment = Appointment.query.get(appointment_id)
    if appointment:
        db.session.delete(appointment)
        db.session.commit()
    return redirect(url_for('admin_dashboard'))

@app.route('/remove_user/<int:user_id>', methods=['POST'])
@login_required
def remove_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
    return redirect(url_for('admin_dashboard'))

"""@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password_request():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        if user:
            token = s.dumps(user.email, salt='password-reset-salt')
            reset_link = url_for('reset_password', token=token, _external=True)
            msg = Message('Password Reset Request', sender=app.config['MAIL_DEFAULT_SENDER'], recipients=[user.email])
            msg.body = f'Your link to reset the password is {reset_link}. The link is valid for 1 hour.'
            mail.send(msg)
            flash('A password reset link has been sent to your email.', 'info')          
        else:
            flash('Email not found', 'error')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html')"""

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password_request():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        if user:
            token = s.dumps(user.email, salt='password-reset-salt')
            reset_link = url_for('reset_password', token=token, _external=True)
            msg = Message('Password Reset Request', sender=app.config['MAIL_DEFAULT_SENDER'], recipients=[user.email])
            msg.body = f'Your link to reset the password is {reset_link}. The link is valid for 1 hour.'
            mail.send(msg)
            flash('A password reset link has been sent to your email.', 'info')
        else:
            flash('Email not found', 'error')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html')

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        email = s.loads(token, salt='password-reset-salt', max_age=3600)
    except:
        flash('The reset link is invalid or has expired.', 'error')
        return redirect(url_for('reset_password_request'))
    
    if request.method == 'POST':
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user:
            user.password = generate_password_hash(password)
            db.session.commit()
            flash('Your password has been updated!', 'success')
            return redirect(url_for('login'))
        else:
            flash('User not found', 'error')
            return redirect(url_for('reset_password_request'))
    
    return render_template('reset_password.html', token=token)



if __name__ == '__main__':
    app.run(debug=True)

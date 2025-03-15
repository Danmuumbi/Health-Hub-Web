from flask import Flask, render_template, redirect, url_for, flash, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,timedelta
from flask_wtf import FlaskForm
from functools import wraps
from wtforms import StringField, PasswordField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required
from flask_migrate import Migrate
from config import Config
from models import db, User, MedicalRecord, Appointment, Department, Payment, Product, OrderItem, Order, DoctorAppointment, Doctor, doctor_models
from forms import RegistrationForm, LoginForm, MedicalRecordForm, AppointmentForm, PaymentForm
import logging
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from sqlalchemy.exc import IntegrityError 
from werkzeug.security import check_password_hash, generate_password_hash
import os
from werkzeug.utils import secure_filename
import requests

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
migrate = Migrate(app, db)

# Initialize Flask-Mail
mail = Mail(app)
s = URLSafeTimedSerializer(app.config['SECRET_KEY'])

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

logging.basicConfig(level=logging.DEBUG)

""" Requesting API from sell_goods """
@app.route('/health_hub_route')
def health_hub_route():
    sell_goods_response = requests.get('http://localhost:5001/api/sell_goods_data')
    
    if sell_goods_response.status_code == 200:
        sell_goods_data = sell_goods_response.json()['goods']
        return jsonify({'sell_goods_data': sell_goods_data})
    else:
        return jsonify({'error': 'Failed to fetch sell_goods data'}), 500
    

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

""" End of fetching data """
@app.route('/sell_goods')
def sell_goods():
    return render_template('products_sale.html')

# Load user function with role check
@login_manager.user_loader
def load_user(user_id):
    if session.get('role') == 'doctor':
        return Doctor.query.get(int(user_id))
    return User.query.get(int(user_id))

@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html')

# User registration route
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
            session['role'] = 'user'  # Set the session role for users
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

# User login route
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        logging.debug("Login form validation successful.")
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['role'] = 'user'  # Set the session role for users
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    else:
        logging.debug("Login form validation failed.")
        logging.debug(form.errors)
    return render_template('login.html', title='Login', form=form)

# Logout route
@app.route("/logout")
@login_required
def logout():
    logout_user()
    session.clear()  # Clear the session
    return redirect(url_for('home'))    

# Dashboard route with role-based redirection
@app.route("/dashboard")
@login_required
def dashboard():
    if session.get('role') == 'doctor':
        return redirect(url_for('doctor_dashboard'))
    
    user_medical_records = MedicalRecord.query.filter_by(user_id=current_user.user_id).all()
    user_appointments = Appointment.query.filter_by(patient_id=current_user.user_id).all()
    user_payments = Payment.query.filter_by(user_id=current_user.user_id).all()
    now = datetime.now()

    return render_template('dashboard.html', user=current_user, 
                           medical_records=user_medical_records, 
                           appointments=user_appointments, 
                           payments=user_payments,
                           now=now)

# Route to add medical record
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

# Route to add appointment
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

# Route to add payment


@app.route("/add_payment", methods=['GET', 'POST'])
def add_payment():
    form = PaymentForm()
    if form.validate_on_submit():
        flash('Payment made successfully', 'success')
        return redirect(url_for('home'))  # Redirect to the dashboard or the appropriate page after successful payment
    
    return render_template('new_payment.html', form=form)  # Render the form again if validation fails or if it's a GET request


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

from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature

from flask_mail import Message

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password_request():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        if user:
            token = s.dumps(user.email, salt='password-reset-salt')
            reset_link = url_for('reset_password', token=token, _external=True)
            try:
                msg = Message('Password Reset Request', sender=app.config['MAIL_USERNAME'], recipients=[user.email])
                msg.body = f'Your link to reset the password is {reset_link}. The link is valid for 1 hour.'
                mail.send(msg)
                flash('A password reset link has been sent to your email.', 'info')
            except Exception as e:
                flash(f'Failed to send email: {str(e)}', 'error')
        else:
            flash('Email not found', 'error')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html')



@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        email = s.loads(token, salt='password-reset-salt', max_age=3600)
    except SignatureExpired:
        flash('The reset link is invalid or has expired.', 'error')
        return redirect(url_for('reset_password_request'))
    except BadSignature:
        flash('The reset link is invalid.', 'error')
        return redirect(url_for('reset_password_request'))
    
    if request.method == 'POST':
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user:
            user.password = bcrypt.generate_password_hash(password).decode('utf-8')
            db.session.commit()
            flash('Your password has been updated!', 'success')
            return redirect(url_for('login'))
        else:
            flash('User not found', 'error')
            return redirect(url_for('reset_password_request'))
    
    return render_template('reset_password.html', token=token)



@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([
        {
            'product_id': product.product_id,
            'product_name': product.product_name,
            'description': product.description,
            'price': str(product.price),
            'stock': product.stock,
            'image': product.image
        } for product in products
    ])

@app.route('/products', methods=['POST'])
def add_product():
    data = request.form
    file = request.files.get('image')
    image_path = None

    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    new_product = Product(
        product_name=data['product_name'],
        description=data['description'],
        price=data['price'],
        stock=data['stock'],
        image=image_path
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify({"message": "Product added successfully!"}), 201

@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"message": "Product not found"}), 404

    data = request.form
    file = request.files.get('image')
    image_path = None

    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    product.product_name = data['product_name']
    product.description = data['description']
    product.price = data['price']
    product.stock = data['stock']
    product.image = image_path
    db.session.commit()
    return jsonify({"message": "Product updated successfully!"}), 200

@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"message": "Product not found"}), 404

    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted successfully!"}), 200

@app.route('/orders', methods=['POST'])
def place_order():
    data = request.json
    new_order = Order(
        buyer_id=data['buyer_id'],
        total_amount=data['total_amount'],
        status="Pending"
    )
    db.session.add(new_order)
    db.session.commit()

    for item in data['items']:
        order_item = OrderItem(
            order_id=new_order.order_id,
            product_id=item['product_id'],
            quantity=item['quantity'],
            price=item['price']
        )
        db.session.add(order_item)
    
    db.session.commit()
    return jsonify({"message": "Order placed successfully!"}), 201

@app.route('/public_products')
def public_products():
    sell_goods_response = requests.get('http://localhost:5001/api/sell_goods_data')
    
    if sell_goods_response.status_code == 200:
        sell_goods_data = sell_goods_response.json()['goods']
        return render_template('public_products.html', goods=sell_goods_data)
    else:
        flash('Failed to retrieve goods data', 'danger')
        return redirect(url_for('home'))

""" Doctors Information """

@login_manager.user_loader
def load_user(user_id):
    if session.get('role') == 'doctor':
        return Doctor.query.get(int(user_id))
    return User.query.get(int(user_id))

# Doctor login route with role session setting
@app.route('/doctor_login', methods=['GET', 'POST'])
def doctor_login():
    form = LoginForm()
    if form.validate_on_submit():
        doctor = Doctor.query.filter_by(email=form.email.data).first()
        if doctor and check_password_hash(doctor.password, form.password.data):
            session['role'] = 'doctor'  # Set the session role for doctors
            login_user(doctor)
            return redirect(url_for('doctor_dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('doctor_login.html', title='Doctor Login', form=form)

# Doctor registration route

from flask import current_app

@app.route('/doctor_register', methods=['GET', 'POST'])
def doctor_register():
    form = RegistrationForm()  # Assuming you have a separate form for doctors
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        profile_picture = form.profile_picture.data

        if profile_picture:
            filename = secure_filename(profile_picture.filename)
            profile_picture_folder = os.path.join(current_app.root_path, 'static/profile_pics')
            os.makedirs(profile_picture_folder, exist_ok=True)
            profile_picture_path = os.path.join(profile_picture_folder, filename)
            profile_picture.save(profile_picture_path)
            profile_picture_url = os.path.join('static/profile_pics', filename)
        else:
            profile_picture_url = None

        new_doctor = Doctor(username=form.username.data, email=form.email.data, password=hashed_password,
                            date_of_birth=form.date_of_birth.data, gender=form.gender.data,
                            address=form.address.data, phone_number=form.phone_number.data,
                            profile_picture=profile_picture_url)

        try:
            db.session.add(new_doctor)
            db.session.commit()
            flash('Registration successful!', 'success')
            return redirect(url_for('doctor_login'))
        except IntegrityError:
            db.session.rollback()
            flash('Email address already exists', 'danger')
    else:
        print(f"Form validation failed: {form.errors}")

    return render_template('doctor_register.html', title='Doctor Register', form=form)


@app.route('/doctor_dashboard')
@login_required
def doctor_dashboard():
    if session.get('role') != 'doctor':
        return redirect(url_for('dashboard'))
    
    doctor_id = current_user.get_id()
    doctor = Doctor.query.get(doctor_id)
    
    # Fetch all appointments for this doctor
    appointments = Appointment.query.filter_by(doctor_id=doctor_id).all()
    
    # Filter for pending appointments
    pending_appointments = [appt for appt in appointments if appt.status == 'Pending']
    
    # Get today's appointments
    now = datetime.now()
    today_start = datetime(now.year, now.month, now.day)
    today_end = today_start + timedelta(days=1)
    today_appointments = [appt for appt in appointments if today_start <= appt.date_time < today_end]
    
    appointments_by_hour = {}
    for appointment in appointments:
        hour = appointment.date_time.hour
        if hour not in appointments_by_hour:
            appointments_by_hour[hour] = []
        appointments_by_hour[hour].append(appointment)
    
    return render_template(
        'doctor_dashboard.html',
        doctor=doctor,
        appointments=appointments,
        pending_appointments=pending_appointments,
        today_appointments=today_appointments,
        appointments_by_hour=appointments_by_hour,
        now=now
    )


@app.route('/appointments/today')
@login_required
def todays_appointments():
    # Fetch all pending appointments for today
    now = datetime.now()
    today_start = datetime(now.year, now.month, now.day)
    today_end = today_start + timedelta(days=1)

    pending_appointments = Appointment.query.filter(
        Appointment.date_time >= today_start,
        Appointment.date_time < today_end,
        Appointment.status == 'Pending'
    ).all()

    return render_template('today_appointments.html', pending_appointments=pending_appointments, now=now)


@app.route('/approves_appointment', methods=['POST'])
@login_required
def approves_appointment():
    appointment_id = request.form.get('appointment_id')
    price = request.form.get('price')
    now = datetime.now()
    
    appointment = Appointment.query.get(appointment_id)
    if appointment:
        appointment.status = 'Approved'
        appointment.price = price
        db.session.commit()
        now=now
        
    
    return redirect(url_for('doctor_dashboard'))


@app.route('/display_appointments')
@login_required
def display_appointments():
    now = datetime.now()
    pending_appointments = Appointment.query.filter(Appointment.status != 'Approved', Appointment.date_time > now).all()
    approved_appointments = Appointment.query.filter(Appointment.status == 'Approved', Appointment.date_time > now).all()
    approved_appointments_count = len(approved_appointments)

    return render_template('display_appointments.html', 
                           pending_appointments=pending_appointments, 
                           approved_appointments=approved_appointments, 
                           approved_appointments_count=approved_appointments_count,now=now)






if __name__ == '__main__':
    app.run(port=5000, debug=True)


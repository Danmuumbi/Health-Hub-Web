from flask import Flask, render_template, redirect, url_for, flash, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_wtf import FlaskForm
from functools import wraps
from wtforms import StringField, PasswordField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required
from flask_migrate import Migrate
from config import Config
from models import db, User, MedicalRecord, Appointment, Department, Payment, Product, OrderItem, Order
from forms import RegistrationForm, LoginForm, MedicalRecordForm, AppointmentForm, PaymentForm
import logging
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from sqlalchemy.exc import IntegrityError 
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

#  i Initialized Flask-Mail
mail = Mail(app)
s = URLSafeTimedSerializer(app.config['SECRET_KEY'])

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

logging.basicConfig(level=logging.DEBUG)
"""requsting api from sell_goods"""
@app.route('/health_hub_route')
def health_hub_route():
    # Make a request to the sell_goods API to fetch goods data
    sell_goods_response = requests.get('http://localhost:5001/api/sell_goods_data')
    
    if sell_goods_response.status_code == 200:
        # If the request was successful, extract the goods data from the response
        sell_goods_data = sell_goods_response.json()['goods']
        return jsonify({'sell_goods_data': sell_goods_data})
    else:
        # If the request failed, return an error response
        return jsonify({'error': 'Failed to fetch sell_goods data'}), 500
    

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


"""end of fetching my data"""
@app.route('/sell_goods')
def sell_goods():
    return render_template('products_sale.html')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password_request():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        if user:
            token = s.dumps(user.email, salt='password-reset-salt')
            reset_link = url_for('reset_password', token=token, _external=True)
            msg = Message('Password Reset Request', sender=app.config['MAIL_USERNAME'], recipients=[user.email])
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
            user.password = bcrypt.generate_password_hash(password).decode('utf-8')
            db.session.commit()
            flash('Your password has been updated!', 'success')
            return redirect(url_for('login'))
        else:
            flash('User not found', 'error')
            return redirect(url_for('reset_password_request'))
    
    return render_template('reset_password.html', token=token)

"""@app.route('/products_sale')
def products_sale():
    return render_template('products_sale.html')"""

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


if __name__ == '__main__':
    app.run(port=5000,debug=True)


from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'Users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    address = db.Column(db.String(255))
    phone_number = db.Column(db.String(15))
    profile_picture = db.Column(db.LargeBinary)
    
    # Establishing relationship with Appointment
    appointments = db.relationship('Appointment', back_populates='patient')

class MedicalRecord(db.Model):
    __tablename__ = 'Medical_Records'
    record_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)
    medical_history = db.Column(db.Text)
    medications = db.Column(db.Text)
    vaccination_record = db.Column(db.Text)
    lab_results = db.Column(db.Text)
    allergies = db.Column(db.Text)
    immunizations = db.Column(db.Text)
    
    user = db.relationship('User', back_populates='medical_records')

class Appointment(db.Model):
    __tablename__ = 'Appointments'
    appointment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)
    doctor_id = db.Column(db.Integer, nullable=False)  # Assuming doctor_id is a reference to another table
    service_type = db.Column(db.String(100))
    date_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50))

    # Establishing relationship with User
    patient = db.relationship('User', back_populates='appointments')

class Department(db.Model):
    __tablename__ = 'Departments'
    department_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    department_name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(255))
    contact_info = db.Column(db.String(255))

class Payment(db.Model):
    __tablename__ = 'Payments'
    payment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)
    payment_info = db.Column(db.Text, nullable=False)
    
    user = db.relationship('User', back_populates='payments')
class Product(db.Model):
    product_id = db.Column(db.Integer, primary_key=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    product_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    image = db.Column(db.LargeBinary)

class Order(db.Model):
    order_id = db.Column(db.Integer, primary_key=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(50))

class OrderItem(db.Model):
    order_item_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.order_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)

# Define your routes here
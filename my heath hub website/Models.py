from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

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

class Appointment(db.Model):
    __tablename__ = 'Appointments'
    appointment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)
    doctor_id = db.Column(db.Integer, nullable=False)  # Assuming doctor_id is a reference to another table
    service_type = db.Column(db.String(100))
    date_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50))

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

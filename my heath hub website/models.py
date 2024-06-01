# models.py
from app import db

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.String(10))
    address = db.Column(db.String(255))
    phone_number = db.Column(db.String(20))
    profile_picture = db.Column(db.String(255))

class MedicalRecord(db.Model):
    __tablename__ = 'medical_records'
    record_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    medical_history = db.Column(db.Text)
    medications = db.Column(db.Text)
    vaccination_record = db.Column(db.Text)
    lab_results = db.Column(db.Text)
    allergies = db.Column(db.Text)
    immunizations = db.Column(db.Text)

class Appointment(db.Model):
    __tablename__ = 'appointments'
    appointment_id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    service_type = db.Column(db.String(100))
    date_time = db.Column(db.DateTime)
    status = db.Column(db.String(50))

class Department(db.Model):
    __tablename__ = 'departments'
    department_id = db.Column(db.Integer, primary_key=True)
    department_name = db.Column(db.String(100))
    location = db.Column(db.String(255))
    contact_information = db.Column(db.String(255))

class Payment(db.Model):
    __tablename__ = 'payments'
    payment_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    payment_information = db.Column(db.String(255))

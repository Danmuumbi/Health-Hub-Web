from . import db
from flask_login import UserMixin

class Doctor(db.Model, UserMixin):
    __tablename__ = 'Doctors'
    doctor_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    address = db.Column(db.String(255))
    phone_number = db.Column(db.String(15))
    profile_picture = db.Column(db.String(200), nullable=True) 
   #profile_picture = db.Column(db.LargeBinary)

    appointments = db.relationship('DoctorAppointment', back_populates='doctor')

    def get_id(self):
        return str(self.doctor_id)

class DoctorAppointment(db.Model):
    __tablename__ = 'Doctor_Appointments'
    appointment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('Doctors.doctor_id'), nullable=False)
    service_type = db.Column(db.String(100))
    date_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50))

    doctor = db.relationship('Doctor', back_populates='appointments')
    patient = db.relationship('User')
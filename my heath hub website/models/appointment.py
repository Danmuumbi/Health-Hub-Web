from . import db

class Appointment(db.Model):
    __tablename__ = 'Appointments'
    appointment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)
    doctor_id = db.Column(db.Integer, nullable=False)  # Assuming doctor_id is a reference to another table
    service_type = db.Column(db.String(100))
    date_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50))
    patient = db.relationship('User', back_populates='appointments')
    price = db.Column(db.Numeric(10, 2))


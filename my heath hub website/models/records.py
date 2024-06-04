# Models/medical_record.py
from . import db
from datetime import datetime

class MedicalRecord(db.Model):
    __tablename__ = 'medical_records'
    record_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    medical_history = db.Column(db.Text)
    medications = db.Column(db.Text)
    vaccination_record = db.Column(db.Text)
    lab_results = db.Column(db.Text)
    allergies = db.Column(db.Text)
    immunizations = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

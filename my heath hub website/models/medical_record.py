from . import db

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

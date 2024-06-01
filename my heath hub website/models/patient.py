"""from models.base_model import BaseModel

class Patient(BaseModel):
    def __init__(self, *args, **kwargs):
        self.name = ""
        self.age = 0
        self.medical_history = ""
        self.contact_info = ""
        super().__init__(*args, **kwargs)
"""
from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

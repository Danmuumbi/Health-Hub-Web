from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User
from .medical_record import MedicalRecord
from .appointment import Appointment
from .department import Department
from .payment import Payment

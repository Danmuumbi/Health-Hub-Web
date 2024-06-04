from . import db

class Department(db.Model):
    __tablename__ = 'Departments'
    department_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    department_name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(255))
    contact_info = db.Column(db.String(255))

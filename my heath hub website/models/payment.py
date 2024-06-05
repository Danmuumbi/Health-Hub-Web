from . import db

class Payment(db.Model):
    __tablename__ = 'Payments'
    payment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)
    payment_info = db.Column(db.Text, nullable=False)
    user = db.relationship('User', back_populates='payments')
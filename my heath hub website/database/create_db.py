from app import app
from models import db
from models.user import User  # Import other models if necessary

with app.app_context():
    db.create_all()

"""from app import db
from models.user import User  # Import all models you have

def create_database():
    db.create_all()

if __name__ == '__main__':
    create_database()"""

from app import app
from models import db
from models.user import User  # Import other models if necessary

with app.app_context():
    db.create_all()

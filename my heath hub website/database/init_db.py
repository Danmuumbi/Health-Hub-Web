from flask_sqlalchemy import SQLAlchemy
from api import api
from models import User, Post  # Assuming you have User and Post models defined in models.py

# Initialize SQLAlchemy with the Flask app
db = SQLAlchemy(app)

# Function to initialize the database
def init_db():
    # Create all tables
    db.create_all()

    # Seed initial data
    # Example: Creating a user
    user1 = User(username='example_user', email='user@example.com')
    db.session.add(user1)

    # Example: Creating a post
    post1 = Post(title='First Post', content='This is the content of the first post.', user=user1)
    db.session.add(post1)

    # Commit changes to the database
    db.session.commit()

# Run the init_db function to initialize the database
if __name__ == '__main__':
    init_db()

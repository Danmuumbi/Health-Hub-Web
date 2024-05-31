from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Create Flask application instance
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # Adjust this to your database connection URI

# Initialize SQLAlchemy with the Flask app
db = SQLAlchemy(app)

# Import routes and models
from views import *
from models import *

if __name__ == '__main__':
        app.run(debug=True)


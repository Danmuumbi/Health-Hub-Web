from flask import Blueprint, render_template

user_bp = Blueprint('user', __name__)

@user_bp.route('/profile')
def profile():
    # Handle user profile view logic here
    return render_template('profile.html')

@user_bp.route('/appointments')
def appointments():
    # Handle user appointments view logic here
    return render_template('appointments.html')

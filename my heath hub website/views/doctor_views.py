from flask import Blueprint, render_template

doctor_bp = Blueprint('doctor', __name__)

@doctor_bp.route('/profile')
def profile():
    # Handle doctor profile view logic here
    return render_template('doctor_profile.html')

@doctor_bp.route('/schedule')
def schedule():
    # Handle doctor schedule view logic here
    return render_template('schedule.html')

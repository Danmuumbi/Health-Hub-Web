from flask import Blueprint, render_template

appointment_bp = Blueprint('appointment', __name__)

@appointment_bp.route('/book')
def book():
    # Handle appointment booking logic here
    return render_template('book_appointment.html')

@appointment_bp.route('/view')
def view():
    # Handle appointment view logic here
    return render_template('view_appointments.html')

@appointment_bp.route('/cancel')
def cancel():
    # Handle appointment cancellation logic here
    return render_template('cancel_appointment.html')

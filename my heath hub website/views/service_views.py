from flask import Blueprint, render_template

service_bp = Blueprint('service', __name__)

@service_bp.route('/view')
def view():
    # Handle service view logic here
    return render_template('view_services.html')

@service_bp.route('/book')
def book():
    # Handle service booking logic here
    return render_template('book_service.html')

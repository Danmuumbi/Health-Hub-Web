from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField, SubmitField, IntegerField
from wtforms.validators import DataRequired, ValidationError
from datetime import datetime

class AppointmentForm(FlaskForm):
    service_type = StringField('Service Type', validators=[DataRequired()])
    date_time = StringField('Date and Time', validators=[DataRequired()])
    doctor_id = IntegerField('Doctor ID', validators=[DataRequired()])
    status = StringField('Status', default='Pending')
    submit = SubmitField('Book Appointment')

    def validate_date_time(form, field):
        try:
            datetime.strptime(field.data, '%Y-%m-%dT%H:%M')
        except ValueError:
            raise ValidationError("Invalid date and time format")

    def get_date_time(self):
        return datetime.strptime(self.date_time.data, '%Y-%m-%dT%H:%M')

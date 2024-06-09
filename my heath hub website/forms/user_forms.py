from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateTimeField, SubmitField, PasswordField, DateField, SelectField,IntegerField,FileField
from wtforms.validators import DataRequired, Email, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    date_of_birth = DateField('Date of Birth', format='%Y-%m-%d', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')])
    address = StringField('Address')
    phone_number = StringField('Phone Number')
    submit = SubmitField('Sign Up')
    profile_picture = FileField('Profile Picture')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class MedicalRecordForm(FlaskForm):
    medical_history = TextAreaField('Medical History', validators=[DataRequired()])
    medications = TextAreaField('Medications')
    vaccination_record = TextAreaField('Vaccination Record')
    lab_results = TextAreaField('Lab Results')
    allergies = TextAreaField('Allergies')
    immunizations = TextAreaField('Immunizations')
    submit = SubmitField('Add Medical Record')


class AppointmentForm(FlaskForm):
    service_type = StringField('Service Type', validators=[DataRequired()])
    date_time = DateTimeField('Date and Time', format='%Y-%m-%d %H:%M:%S', validators=[DataRequired()])
    doctor_id = IntegerField('Doctor ID', validators=[DataRequired()])  # Adjust as needed
    submit = SubmitField('Book Appointment')


class PaymentForm(FlaskForm):
    payment_info = TextAreaField('Payment Info', validators=[DataRequired()])
    submit = SubmitField('Make Payment')

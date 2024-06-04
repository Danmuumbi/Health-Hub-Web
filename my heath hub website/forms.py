"""from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from wtforms import StringField, TextAreaField, DateTimeField, SubmitField

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
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
    status = StringField('Status')
    submit = SubmitField('Book Appointment')

class PaymentForm(FlaskForm):
    payment_info = TextAreaField('Payment Info', validators=[DataRequired()])
    submit = SubmitField('Make Payment')
"""

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateTimeField, SubmitField, PasswordField, DateField, SelectField
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
    status = StringField('Status')
    submit = SubmitField('Book Appointment')

class PaymentForm(FlaskForm):
    payment_info = TextAreaField('Payment Info', validators=[DataRequired()])
    submit = SubmitField('Make Payment')

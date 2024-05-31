import random
import string
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

def generate_confirmation_code(length=6):
    """Generate a random confirmation code."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def send_email(subject, recipient, body):
    """Send an email using SMTP."""
    smtp_server = 'smtp.example.com'
    smtp_port = 587
    sender_email = 'your_email@example.com'
    sender_password = 'your_email_password'

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)

def format_date(date):
    """Format a date string to a human-readable format."""
    return datetime.strptime(date, '%Y-%m-%d').strftime('%B %d, %Y')

def calculate_age(birth_date):
    """Calculate the age based on the birth date."""
    today = datetime.today()
    birth_date = datetime.strptime(birth_date, '%Y-%m-%d')
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age

def generate_random_string(length=10):
    """Generate a random string."""
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

def capitalize_words(text):
    """Capitalize each word in a string."""
    return ' '.join(word.capitalize() for word in text.split())

def shuffle_list(lst):
    """Shuffle a list."""
    random.shuffle(lst)
    return lst

def reverse_string(text):
    """Reverse a string."""
    return text[::-1]

def calculate_average(numbers):
    """Calculate the average of a list of numbers."""
    return sum(numbers) / len(numbers)

# Test the helper functions here
if __name__ == '__main__':
    confirmation_code = generate_confirmation_code()
    print("Generated Confirmation Code:", confirmation_code)

    subject = "Test Email"
    recipient = "recipient@example.com"
    body = "This is a test email."
    send_email(subject, recipient, body)
    print("Email sent successfully.")

    date_string = "2022-01-15"
    formatted_date = format_date(date_string)
    print("Formatted Date:", formatted_date)

    birth_date = "1990-05-25"
    age = calculate_age(birth_date)
    print("Age:", age)

    random_string = generate_random_string()
    print("Generated Random String:", random_string)

    text = "hello world"
    capitalized_text = capitalize_words(text)
    print("Capitalized Words:", capitalized_text)

    lst = [1, 2, 3, 4, 5]
    shuffled_lst = shuffle_list(lst)
    print("Shuffled List:", shuffled_lst)

    reversed_text = reverse_string(text)
    print("Reversed String:", reversed_text)

    numbers = [10, 20, 30, 40, 50]
    average = calculate_average(numbers)
    print("Average:", average)

import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '4055426f967b2918f67f318085e74a5d296101935e692efc0ce0e3f5bb0025a4'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:%40Mmuuo2015@localhost/health_hub'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com',
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'muumbidaniel0@gmail.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'mmuuo2015'
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or 'muumbidaniel0@gmail.com'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'app/static/uploads')
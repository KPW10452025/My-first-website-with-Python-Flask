import os

from dotenv import load_dotenv
load_dotenv()

class Config(object):
    
    # Database configuration
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../app.db'

    # Secret key
    SECRET_KEY = os.environ.get('SECRET_KEY')

    # RECAPTCHA KEY
    RECAPTCHA_PUBLIC_KEY = os.environ.get("RECAPTCHA_PUBLIC_KEY")
    RECAPTCHA_PRIVATE_KEY = os.environ.get("RECAPTCHA_PRIVATE_KEY")

    # flask-mail by gmail configuration
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get("GMAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("GMAIL_PASSWORD")

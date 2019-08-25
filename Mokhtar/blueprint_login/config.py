import os

'''SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')'''

class Config:
	SECRET_KEY = '6673ffee83188cb99b4acff21ef56e03'
	SQLALCHEMY_DATABASE_URI = 'sqlite:///login.db'


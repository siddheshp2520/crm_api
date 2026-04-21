import os

class Config:
    # MySQL
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.environ.get('MYSQL_USER', 'crm')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '1234')
    MYSQL_DB = os.environ.get('MYSQL_DB', 'crm')

    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY', 'crm-secret-key')
    DEBUG = False
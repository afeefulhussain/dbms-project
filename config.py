import os

class Config:
    # MySQL Database Configuration
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_PORT = int(os.environ.get('MYSQL_PORT', 3306))
    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '@feef123')
    MYSQL_DB = os.environ.get('MYSQL_DB', 'clinic_db')
    
    # Flask App Secret Key
    SECRET_KEY = os.environ.get('SECRET_KEY', 'clinic_secret_key_2026_uet_dbms')

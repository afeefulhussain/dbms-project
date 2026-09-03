import os
from urllib.parse import urlparse

class Config:
    # Check if Railway provided a full MySQL connection URL (e.g. MYSQL_URL or DATABASE_URL)
    db_url = os.environ.get('MYSQL_URL') or os.environ.get('DATABASE_URL')
    
    if db_url and (db_url.startswith('mysql://') or db_url.startswith('mysql+pymysql://')):
        parsed = urlparse(db_url)
        MYSQL_HOST = parsed.hostname
        MYSQL_PORT = int(parsed.port or 3306)
        MYSQL_USER = parsed.username or 'root'
        MYSQL_PASSWORD = parsed.password or ''
        MYSQL_DB = parsed.path.lstrip('/') if parsed.path else 'clinic_db'
    else:
        # Check standard variables or Railway individual variables (MYSQLHOST, MYSQLUSER, etc.)
        MYSQL_HOST = os.environ.get('MYSQLHOST') or os.environ.get('MYSQL_HOST') or 'localhost'
        MYSQL_PORT = int(os.environ.get('MYSQLPORT') or os.environ.get('MYSQL_PORT') or 3306)
        MYSQL_USER = os.environ.get('MYSQLUSER') or os.environ.get('MYSQL_USER') or 'root'
        MYSQL_PASSWORD = os.environ.get('MYSQLPASSWORD') or os.environ.get('MYSQL_PASSWORD') or '@feef123'
        MYSQL_DB = os.environ.get('MYSQLDATABASE') or os.environ.get('MYSQL_DB') or 'clinic_db'

    # Flask App Secret Key
    SECRET_KEY = os.environ.get('SECRET_KEY', 'clinic_secret_key_2026_uet_dbms')

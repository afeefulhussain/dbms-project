import pymysql
import pymysql.cursors
from config import Config

def get_db_connection(use_db=True):
    """Establishes a connection to the MySQL database."""
    return pymysql.connect(
        host=Config.MYSQL_HOST,
        port=Config.MYSQL_PORT,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DB if use_db else None,
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )

def query_db(query, args=(), one=False):
    """Executes a SELECT query and returns the results."""
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, args)
            rv = cursor.fetchall()
            return (rv[0] if rv else None) if one else rv
    finally:
        conn.close()

def execute_db(query, args=()):
    """Executes an INSERT, UPDATE, or DELETE query."""
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, args)
            last_id = cursor.lastrowid
            return last_id
    finally:
        conn.close()

def init_db():
    """Creates the database and tables if they don't exist and seeds initial data."""
    # Connect without specific DB to create database
    conn = get_db_connection(use_db=False)
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{Config.MYSQL_DB}`;")
    finally:
        conn.close()

    # Connect to the created DB and execute table creation
    conn = get_db_connection(use_db=True)
    try:
        with conn.cursor() as cursor:
            # 1. Admins Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS admins (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    name VARCHAR(100) DEFAULT 'System Admin',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

            # 2. Receptionists Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS receptionists (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    receptionist_code VARCHAR(50) UNIQUE NOT NULL,
                    name VARCHAR(100) NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

            # 3. Doctors Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS doctors (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    phone VARCHAR(30) NOT NULL,
                    specialization VARCHAR(100) NOT NULL,
                    password VARCHAR(255) DEFAULT '123456',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

            # 4. Patients Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS patients (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    token_number INT NOT NULL,
                    name VARCHAR(100) NOT NULL,
                    doctor_id INT NOT NULL,
                    receptionist_id INT NULL,
                    appointment_date VARCHAR(20) NOT NULL,
                    appointment_time VARCHAR(20) NOT NULL,
                    is_checked TINYINT(1) DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (doctor_id) REFERENCES doctors(id) ON DELETE CASCADE,
                    FOREIGN KEY (receptionist_id) REFERENCES receptionists(id) ON DELETE SET NULL
                );
            """)

            # Seed Default Admin if not exists
            cursor.execute("SELECT id FROM admins WHERE username = 'admin'")
            if not cursor.fetchone():
                cursor.execute(
                    "INSERT INTO admins (username, password, name) VALUES (%s, %s, %s)",
                    ('admin', 'admin123', 'Super Admin')
                )

            # Seed Sample Doctors if table empty
            cursor.execute("SELECT COUNT(*) as count FROM doctors")
            if cursor.fetchone()['count'] == 0:
                sample_doctors = [
                    ('Dr. Ahmed Khan', '0300-1234567', 'ENT Specialist', '123456'),
                    ('Dr. Ayesha Malik', '0312-7654321', 'Skin Specialist', '123456'),
                    ('Dr. Usman Tariq', '0321-9876543', 'General Physician', '123456'),
                    ('Dr. Fatima Noor', '0333-5554433', 'Cardiologist', '123456')
                ]
                for doc in sample_doctors:
                    cursor.execute(
                        "INSERT INTO doctors (name, phone, specialization, password) VALUES (%s, %s, %s, %s)",
                        doc
                    )

            # Seed Sample Receptionist if table empty
            cursor.execute("SELECT COUNT(*) as count FROM receptionists")
            if cursor.fetchone()['count'] == 0:
                sample_receptionists = [
                    ('REC101', 'Zainab Bibi', 'pass123'),
                    ('REC102', 'Bilal Hassan', 'pass123')
                ]
                for rec in sample_receptionists:
                    cursor.execute(
                        "INSERT INTO receptionists (receptionist_code, name, password) VALUES (%s, %s, %s)",
                        rec
                    )

            # Seed Sample Patients if table empty
            cursor.execute("SELECT COUNT(*) as count FROM patients")
            if cursor.fetchone()['count'] == 0:
                sample_patients = [
                    (1, 'Ali Raza', 1, 1, '2026-09-03', '10:00 AM', 0),
                    (2, 'Hamza Tariq', 1, 1, '2026-09-03', '10:30 AM', 0),
                    (3, 'Sara Ahmed', 2, 2, '2026-09-03', '11:00 AM', 0),
                    (4, 'Muhammad Omer', 3, 1, '2026-09-03', '11:30 AM', 1),
                ]
                for pat in sample_patients:
                    cursor.execute(
                        """INSERT INTO patients 
                           (token_number, name, doctor_id, receptionist_id, appointment_date, appointment_time, is_checked) 
                           VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                        pat
                    )
        print("Database initialized and verified successfully!")
    finally:
        conn.close()

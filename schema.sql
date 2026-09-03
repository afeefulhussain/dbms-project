-- ===================================================
-- Hospital & Clinic Management System Database Schema
-- Database: clinic_db
-- ===================================================

CREATE DATABASE IF NOT EXISTS clinic_db;
USE clinic_db;

-- 1. Admins Table
CREATE TABLE IF NOT EXISTS admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    name VARCHAR(100) DEFAULT 'System Admin',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Receptionists Table
CREATE TABLE IF NOT EXISTS receptionists (
    id INT AUTO_INCREMENT PRIMARY KEY,
    receptionist_code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Doctors Table
CREATE TABLE IF NOT EXISTS doctors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(30) NOT NULL,
    specialization VARCHAR(100) NOT NULL, -- ENT, Skin, General, Cardiology, etc.
    password VARCHAR(255) DEFAULT '123456',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Patients Table
CREATE TABLE IF NOT EXISTS patients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    token_number INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    doctor_id INT NOT NULL,
    receptionist_id INT NULL,
    appointment_date VARCHAR(20) NOT NULL,
    appointment_time VARCHAR(20) NOT NULL,
    is_checked TINYINT(1) DEFAULT 0, -- 0 = Waiting/Running, 1 = Checked
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (doctor_id) REFERENCES doctors(id) ON DELETE CASCADE,
    FOREIGN KEY (receptionist_id) REFERENCES receptionists(id) ON DELETE SET NULL
);

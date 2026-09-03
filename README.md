# MedCare — Clinic & Hospital Management Web System

A full-stack Web Application with a **MySQL Relational Database** backend built in **Python Flask**, adapted from the C++ Patient & Appointment Management System.

---

## 🎓 Academic Supervision & Acknowledgements

- **Course:** Database Management Systems (DBMS)
- **Institution:** University of Engineering and Technology (UET)
- **Project Supervisor & Course Instructor:** **Mrs. Minahil Tayyab**

*This project was developed under the guidance and academic supervision of Mrs. Minahil Tayyab as part of the DBMS course curriculum.*

---

## 🌟 Key Features & Role Breakdown

### 1. 🛡️ Admin Portal (`/admin`)
- **Manage Doctors**: Add doctor with Name, Phone, and Specialization (ENT, Skin, General, Cardiology, etc.), view directory, delete doctors.
- **Manage Receptionists**: Create receptionist accounts with unique Receptionist ID/Code and secure password.
- **Book Patients**: Direct appointment booking with auto-assigned token numbers.
- **Patient Directory**:
  - **View All Patients** (Token, Name, Assigned Doctor, Booked By, Date, Time, Status).
  - **View Running (Waiting) Patients** (Live pending queue).
  - **View Checked Patients** (Completed consultations).
  - One-click status toggle, record deletion, and Token slip printing.

### 2. 📇 Receptionist Desk (`/receptionist`)
- **Quick Patient Registration**: Book walk-in or scheduled appointments, select from active doctors, assign appointment date and time.
- **Auto-Token Generation**: Sequential token number tracking for clinic queues.
- **Appointment Lookup**: Search and filter by patient name, doctor, or token.
- **Print Token Receipt**: Generate printable patient appointment slips with 1 click.

### 3. 🩺 Doctor Workspace (`/doctor`)
- **Live My Patients Queue**: Real-time list of all unchecked (`Waiting`) patients assigned to the logged-in doctor, ordered by token.
- **Mark as Checked**: 1-click consultation completion action that moves patient from "Waiting" to "Checked".
- **Consultation History**: Past record of all checked patients.

### 4. 📺 Live Digital Signage / TV Queue Board (`/queue`)
- Real-time room-by-room patient calling board for the clinic waiting area (auto-refreshes every 10 seconds).

---

## 🗄️ MySQL Database Schema (`clinic_db`)

The application uses **MySQL 8.0** with foreign key relational integrity:

1. **`admins`**: `id`, `username`, `password`, `name`, `created_at`
2. **`receptionists`**: `id`, `receptionist_code`, `name`, `password`, `created_at`
3. **`doctors`**: `id`, `name`, `phone`, `specialization`, `password`, `created_at`
4. **`patients`**: `id`, `token_number`, `name`, `doctor_id` (FK), `receptionist_id` (FK), `appointment_date`, `appointment_time`, `is_checked` (0 = Waiting, 1 = Checked), `created_at`

---

## 🔑 Default Login Credentials

| Role | Login Identifier | Password | Access URL |
| :--- | :--- | :--- | :--- |
| **Admin** | `admin` | `admin123` | `http://127.0.0.1:5000/login?role=admin` |
| **Receptionist** | `REC101` | `pass123` | `http://127.0.0.1:5000/login?role=receptionist` |
| **Doctor** | `1` (or `Dr. Ahmed Khan`) | `123456` | `http://127.0.0.1:5000/login?role=doctor` |

---

## 🚀 How to Run the Application

### Option 1: Double-Click Batch File (Easiest)
Simply double click `run.bat` in the project folder.

### Option 2: Command Line
1. Open PowerShell / Command Prompt in the project folder:
   ```bash
   cd "d:\UET study\DBMS\project web"
   ```
2. Initialize Database and Tables (if not already done):
   ```bash
   python setup_db.py
   ```
3. Start the Flask Server:
   ```bash
   python app.py
   ```
4. Open your web browser and navigate to:
   **`http://127.0.0.1:5000`**

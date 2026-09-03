from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from functools import wraps
from config import Config
from db import query_db, execute_db, init_db
import datetime

app = Flask(__name__)
app.config.from_object(Config)

# Initialize database tables on app start
try:
    init_db()
except Exception as e:
    print(f"Warning: Could not auto-init DB on start: {e}")


# ==========================================
# AUTHENTICATION & ACCESS DECORATORS
# ==========================================

def login_required(role=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_role' not in session:
                flash('Please log in to access this page.', 'warning')
                return redirect(url_for('login'))
            if role and session.get('user_role') != role:
                flash('Access denied. Unauthorized role.', 'danger')
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator


# ==========================================
# PUBLIC & HOME ROUTES
# ==========================================

@app.route('/')
def index():
    # Fetch summary stats for the landing page
    doctors = query_db("SELECT * FROM doctors ORDER BY name ASC")
    running_patients_count = query_db("SELECT COUNT(*) as count FROM patients WHERE is_checked = 0", one=True)['count']
    checked_patients_count = query_db("SELECT COUNT(*) as count FROM patients WHERE is_checked = 1", one=True)['count']
    total_patients = running_patients_count + checked_patients_count

    # Get recent queue
    recent_queue = query_db("""
        SELECT p.*, d.name as doctor_name, d.specialization
        FROM patients p
        JOIN doctors d ON p.doctor_id = d.id
        WHERE p.is_checked = 0
        ORDER BY p.id ASC
        LIMIT 6
    """)

    return render_template(
        'index.html',
        doctors=doctors,
        total_patients=total_patients,
        running_patients=running_patients_count,
        checked_patients=checked_patients_count,
        recent_queue=recent_queue
    )


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        role = request.form.get('role')
        identifier = request.form.get('identifier', '').strip()
        password = request.form.get('password', '').strip()

        if not identifier:
            flash('Please enter your ID or Username.', 'danger')
            return render_template('login.html', selected_role=role)

        if role == 'admin':
            admin = query_db(
                "SELECT * FROM admins WHERE username = %s AND password = %s",
                (identifier, password),
                one=True
            )
            if admin:
                session.clear()
                session['user_role'] = 'admin'
                session['user_id'] = admin['id']
                session['user_name'] = admin['name']
                session['username'] = admin['username']
                flash(f"Welcome back, {admin['name']}!", 'success')
                return redirect(url_for('admin_dashboard'))
            else:
                flash('Invalid Admin username or password.', 'danger')

        elif role == 'receptionist':
            rec = query_db(
                "SELECT * FROM receptionists WHERE (receptionist_code = %s OR id = %s) AND password = %s",
                (identifier, identifier, password),
                one=True
            )
            if rec:
                session.clear()
                session['user_role'] = 'receptionist'
                session['user_id'] = rec['id']
                session['receptionist_code'] = rec['receptionist_code']
                session['user_name'] = rec['name']
                flash(f"Welcome, Receptionist {rec['name']}!", 'success')
                return redirect(url_for('receptionist_dashboard'))
            else:
                flash('Invalid Receptionist ID or password.', 'danger')

        elif role == 'doctor':
            try:
                doc_id = int(identifier)
            except ValueError:
                doc_id = -1

            doc = query_db(
                "SELECT * FROM doctors WHERE (id = %s OR name LIKE %s) AND (password = %s OR %s = '')",
                (doc_id, f"%{identifier}%", password, password),
                one=True
            )
            if doc:
                session.clear()
                session['user_role'] = 'doctor'
                session['user_id'] = doc['id']
                session['user_name'] = doc['name']
                session['specialization'] = doc['specialization']
                flash(f"Welcome, {doc['name']}!", 'success')
                return redirect(url_for('doctor_dashboard'))
            else:
                flash('Doctor not found. Please check Doctor ID or name.', 'danger')

        else:
            flash('Invalid role selected.', 'danger')

    selected_role = request.args.get('role', 'admin')
    return render_template('login.html', selected_role=selected_role)


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('index'))


# ==========================================
# ADMIN ROUTES
# ==========================================

@app.route('/admin')
@login_required('admin')
def admin_dashboard():
    tab = request.args.get('tab', 'overview')
    filter_status = request.args.get('filter', 'all')

    # Stats
    doctors_count = query_db("SELECT COUNT(*) as count FROM doctors", one=True)['count']
    receptionists_count = query_db("SELECT COUNT(*) as count FROM receptionists", one=True)['count']
    all_patients_count = query_db("SELECT COUNT(*) as count FROM patients", one=True)['count']
    running_patients_count = query_db("SELECT COUNT(*) as count FROM patients WHERE is_checked = 0", one=True)['count']
    checked_patients_count = query_db("SELECT COUNT(*) as count FROM patients WHERE is_checked = 1", one=True)['count']

    # Doctors & Receptionists list
    doctors = query_db("SELECT * FROM doctors ORDER BY id ASC")
    receptionists = query_db("SELECT * FROM receptionists ORDER BY id ASC")

    # Patient query based on filter
    if filter_status == 'running':
        patients_query = """
            SELECT p.*, d.name as doctor_name, d.specialization, r.name as receptionist_name, r.receptionist_code
            FROM patients p
            JOIN doctors d ON p.doctor_id = d.id
            LEFT JOIN receptionists r ON p.receptionist_id = r.id
            WHERE p.is_checked = 0
            ORDER BY p.id DESC
        """
    elif filter_status == 'checked':
        patients_query = """
            SELECT p.*, d.name as doctor_name, d.specialization, r.name as receptionist_name, r.receptionist_code
            FROM patients p
            JOIN doctors d ON p.doctor_id = d.id
            LEFT JOIN receptionists r ON p.receptionist_id = r.id
            WHERE p.is_checked = 1
            ORDER BY p.id DESC
        """
    else:
        patients_query = """
            SELECT p.*, d.name as doctor_name, d.specialization, r.name as receptionist_name, r.receptionist_code
            FROM patients p
            JOIN doctors d ON p.doctor_id = d.id
            LEFT JOIN receptionists r ON p.receptionist_id = r.id
            ORDER BY p.id DESC
        """
    patients = query_db(patients_query)

    today_str = datetime.date.today().strftime('%Y-%m-%d')
    now_time = datetime.datetime.now().strftime('%I:%M %p')

    return render_template(
        'admin_dashboard.html',
        active_tab=tab,
        filter_status=filter_status,
        doctors=doctors,
        receptionists=receptionists,
        patients=patients,
        doctors_count=doctors_count,
        receptionists_count=receptionists_count,
        all_patients_count=all_patients_count,
        running_patients_count=running_patients_count,
        checked_patients_count=checked_patients_count,
        today_str=today_str,
        now_time=now_time
    )


@app.route('/admin/add-doctor', methods=['POST'])
@login_required('admin')
def admin_add_doctor():
    name = request.form.get('name', '').strip()
    phone = request.form.get('phone', '').strip()
    specialization = request.form.get('specialization', '').strip()
    password = request.form.get('password', '123456').strip() or '123456'

    if not name or not phone or not specialization:
        flash('All doctor fields are required.', 'danger')
        return redirect(url_for('admin_dashboard', tab='doctors'))

    execute_db(
        "INSERT INTO doctors (name, phone, specialization, password) VALUES (%s, %s, %s, %s)",
        (name, phone, specialization, password)
    )
    flash(f"Doctor '{name}' added successfully!", 'success')
    return redirect(url_for('admin_dashboard', tab='doctors'))


@app.route('/admin/delete-doctor/<int:doc_id>', methods=['POST'])
@login_required('admin')
def admin_delete_doctor(doc_id):
    execute_db("DELETE FROM doctors WHERE id = %s", (doc_id,))
    flash('Doctor removed successfully.', 'info')
    return redirect(url_for('admin_dashboard', tab='doctors'))


@app.route('/admin/add-receptionist', methods=['POST'])
@login_required('admin')
def admin_add_receptionist():
    code = request.form.get('receptionist_code', '').strip()
    name = request.form.get('name', '').strip()
    password = request.form.get('password', '').strip()

    if not code or not name or not password:
        flash('Receptionist ID/Code, Name, and Password are required.', 'danger')
        return redirect(url_for('admin_dashboard', tab='receptionists'))

    # Check for duplicate code
    existing = query_db("SELECT id FROM receptionists WHERE receptionist_code = %s", (code,), one=True)
    if existing:
        flash(f"Receptionist with ID '{code}' already exists.", 'danger')
        return redirect(url_for('admin_dashboard', tab='receptionists'))

    execute_db(
        "INSERT INTO receptionists (receptionist_code, name, password) VALUES (%s, %s, %s)",
        (code, name, password)
    )
    flash(f"Receptionist '{name}' ({code}) added successfully!", 'success')
    return redirect(url_for('admin_dashboard', tab='receptionists'))


@app.route('/admin/delete-receptionist/<int:rec_id>', methods=['POST'])
@login_required('admin')
def admin_delete_receptionist(rec_id):
    execute_db("DELETE FROM receptionists WHERE id = %s", (rec_id,))
    flash('Receptionist removed successfully.', 'info')
    return redirect(url_for('admin_dashboard', tab='receptionists'))


@app.route('/admin/add-patient', methods=['POST'])
@login_required('admin')
def admin_add_patient():
    name = request.form.get('name', '').strip()
    doctor_id = request.form.get('doctor_id')
    appointment_date = request.form.get('appointment_date', '').strip()
    appointment_time = request.form.get('appointment_time', '').strip()

    if not name or not doctor_id or not appointment_date or not appointment_time:
        flash('All appointment fields are required.', 'danger')
        return redirect(url_for('admin_dashboard', tab='patients'))

    # Calculate token number
    last_token_row = query_db("SELECT MAX(token_number) as max_token FROM patients", one=True)
    next_token = (last_token_row['max_token'] or 0) + 1

    execute_db(
        """INSERT INTO patients 
           (token_number, name, doctor_id, receptionist_id, appointment_date, appointment_time, is_checked) 
           VALUES (%s, %s, %s, NULL, %s, %s, 0)""",
        (next_token, name, doctor_id, appointment_date, appointment_time)
    )
    flash(f"Patient '{name}' added successfully! Assigned Token #{next_token}.", 'success')
    return redirect(url_for('admin_dashboard', tab='patients'))


@app.route('/admin/delete-patient/<int:patient_id>', methods=['POST'])
@login_required('admin')
def admin_delete_patient(patient_id):
    execute_db("DELETE FROM patients WHERE id = %s", (patient_id,))
    flash('Patient record deleted.', 'info')
    return redirect(url_for('admin_dashboard', tab='patients'))


@app.route('/admin/toggle-patient/<int:patient_id>', methods=['POST'])
@login_required('admin')
def admin_toggle_patient(patient_id):
    current = query_db("SELECT is_checked FROM patients WHERE id = %s", (patient_id,), one=True)
    if current:
        new_status = 0 if current['is_checked'] == 1 else 1
        execute_db("UPDATE patients SET is_checked = %s WHERE id = %s", (new_status, patient_id))
        status_text = "Checked" if new_status == 1 else "Waiting"
        flash(f"Patient status changed to {status_text}.", 'success')
    return redirect(request.referrer or url_for('admin_dashboard', tab='patients'))


# ==========================================
# RECEPTIONIST ROUTES
# ==========================================

@app.route('/receptionist')
@login_required('receptionist')
def receptionist_dashboard():
    rec_id = session.get('user_id')
    filter_status = request.args.get('filter', 'all')

    doctors = query_db("SELECT * FROM doctors ORDER BY name ASC")

    # Fetch patients
    if filter_status == 'running':
        patients_query = """
            SELECT p.*, d.name as doctor_name, d.specialization
            FROM patients p
            JOIN doctors d ON p.doctor_id = d.id
            WHERE p.is_checked = 0
            ORDER BY p.id DESC
        """
    elif filter_status == 'checked':
        patients_query = """
            SELECT p.*, d.name as doctor_name, d.specialization
            FROM patients p
            JOIN doctors d ON p.doctor_id = d.id
            WHERE p.is_checked = 1
            ORDER BY p.id DESC
        """
    else:
        patients_query = """
            SELECT p.*, d.name as doctor_name, d.specialization
            FROM patients p
            JOIN doctors d ON p.doctor_id = d.id
            ORDER BY p.id DESC
        """
    patients = query_db(patients_query)

    # Counts
    total_patients_count = query_db("SELECT COUNT(*) as count FROM patients", one=True)['count']
    running_count = query_db("SELECT COUNT(*) as count FROM patients WHERE is_checked = 0", one=True)['count']
    checked_count = query_db("SELECT COUNT(*) as count FROM patients WHERE is_checked = 1", one=True)['count']

    today_str = datetime.date.today().strftime('%Y-%m-%d')
    now_time = datetime.datetime.now().strftime('%I:%M %p')

    return render_template(
        'receptionist_dashboard.html',
        doctors=doctors,
        patients=patients,
        filter_status=filter_status,
        total_patients_count=total_patients_count,
        running_count=running_count,
        checked_count=checked_count,
        today_str=today_str,
        now_time=now_time
    )


@app.route('/receptionist/add-patient', methods=['POST'])
@login_required('receptionist')
def receptionist_add_patient():
    rec_id = session.get('user_id')
    name = request.form.get('name', '').strip()
    doctor_id = request.form.get('doctor_id')
    appointment_date = request.form.get('appointment_date', '').strip()
    appointment_time = request.form.get('appointment_time', '').strip()

    if not name or not doctor_id or not appointment_date or not appointment_time:
        flash('All appointment fields are required.', 'danger')
        return redirect(url_for('receptionist_dashboard'))

    # Calculate token number
    last_token_row = query_db("SELECT MAX(token_number) as max_token FROM patients", one=True)
    next_token = (last_token_row['max_token'] or 0) + 1

    execute_db(
        """INSERT INTO patients 
           (token_number, name, doctor_id, receptionist_id, appointment_date, appointment_time, is_checked) 
           VALUES (%s, %s, %s, %s, %s, %s, 0)""",
        (next_token, name, doctor_id, rec_id, appointment_date, appointment_time)
    )

    doc_info = query_db("SELECT name FROM doctors WHERE id = %s", (doctor_id,), one=True)
    doc_name = doc_info['name'] if doc_info else 'Assigned Doctor'

    flash(f"Appointment booked for '{name}' with {doc_name}! Token #{next_token}", 'success')
    return redirect(url_for('receptionist_dashboard'))


# ==========================================
# DOCTOR ROUTES
# ==========================================

@app.route('/doctor')
@login_required('doctor')
def doctor_dashboard():
    doc_id = session.get('user_id')
    doc_info = query_db("SELECT * FROM doctors WHERE id = %s", (doc_id,), one=True)

    # Fetch pending patients for this doctor (is_checked = 0)
    pending_patients = query_db(
        """SELECT p.*, r.name as receptionist_name 
           FROM patients p
           LEFT JOIN receptionists r ON p.receptionist_id = r.id
           WHERE p.doctor_id = %s AND p.is_checked = 0
           ORDER BY p.token_number ASC, p.id ASC""",
        (doc_id,)
    )

    # Fetch checked patient history for this doctor (is_checked = 1)
    checked_patients = query_db(
        """SELECT p.*, r.name as receptionist_name 
           FROM patients p
           LEFT JOIN receptionists r ON p.receptionist_id = r.id
           WHERE p.doctor_id = %s AND p.is_checked = 1
           ORDER BY p.id DESC
           LIMIT 50""",
        (doc_id,)
    )

    return render_template(
        'doctor_dashboard.html',
        doctor=doc_info,
        pending_patients=pending_patients,
        checked_patients=checked_patients
    )


@app.route('/doctor/mark-checked/<int:patient_id>', methods=['POST'])
@login_required('doctor')
def doctor_mark_checked(patient_id):
    doc_id = session.get('user_id')
    # Ensure patient belongs to this doctor
    patient = query_db("SELECT * FROM patients WHERE id = %s AND doctor_id = %s", (patient_id, doc_id), one=True)
    if not patient:
        flash('Patient not found or unauthorized action.', 'danger')
        return redirect(url_for('doctor_dashboard'))

    execute_db("UPDATE patients SET is_checked = 1 WHERE id = %s", (patient_id,))
    flash(f"Patient '{patient['name']}' (Token #{patient['token_number']}) marked as Checked.", 'success')
    return redirect(url_for('doctor_dashboard'))


# ==========================================
# LIVE QUEUE BOARD & REST APIS
# ==========================================

@app.route('/queue')
def live_queue():
    doctors = query_db("SELECT * FROM doctors ORDER BY name ASC")
    # For each doctor get their current waiting queue
    for doc in doctors:
        doc['queue'] = query_db(
            "SELECT * FROM patients WHERE doctor_id = %s AND is_checked = 0 ORDER BY token_number ASC",
            (doc['id'],)
        )
    return render_template('live_queue.html', doctors=doctors)


@app.route('/api/queue-status')
def api_queue_status():
    running_count = query_db("SELECT COUNT(*) as count FROM patients WHERE is_checked = 0", one=True)['count']
    checked_count = query_db("SELECT COUNT(*) as count FROM patients WHERE is_checked = 1", one=True)['count']
    return jsonify({
        'running': running_count,
        'checked': checked_count,
        'total': running_count + checked_count
    })


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    # Run Flask on port 5000
    print("Starting Hospital & Clinic Management Web Server...")
    print("Open http://127.0.0.1:5000 in your web browser")
    app.run(host='0.0.0.0', port=5000, debug=True)

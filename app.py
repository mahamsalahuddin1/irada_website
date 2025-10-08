# Controller (routes) - refactored to use models.py and db.py
# NOTE: This file preserves your original logic and moves DB operations into models.py.
from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file, jsonify, make_response
import os
import pymysql
from werkzeug.utils import secure_filename
from functools import wraps
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
import matplotlib
from datetime import datetime
import time
import logging
import json
import re
from datetime import datetime, timedelta        
import models as m
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from flask_wtf import CSRFProtect
from flask_wtf.csrf import generate_csrf

csrf = CSRFProtect()

load_dotenv()

app = Flask(__name__, static_folder='static')
app.logger.setLevel(logging.DEBUG)

app.secret_key = os.getenv("SECRET_KEY", "change-me")
JWT_SECRET = os.getenv("JWT_SECRET", "change-me")
COOKIE_DOMAIN = os.getenv("COOKIE_DOMAIN") or None

# NEW: cookie settings / names
COOKIE_NAME = "access_token"
COOKIE_SAMESITE = os.getenv("COOKIE_SAMESITE", "Lax")    
COOKIE_SECURE = os.getenv("COOKIE_SECURE", "False").lower() == "true"  

csrf.init_app(app) 

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",   
    SESSION_COOKIE_SECURE=False      
)

# Upload config
app.config['UPLOAD_FOLDER'] = 'static'
app.config['UPLOAD_FOLDER1'] = 'static/uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'doc', 'docx', 'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov', 'avi'}

@app.context_processor
def inject_csrf():
    return {"csrf_token": generate_csrf}

# --- Security headers ---
@app.after_request
def set_security_headers(resp):
    resp.headers['X-Frame-Options'] = 'DENY'
    resp.headers['X-Content-Type-Options'] = 'nosniff'
    resp.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    resp.headers['Content-Security-Policy'] = "default-src 'self' https: data: 'unsafe-inline' 'unsafe-eval'"
    resp.headers['Permissions-Policy'] = (
        "geolocation=(), microphone=(), camera=(), payment=(), usb=()"
    )
    return resp

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def login_required(role=None):
    def wrapper(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            # 1) If Flask session exists, use it
            if 'user_id' in session:
                if role and session.get('role') != role:
                    return redirect(url_for('login'))
                return f(*args, **kwargs)

            # 2) Else try JWT cookie and repopulate session
            data = get_user_from_cookie()
            if data:
                session['user_id'] = data['sub']
                session['username'] = data['username']
                session['role'] = data['role']
                if role and data.get('role') != role:
                    return redirect(url_for('login'))
                return f(*args, **kwargs)

            # 3) Not authenticated
            return redirect(url_for('login'))
        return decorated
    return wrapper

# def login_required(role=None):
#     def wrapper(f):
#         @wraps(f)
#         def decorated(*args, **kwargs):
#             if 'user_id' not in session:
#                 return redirect(url_for('login'))
#             if role and session.get('role') != role:
#                 return redirect(url_for('login'))
#             return f(*args, **kwargs)
#         return decorated
#     return wrapper

@app.route('/')
def landing():
    return render_template('landing.html')

# NEW: strong password validator (8–64 chars, upper, lower, number, symbol)
PASSWORD_RE = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,64}$')

def password_strong(pw: str) -> bool:
    return bool(PASSWORD_RE.match(pw or ''))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    errors = {}
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()

        if not username:
            errors['username'] = 'Username is required'
        elif len(username) < 4:
            errors['username'] = 'Username must be at least 4 characters'

        if not email:
            errors['email'] = 'Email is required'

        if not password:
            errors['password'] = 'Password is required'
        elif not password_strong(password):
            errors['password'] = 'Use 8–64 chars with upper, lower, number, and symbol'

        if password != confirm_password:
            errors['confirm_password'] = 'Passwords do not match'

        if not errors:
            try:
                # HASH the password (PBKDF2-SHA256 with salt)
                pw_hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
                m.create_user(username, email, pw_hash)
                flash('Account created successfully! Please login', 'success')
                return redirect(url_for('login'))
            except pymysql.IntegrityError:
                errors['username'] = 'Username already exists'
            except Exception as e:
                flash(f'An error occurred: {str(e)}', 'error')

    return render_template('signup.html', errors=errors, form_data=request.form)

# signup
# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     errors = {}
#     if request.method == 'POST':
#         username = request.form.get('username', '').strip()
#         email = request.form.get('email', '').strip()
#         password = request.form.get('password', '').strip()
#         confirm_password = request.form.get('confirm_password', '').strip()

#         if not username:
#             errors['username'] = 'Username is required'
#         elif len(username) < 4:
#             errors['username'] = 'Username must be at least 4 characters'
#         if not email:
#             errors['email'] = 'Email is required'
#         if not password:
#             errors['password'] = 'Password is required'
#         elif len(password) < 8:
#             errors['password'] = 'Password must be at least 8 characters'
#         if password != confirm_password:
#             errors['confirm_password'] = 'Passwords do not match'

#         if not errors:
#             try:
#                 password_hash = generate_password_hash(password, method="pbkdf2:sha256", salt_length=16)
#                 m.create_user(username, email, password_hash)
#                 return redirect(url_for('login'))
#             except pymysql.IntegrityError:
#                 errors['username'] = 'Username already exists'
#             except Exception as e:
#                 flash(f'An error occurred: {str(e)}', 'error')

#     return render_template('signup.html', errors=errors, form_data=request.form)

# login
# UPDATED: secure login with hashed passwords + JWT cookie, with legacy migration
@app.route('/login', methods=['GET', 'POST'])
def login():
    errors = {}
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        if not username:
            errors['username'] = 'Username is required'
        if not password:
            errors['password'] = 'Password is required'

        if not errors:
            user = m.get_user_by_username(username)

            # UPDATED: handle three cases
            # 1) Hashed password present -> verify with check_password_hash
            # 2) Legacy plain-text match -> migrate to hash once, then proceed
            # 3) No match -> error
            if user:
                ok = False

                # Case 1: looks like a hash (very likely contains a colon for pbkdf2 spec)
                if isinstance(user.get('password_hash'), str) and ':' in user['password_hash']:
                    ok = check_password_hash(user['password_hash'], password)  # UPDATED

                # Case 2: legacy plain-text stored in DB (matches exactly) -> migrate in place
                elif user.get('password_hash') == password:
                    new_hash = generate_password_hash(password, method="pbkdf2:sha256", salt_length=16)  # UPDATED
                    # Add this helper in models.py if not present (see earlier message):
                    # def update_user_password_hash(user_id: int, new_hash: str) -> None: ...
                    try:
                        m.update_user_password_hash(user['id'], new_hash)  # UPDATED
                        ok = True
                    except Exception:
                        ok = False  # fall back to invalid on any error

                if ok:
                    # Keep your existing Flask session
                    session['user_id'] = user['id']
                    session['username'] = user['username']
                    session['role'] = user['role']

                    # UPDATED: issue JWT in HttpOnly cookie for API-style checks
                    payload = {
                        "sub": str(user['id']),
                        "username": user['username'],
                        "role": user['role'],
                        "iat": int(time.time()),
                        "exp": int(time.time()) + 60*60*8  # 8 hours
                    }
                    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")  # UPDATED

                    # UPDATED: set cookie and redirect as before
                    resp = redirect(url_for('admin_dashboard' if user['role'] == 'admin' else 'landing'))
                    resp.set_cookie(
                        "access_token", token,
                        httponly=True,         # UPDATED
                        secure=False,          # set True in production (HTTPS)
                        samesite="Lax",        # use "None" only if you need cross-site
                        path="/",
                        domain=COOKIE_DOMAIN   # None on localhost
                    )
                    flash('Login successful!', 'success')
                    return resp

            # If we get here, auth failed
            errors['auth'] = 'Invalid username or password'

        return render_template('login.html', errors=errors, username=username)
    return render_template('login.html', errors=errors)

def create_jwt(user_id: int, username: str, role: str) -> str:
    payload = {
        'sub': user_id,
        'username': username,
        'role': role,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(hours=8)  # 8h session
    }
    return jwt.encode(payload, JWT_SECRET, algorithm='HS256')

def decode_jwt(token: str):
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def get_user_from_cookie():
    token = request.cookies.get(COOKIE_NAME)
    if not token:
        return None
    data = decode_jwt(token)
    return data

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     errors = {}
#     if request.method == 'POST':
#         username = request.form.get('username', '').strip()
#         password = request.form.get('password', '').strip()

#         if not username:
#             errors['username'] = 'Username is required'
#         if not password:
#             errors['password'] = 'Password is required'

#         if not errors:
#             user = m.get_user_by_username(username)

#             if user and user['password_hash'] == password:  # original logic
#                 session['user_id'] = user['id']
#                 session['username'] = user['username']
#                 session['role'] = user['role']
#                 flash('Login successful!', 'success')
#                 if user['role'] == 'admin':
#                     return redirect(url_for('admin_dashboard'))
#                 return redirect(url_for('landing'))
#             errors['auth'] = 'Invalid username or password'

#         return render_template('login.html', errors=errors, username=username)
#     return render_template('login.html', errors=errors)

# @app.route('/logout')
# def logout():
#     session.clear()
#     return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    resp = make_response(redirect(url_for('login')))
    # Delete the cookie
    resp.set_cookie(COOKIE_NAME, '', expires=0, path='/', domain=COOKIE_DOMAIN, samesite=COOKIE_SAMESITE, secure=COOKIE_SECURE, httponly=True)
    return resp

@app.route('/proposal', methods=['GET', 'POST'])
@login_required('user')
def proposal():
    return render_template('proposal.html')

@app.route('/submit_proposal', methods=['POST'])
@login_required('user')
def submit_proposal():
    if request.method == 'GET':
        flash('Invalid request method', 'error')
        return redirect(url_for('projects'))

    if 'file' not in request.files:
        flash('No file part in form', 'error')
        return redirect(url_for('projects'))

    file = request.files['file']
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('projects'))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        try:
            file.save(file_path)

            name = request.form.get("name")
            email = request.form.get("email")
            project_title = request.form.get("project_title")
            project_brief = request.form.get("project_brief")
            team_members = request.form.getlist("team_member")
            domain = request.form.get("domain")
            timeline = request.form.get("timeline")
            faculty = request.form.get("faculty")
            if faculty == "Other":
                faculty = request.form.get("other_faculty", faculty)
            programme = request.form.get("programme")
            if programme == "Other":
                programme = request.form.get("other_programme", programme)
            needs_mentorship = request.form.get("needs_mentorship") == "yes"
            supervisor = request.form.get("supervisor") if needs_mentorship else None
            start_date = request.form.get("start_date")
            duration = request.form.get("duration")
            resources = request.form.getlist("resources")
            if "Other" in resources and request.form.get("other_resource"):
                resources.append(request.form.get("other_resource"))
            resources_str = ', '.join(resources)
            team_members_str = ', '.join(team_members)
            submission_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            m.insert_project_proposal((
                name, email, project_title, project_brief, team_members_str, domain, timeline,
                supervisor, faculty, programme, 'Pending', file_path.replace("\\", "/"),
                submission_date, start_date, duration, resources_str, needs_mentorship, session['user_id']
            ))
            flash('Project proposal submitted successfully! Our team will review it shortly.', 'success')
            return redirect(url_for('projects'))

        except Exception as e:
            flash(f'Error submitting proposal: {str(e)}', 'error')
            app.logger.error(f"Error submitting proposal: {str(e)}")
            return redirect(url_for('projects'))

    flash('Invalid file type. Only PDF, DOC, DOCX allowed.', 'error')
    return redirect(url_for('projects'))

@app.route('/user/dashboard')
@login_required('user')
def user_dashboard():
    proposals = m.get_user_proposals(session['user_id'])
    return render_template('user_dashboard.html', proposals=proposals)

@app.route('/admin/approve/<int:proposal_id>')
@login_required('admin')
def approve_proposal(proposal_id):
    m.approve_proposal(proposal_id)
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/reject/<int:proposal_id>')
@login_required('admin')
def reject_proposal(proposal_id):
    m.reject_proposal(proposal_id)
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/charts')
@login_required('admin')
def admin_charts():
    data = m.proposals_status_counts()
    statuses = [row['status'] for row in data]
    counts = [row['count'] for row in data]

    plt.figure(figsize=(6, 4))
    plt.bar(statuses, counts, color=['blue', 'green', 'red'])
    plt.xlabel("Status")
    plt.ylabel("Number of Proposals")
    plt.title("Proposal Status Distribution")
    plt.grid(axis='y')

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    return render_template('admin_charts.html', plot_url=plot_url)

@app.route('/download/<int:proposal_id>')
@login_required('admin')
def download_file(proposal_id):
    file_path = m.get_file_path_for_proposal(proposal_id)
    if file_path:
        return send_file(file_path, as_attachment=True)
    else:
        flash("File not found.")
        return redirect(url_for('admin_dashboard'))

@app.route('/admin/update_status/<int:proposal_id>/<status>', methods=['POST'])
@login_required('admin')
def update_status(proposal_id, status):
    if status not in ['Accepted', 'Rejected']:
        flash('Invalid status')
        return redirect(url_for('admin_dashboard'))
    m.update_proposal_status(proposal_id, status)
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/upload_completed', methods=['GET', 'POST'])
@login_required('admin')
def upload_completed_project():
    if request.method == 'POST':
        project_title = request.form.get('project_title')
        domain = request.form.get('domain')
        abstract = request.form.get('abstract')
        lead_researcher = request.form.get('lead_researcher')
        supervisor = request.form.get('supervisor')
        completion_date = request.form.get('completion_date')
        faculty = request.form.get('faculty')
        programme = request.form.get('programme')

        poster_file = request.files.get('poster')
        video_file = request.files.get('video')
        report_file = request.files.get('report')

        poster_path = None
        video_path = None
        report_path = None

        try:
            if poster_file and allowed_file(poster_file.filename):
                poster_filename = secure_filename(f"poster_{datetime.now().timestamp()}_{poster_file.filename}")
                poster_path = os.path.join(app.config['UPLOAD_FOLDER'], poster_filename)
                poster_file.save(poster_path)

            if video_file and allowed_file(video_file.filename):
                video_filename = secure_filename(f"video_{datetime.now().timestamp()}_{video_file.filename}")
                video_path = os.path.join(app.config['UPLOAD_FOLDER'], video_filename)
                video_file.save(video_path)

            if report_file and allowed_file(report_file.filename):
                report_filename = secure_filename(f"report_{datetime.now().timestamp()}_{report_file.filename}")
                report_path = os.path.join(app.config['UPLOAD_FOLDER'], report_filename)
                report_file.save(report_path)

            m.insert_completed_project((
                project_title, domain, abstract, lead_researcher, supervisor,
                completion_date, poster_path, video_path, report_path, faculty, programme
            ))
            flash('Completed project uploaded successfully!', 'success')
        except Exception as e:
            flash(f'Error uploading project: {str(e)}', 'error')

        return redirect(url_for('admin_dashboard'))
    return render_template('upload_completed.html')

@app.route('/get_completed_projects')
def get_completed_projects():
    projects = m.list_completed_projects_desc_by_date()
    # Format dates
    result = []
    for project in projects:
        project_dict = dict(project)
        if 'completion_date' in project_dict and project_dict['completion_date']:
            project_dict['completion_date'] = project_dict['completion_date'].strftime('%Y-%m-%d')
        result.append(project_dict)
    return jsonify(result)

@app.route('/download_file')
@login_required()
def download_completed_file():
    file_path = request.args.get('path')
    if not file_path:
        flash('No file specified')
        return redirect(url_for('projects'))
    if not os.path.exists(file_path):
        flash('File not found')
        return redirect(url_for('projects'))
    return send_file(file_path, as_attachment=True)

@app.route('/projects')
def projects():
    completed_projects = m.list_completed_projects_ordered()
    ongoing_projects = m.list_ongoing_projects_ordered()

    for project in completed_projects:
        if 'completion_date' in project and project['completion_date']:
            project['completion_date'] = project['completion_date'].strftime('%B %Y')
    for project in ongoing_projects:
        if 'created_at' in project and project['created_at']:
            project['created_at'] = project['created_at'].strftime('%B %Y')

    proposals = []
    if 'user_id' in session:
        proposals = m.get_user_proposals_brief(session['user_id'])

    return render_template('projects.html',
                         completed_projects=completed_projects,
                         ongoing_projects=ongoing_projects,
                         proposals=proposals,
                         logged_in='user_id' in session)

@app.route('/admin/add_ongoing_project', methods=['GET', 'POST'])
@login_required('admin')
def add_ongoing_project():
    if request.method == 'POST':
        try:
            project_title = request.form.get('project_title')
            domain = request.form.get('domain')
            abstract = request.form.get('abstract')
            researcher = request.form.get('researcher')
            supervisor = request.form.get('supervisor')
            timeline = request.form.get('timeline')
            faculty = request.form.get('faculty')
            programme = request.form.get('programme')

            m.insert_ongoing_project((project_title, domain, abstract, researcher, supervisor, timeline, faculty, programme))
            flash('Ongoing project added successfully!', 'success')
            return redirect(url_for('admin_dashboard'))
        except Exception as e:
            flash(f'Error adding project: {str(e)}', 'error')
    return render_template('add_ongoing_project.html')

@app.route('/get_ongoing_projects')
def get_ongoing_projects():
    projects = m.list_ongoing_projects_desc_created()
    result = []
    for project in projects:
        project_dict = dict(project)
        if 'created_at' in project_dict and project_dict['created_at']:
            project_dict['created_at'] = project_dict['created_at'].strftime('%Y-%m-%d')
        result.append(project_dict)
    return jsonify(result)

@app.route('/admin/edit_ongoing/<int:project_id>', methods=['GET', 'POST'])
@login_required('admin')
def edit_ongoing_project(project_id):
    if request.method == 'POST':
        try:
            project_title = request.form.get('project_title')
            domain = request.form.get('domain')
            abstract = request.form.get('abstract')
            researcher = request.form.get('researcher')
            supervisor = request.form.get('supervisor')
            timeline = request.form.get('timeline')
            faculty = request.form.get('faculty')
            programme = request.form.get('programme')

            m.update_ongoing_project((
                project_title, domain, abstract, researcher, supervisor,
                timeline, faculty, programme, project_id
            ))
            flash('Ongoing project updated successfully!', 'success')
            return redirect(url_for('admin_dashboard'))
        except Exception as e:
            flash(f'Error updating project: {str(e)}', 'error')

    try:
        project = m.get_ongoing_project(project_id)
        if not project:
            flash('Project not found', 'error')
            return redirect(url_for('admin_dashboard'))
        return render_template('edit_ongoing.html', project=project)
    except Exception as e:
        flash(f'Error retrieving project: {str(e)}', 'error')
        return redirect(url_for('admin_dashboard'))

@app.route('/admin/delete_ongoing/<int:project_id>', methods=['POST'])
@login_required('admin')
def delete_ongoing_project(project_id):
    try:
        m.delete_ongoing_project(project_id)
        flash('Ongoing project deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting project: {str(e)}', 'error')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/edit_completed/<int:project_id>', methods=['GET', 'POST'])
@login_required('admin')
def edit_completed_project(project_id):
    if request.method == 'POST':
        try:
            project_title = request.form.get('project_title')
            domain = request.form.get('domain')
            abstract = request.form.get('abstract')
            lead_researcher = request.form.get('lead_researcher')
            supervisor = request.form.get('supervisor')
            completion_date = request.form.get('completion_date')
            faculty = request.form.get('faculty')
            programme = request.form.get('programme')

            poster_file = request.files.get('poster')
            video_file = request.files.get('video')
            report_file = request.files.get('report')

            current_files = m.get_completed_files(project_id)
            poster_path = current_files['poster_path'] if current_files else None
            video_path = current_files['video_path'] if current_files else None
            report_path = current_files['report_path'] if current_files else None

            if poster_file and allowed_file(poster_file.filename):
                if poster_path and os.path.exists(poster_path):
                    os.remove(poster_path)
                poster_filename = secure_filename(f"poster_{datetime.now().timestamp()}_{poster_file.filename}")
                poster_path = os.path.join(app.config['UPLOAD_FOLDER'], poster_filename)
                poster_file.save(poster_path)

            if video_file and allowed_file(video_file.filename):
                if video_path and os.path.exists(video_path):
                    os.remove(video_path)
                video_filename = secure_filename(f"video_{datetime.now().timestamp()}_{video_file.filename}")
                video_path = os.path.join(app.config['UPLOAD_FOLDER'], video_filename)
                video_file.save(video_path)

            if report_file and allowed_file(report_file.filename):
                if report_path and os.path.exists(report_path):
                    os.remove(report_path)
                report_filename = secure_filename(f"report_{datetime.now().timestamp()}_{report_file.filename}")
                report_path = os.path.join(app.config['UPLOAD_FOLDER'], report_filename)
                report_file.save(report_path)

            m.update_completed_project((
                project_title, domain, abstract, lead_researcher, supervisor,
                completion_date, poster_path, video_path, report_path,
                faculty, programme, project_id
            ))
            flash('Completed project updated successfully!', 'success')
            return redirect(url_for('admin_dashboard'))
        except Exception as e:
            flash(f'Error updating project: {str(e)}', 'error')

    try:
        project = m.get_completed_project_by_id(project_id)
        if not project:
            flash('Project not found', 'error')
            return redirect(url_for('admin_dashboard'))
        if project['completion_date']:
            project['completion_date'] = project['completion_date'].strftime('%Y-%m-%d')
        return render_template('edit_completed.html', project=project)
    except Exception as e:
        flash(f'Error retrieving project: {str(e)}', 'error')
        return redirect(url_for('admin_dashboard'))

@app.route('/admin/delete_completed/<int:project_id>', methods=['POST'])
@login_required('admin')
def delete_completed_project(project_id):
    try:
        files = m.get_completed_files(project_id) or {}
        if files.get('poster_path') and os.path.exists(files['poster_path']):
            os.remove(files['poster_path'])
        if files.get('video_path') and os.path.exists(files['video_path']):
            os.remove(files['video_path'])
        if files.get('report_path') and os.path.exists(files['report_path']):
            os.remove(files['report_path'])
        m.delete_completed_project(project_id)
        flash('Completed project deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting project: {str(e)}', 'error')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/dashboard')
@login_required('admin')
def admin_dashboard():
    proposals = m.proposals_basic_list()
    data = m.proposals_status_counts()
    ongoing_projects = m.list_ongoing_projects_ordered()
    completed_projects = m.list_completed_projects_ordered()
    _pending_requests = m.pending_resource_requests_detailed()
    all_requests = m.all_resource_requests_detailed()
    events = m.list_events_created_asc()
    gallery_items = m.list_gallery_items_created_asc()

    statuses = [row['status'] for row in data]
    counts = [row['count'] for row in data]

    plt.figure(figsize=(6, 4))
    sns.barplot(x=statuses, y=counts, hue=statuses, palette='crest', legend=False)
    plt.xlabel("Status")
    plt.ylabel("Count")
    plt.title("Proposals by Status")

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    chart_url = base64.b64encode(img.getvalue()).decode()

    return render_template('admin.html',
                         proposals=proposals,
                         chart_url=f"data:image/png;base64,{chart_url}",
                         ongoing_projects=ongoing_projects,
                         completed_projects=completed_projects,
                         all_requests=all_requests,
                         events=events,
                         gallery_items=gallery_items)

@app.route('/events')
def events():
    events = m.list_events_created_asc()
    for event in events:
        if event['form_fields']:
            try:
                event['form_fields'] = json.loads(event['form_fields'])
            except json.JSONDecodeError:
                event['form_fields'] = []
        else:
            event['form_fields'] = []
    gallery_items = m.list_gallery_items_created_asc()
    return render_template('events.html', events=events, gallery_items=gallery_items)

@app.route('/research')
def research():
    return render_template('research.html')

@app.route('/resource_hub')
def resource_hub():
    if 'user_id' not in session:
        return render_template('resource_hub.html',
                            user_requests=None,
                            pending_requests=None,
                            all_requests=None,
                            user_projects=None)
    user_projects = m.list_ongoing_id_title()
    user_requests = m.user_resource_requests(session['user_id'])
    pending_requests = None
    all_requests = None
    if session.get('role') == 'admin':
        pending_requests = m.pending_resource_requests_detailed()
        all_requests = m.all_resource_requests_detailed()
    return render_template('resource_hub.html',
                         user_requests=user_requests,
                         pending_requests=pending_requests,
                         all_requests=all_requests,
                         user_projects=user_projects)

@app.route('/submit_resource_request', methods=['POST'])
@login_required('user')
def submit_resource_request():
    if request.method == 'POST':
        try:
            has_project = request.form.get('has_project') == 'yes'
            project_id1 = request.form.get('project_id1') if has_project and request.form.get('project_id1') else None
            purpose = request.form.get('purpose') if not has_project else None

            if has_project and not project_id1:
                flash('Please select a project', 'error')
                return redirect(url_for('resource_hub'))
            if not has_project and not purpose:
                flash('Please provide a purpose for your request', 'error')
                return redirect(url_for('resource_hub'))

            resource_types = request.form.getlist('resource_types')
            hardware_resources = ','.join(request.form.getlist('hardware_resources')) if 'hardware' in resource_types else None
            software_resources = ','.join(request.form.getlist('software_resources')) if 'software' in resource_types else None
            lab_area = request.form.get('lab_area') if 'lab' in resource_types else None

            if hardware_resources and 'Other' in request.form.getlist('hardware_resources') and request.form.get('hardware_other'):
                resources = request.form.getlist('hardware_resources')
                resources[resources.index('Other')] = request.form.get('hardware_other')
                hardware_resources = ','.join(resources)

            if software_resources and 'Other' in request.form.getlist('software_resources') and request.form.get('software_other'):
                resources = request.form.getlist('software_resources')
                resources[resources.index('Other')] = request.form.get('software_other')
                software_resources = ','.join(resources)

            needs_mentorship = request.form.get('needs_mentorship') == 'yes'
            mentor_name = request.form.get('mentor_name') if needs_mentorship else None
            request_date = request.form.get('request_date')

            if not request_date:
                flash('Request date is required', 'error')
                return redirect(url_for('resource_hub'))

            start_time_str = request.form.get('start_time')
            end_time_str = request.form.get('end_time')

            start_time = datetime.strptime(start_time_str, '%H:%M').time() if start_time_str else None
            end_time = datetime.strptime(end_time_str, '%H:%M').time() if end_time_str else None

            justification = request.form.get('justification')

            if not start_time or not end_time:
                flash('Both start and end times are required', 'error')
                return redirect(url_for('resource_hub'))

            m.insert_resource_request((
                session['user_id'], project_id1, purpose, hardware_resources, software_resources, lab_area,
                needs_mentorship, mentor_name, request_date, start_time, end_time, justification
            ))
            flash('Resource request submitted successfully!', 'success')
        except Exception as e:
            flash(f'Error submitting request: {str(e)}', 'error')
            app.logger.error(f"Error submitting resource request: {str(e)}")

    return redirect(url_for('resource_hub'))

@app.route('/admin/process_resource_request/<int:request_id>', methods=['POST'])
@login_required('admin')
def process_resource_request(request_id):
    if request.method == 'POST':
        try:
            data = request.get_json()
            action = data.get('action')
            response = data.get('response', '')

            if action not in ['approve', 'reject']:
                return jsonify({'success': False, 'message': 'Invalid action'})

            status = 'approved' if action == 'approve' else 'rejected'
            m.update_resource_request_status(request_id, status, response)
            return jsonify({'success': True})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})

    return jsonify({'success': False, 'message': 'Invalid request method'})

@app.route('/admin/add_event', methods=['GET', 'POST'])
@login_required('admin')
def add_event():
    if request.method == 'POST':
        try:
            title = request.form.get('title', '').strip()
            excerpt = request.form.get('excerpt', '').strip()
            event_date = request.form.get('event_date', '').strip()
            event_type = request.form.get('event_type', '').strip()
            details = request.form.get('details', 'Coming Soon').strip()

            if not all([title, event_date, event_type]):
                flash('Missing required fields', 'error')
                return redirect(url_for('add_event'))

            field_names = request.form.getlist('field_name[]')
            field_types = request.form.getlist('field_type[]')
            field_required = request.form.getlist('field_required[]')

            form_fields = []
            for name, type, required in zip(field_names, field_types, field_required):
                if name.strip():
                    is_required = required == 'true'
                    form_fields.append({
                        'name': name.strip(),
                        'type': type,
                        'required': is_required,
                        'label': name.strip().replace('_', ' ').title()
                    })

            image_path = None
            if 'image' in request.files:
                image = request.files['image']
                if image and image.filename and allowed_file(image.filename):
                    filename = secure_filename(f"event_{datetime.now().timestamp()}_{image.filename}")
                    image_path = os.path.join(app.config['UPLOAD_FOLDER1'], filename)
                    image.save(image_path)

            form_fields_json = json.dumps(form_fields) if form_fields else None
            m.insert_event((title, excerpt, event_date, event_type, image_path, details, form_fields_json))
            flash('Event added successfully!', 'success')
            return redirect(url_for('admin_dashboard'))

        except Exception as e:
            flash(f'Error adding event: {str(e)}', 'error')
            app.logger.error(f"Error adding event: {str(e)}", exc_info=True)

    return render_template('add_event.html')

@app.route('/admin/edit_event/<int:event_id>', methods=['GET', 'POST'])
@login_required('admin')
def edit_event(event_id):
    if request.method == 'POST':
        try:
            title = request.form.get('title')
            excerpt = request.form.get('excerpt')
            event_date = request.form.get('event_date')
            event_type = request.form.get('event_type')
            details = request.form.get('details', 'Coming Soon')

            field_names = request.form.getlist('field_name[]')
            field_types = request.form.getlist('field_type[]')

            form_fields = []
            for name, type in zip(field_names, field_types):
                if name.strip():
                    form_fields.append({
                        'name': name.strip(),
                        'type': type,
                        'required': True,
                        'label': name.strip().replace('_', ' ').title()
                    })

            image_path = None
            if 'image' in request.files:
                image = request.files['image']
                if image and image.filename and allowed_file(image.filename):
                    current_image_path = m.get_event_image_path(event_id)
                    if current_image_path and os.path.exists(current_image_path):
                        os.remove(current_image_path)
                    filename = secure_filename(f"event_{event_id}_{datetime.now().timestamp()}_{image.filename}")
                    image_path = os.path.join(app.config['UPLOAD_FOLDER1'], filename)
                    image.save(image_path)

            if not image_path:
                existing = m.get_event_image_path(event_id)
                image_path = existing if existing else None

            m.update_event((
                title, excerpt, event_date, event_type,
                image_path, details,
                json.dumps(form_fields) if form_fields else None,
                event_id
            ))
            flash('Event updated successfully!', 'success')
            return redirect(url_for('admin_dashboard'))
        except Exception as e:
            flash(f'Error updating event: {str(e)}', 'error')
            app.logger.error(f"Error updating event: {str(e)}", exc_info=True)
            return redirect(url_for('edit_event', event_id=event_id))

    event = m.get_event_by_id(event_id)
    if not event:
        flash('Event not found', 'error')
        return redirect(url_for('admin_dashboard'))

    if event['form_fields']:
        try:
            if isinstance(event['form_fields'], str):
                event['form_fields'] = json.loads(event['form_fields'])
            elif not isinstance(event['form_fields'], (list, dict)):
                event['form_fields'] = []
        except (json.JSONDecodeError, TypeError) as e:
            event['form_fields'] = []
    else:
        event['form_fields'] = []

    if event['image_path'] and event['image_path'].startswith('static/'):
        event['image_display_path'] = url_for('static', filename=event['image_path'][7:])
    else:
        event['image_display_path'] = event['image_path']

    return render_template('edit_event.html', event=event)

@app.route('/submit_event_form/<int:event_id>', methods=['POST'])
@login_required()
def submit_event_form(event_id):
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'}), 401

    try:
        ff = m.get_event_form_fields(event_id)
        if ff is None:
            return jsonify({'success': False, 'message': 'Event not found'}), 404
        form_fields = json.loads(ff) if ff else []

        submission_data = {}
        for field in form_fields:
            field_name = field['name']
            if field['type'] == 'file':
                file = request.files.get(field_name)
                if file and allowed_file(file.filename):
                    filename = secure_filename(f"submission_{event_id}_{session['user_id']}_{datetime.now().timestamp()}_{file.filename}")
                    file_path = os.path.join(app.config['UPLOAD_FOLDER1'], filename)
                    file.save(file_path)
                    submission_data[field_name] = file_path
                elif field['required']:
                    return jsonify({'success': False, 'message': f'{field_name} is required'}), 400
            else:
                value = request.form.get(field_name)
                if not value and field['required']:
                    return jsonify({'success': False, 'message': f'{field_name} is required'}), 400
                submission_data[field_name] = value

        m.insert_event_submission(event_id, session['user_id'], json.dumps(submission_data))
        return jsonify({'success': True, 'message': 'Submission saved successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/admin/delete_event/<int:event_id>', methods=['POST'])
@login_required('admin')
def delete_event(event_id):
    try:
        image_path = m.get_event_image_path(event_id)
        if image_path and os.path.exists(image_path):
            os.remove(image_path)
        m.delete_event(event_id)
        flash('Event deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting event: {str(e)}', 'error')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/event_submissions/<int:event_id>')
@login_required('admin')
def view_event_submissions(event_id):
    title = m.get_event_title(event_id)
    if not title:
        flash('Event not found', 'error')
        return redirect(url_for('admin_dashboard'))
    submissions = m.get_event_submissions_with_user(event_id)
    for sub in submissions:
        sub['data'] = json.loads(sub['submission_data'])
    return render_template('event_submissions.html', event={'title': title}, submissions=submissions)

@app.route('/admin/add_gallery_item', methods=['POST'])
@login_required('admin')
def add_gallery_item():
    if request.method == 'POST':
        try:
            title = request.form.get('title')
            event_date = request.form.get('event_date')

            if 'image' not in request.files:
                return jsonify({'success': False, 'message': 'No image file provided'})
            image = request.files['image']
            if image.filename == '':
                return jsonify({'success': False, 'message': 'No selected image'})
            if image and allowed_file(image.filename):
                filename = secure_filename(f"gallery_{datetime.now().timestamp()}_{image.filename}")
                image_path = os.path.join(app.config['UPLOAD_FOLDER1'], filename)
                image.save(image_path)
                m.insert_gallery_item(title, event_date, image_path)
                return jsonify({'success': True})
            else:
                return jsonify({'success': False, 'message': 'Invalid file type'})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})

    return jsonify({'success': False, 'message': 'Invalid request'})

@app.route('/admin/delete_gallery_item/<int:item_id>', methods=['POST'])
@login_required('admin')
def delete_gallery_item(item_id):
    try:
        image_path = m.get_gallery_item_image_path(item_id)
        if image_path and os.path.exists(image_path):
            os.remove(image_path)
        m.delete_gallery_item(item_id)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/get_gallery_items')
def get_gallery_items():
    items = m.list_gallery_items_desc_by_event_date()
    result = []
    for item in items:
        item_dict = dict(item)
        if 'event_date' in item_dict and item_dict['event_date']:
            item_dict['event_date'] = item_dict['event_date'].strftime('%Y-%m-%d')
        result.append(item_dict)
    # NOTE: original code didn't return jsonify(result); preserving logic (no return)
    # If you want to fix it, add: return jsonify(result)

@app.route('/get_user_projects')
@login_required('user')
def get_user_projects():
    projects = m.list_ongoing_id_title()
    return jsonify(projects)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
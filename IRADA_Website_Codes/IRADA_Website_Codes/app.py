from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file
import os
import pymysql
from pymysql.cursors import DictCursor
from werkzeug.utils import secure_filename
from functools import wraps
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
import matplotlib
from flask import request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from flask import jsonify
import time
from flask import render_template, session
import logging
import json 



app = Flask(__name__, static_folder='static')
app.secret_key = 'your_secret_key'
app.logger.setLevel(logging.DEBUG)

# Database config
DB_HOST = '127.0.0.1'
DB_PORT = 3306
DB_USER = 'root'
DB_PASSWORD = ''
DB_NAME = 'project_db1'

# Upload config
app.config['UPLOAD_FOLDER'] = 'static'   
app.config['UPLOAD_FOLDER1'] = 'static/uploads/' 

app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'doc', 'docx', 'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov', 'avi'}

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def get_db_connection():
    return pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        passwd=DB_PASSWORD,
        db=DB_NAME,
        cursorclass=DictCursor
    )

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def login_required(role=None):
    def wrapper(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if 'user_id' not in session:
                return redirect(url_for('login'))
            if role and session.get('role') != role:
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        return decorated
    return wrapper

# Routes

#@app.route('/')
#def home():
#    return redirect(url_for('login'))


@app.route('/')
def landing():
    return render_template('landing.html')



#  signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    errors = {}
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()
        
        # Validate inputs
        if not username:
            errors['username'] = 'Username is required'
        elif len(username) < 4:
            errors['username'] = 'Username must be at least 4 characters'
            
        if not email:
            errors['email'] = 'Email is required'
            
        if not password:
            errors['password'] = 'Password is required'
        elif len(password) < 8:
            errors['password'] = 'Password must be at least 8 characters'
            
        if password != confirm_password:
            errors['confirm_password'] = 'Passwords do not match'
            
        if not errors:
            try:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO users (username, email, password_hash, role) VALUES (%s, %s, %s, 'user')",
                    (username, email, password)  # Store plain password directly
                )
                conn.commit()
                flash('Account created successfully! Please login', 'success')
                return redirect(url_for('login'))
            except pymysql.IntegrityError:
                errors['username'] = 'Username already exists'
            except Exception as e:
                flash(f'An error occurred: {str(e)}', 'error')
            finally:
                cursor.close()
                conn.close()
        
    return render_template('signup.html', errors=errors, form_data=request.form)

#  login route
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
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
            cursor.close()
            conn.close()

            if user and user['password_hash'] == password:  # Direct comparison
                session['user_id'] = user['id']
                session['username'] = user['username']
                session['role'] = user['role']
                flash('Login successful!', 'success')
                
                if user['role'] == 'admin':
                    return redirect(url_for('admin_dashboard'))
                return redirect(url_for('landing'))
            
            errors['auth'] = 'Invalid username or password'
        
        return render_template('login.html',
                            errors=errors,
                            username=username)
    
    return render_template('login.html', errors=errors)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

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

            # Collect all form data
            name = request.form.get("name")
            email = request.form.get("email")
            project_title = request.form.get("project_title")
            project_brief = request.form.get("project_brief")
            team_members = request.form.getlist("team_member")
            domain = request.form.get("domain")
            timeline = request.form.get("timeline")
            #faculty = request.form.get("faculty")
            #programme = request.form.get("programme")
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
            
            # Handle resources
            resources = request.form.getlist("resources")
            if "Other" in resources and request.form.get("other_resource"):
                resources.append(request.form.get("other_resource"))
            resources_str = ', '.join(resources)
            
            team_members_str = ', '.join(team_members)
            submission_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Save to database
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO project_proposals 
                (name, email, project_title, project_brief, team_members, domain, timeline, 
                 supervisor, faculty, programme, status, file_path, submission_date,
                 start_date, duration, resources_required, needs_mentorship, user_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                name,
                email,
                project_title,
                project_brief,
                team_members_str,
                domain,
                timeline,
                supervisor,
                faculty,
                programme,
                'Pending',  
                file_path.replace("\\", "/"),
                submission_date,
                start_date,
                duration,
                resources_str,
                needs_mentorship,
                session['user_id']
            ))
            conn.commit()
            
            flash('Project proposal submitted successfully! Our team will review it shortly.', 'success')
            return redirect(url_for('projects'))
            
        except Exception as e:
            flash(f'Error submitting proposal: {str(e)}', 'error')
            app.logger.error(f"Error submitting proposal: {str(e)}")
            return redirect(url_for('projects'))
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()

    flash('Invalid file type. Only PDF, DOC, DOCX allowed.', 'error')
    return redirect(url_for('projects'))



        
@app.route('/user/dashboard')
@login_required('user')
def user_dashboard():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, project_title, team_members, domain, supervisor, timeline, 
               status, submission_date, file_path
        FROM project_proposals 
        WHERE user_id = %s
        ORDER BY submission_date DESC
    """, (session['user_id'],))
    proposals = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('user_dashboard.html', proposals=proposals)


@app.route('/admin/approve/<int:proposal_id>')
@login_required('admin')
def approve_proposal(proposal_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE project_proposals SET status = 'Accepted' WHERE id = %s", (proposal_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/reject/<int:proposal_id>')
@login_required('admin')
def reject_proposal(proposal_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE project_proposals SET status = 'Rejected' WHERE id = %s", (proposal_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/charts')
@login_required('admin')
def admin_charts():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT status, COUNT(*) AS count FROM project_proposals GROUP BY status")
    data = cursor.fetchall()
    cursor.close()
    conn.close()

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
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT file_path FROM project_proposals WHERE id = %s", (proposal_id,))
    proposal = cursor.fetchone()
    cursor.close()
    conn.close()

    if proposal and proposal['file_path']:
        file_path = proposal['file_path']
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

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE project_proposals SET status = %s WHERE id = %s", (status, proposal_id))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/upload_completed', methods=['GET', 'POST'])
@login_required('admin')
def upload_completed_project():
    if request.method == 'POST':
        # Get form data
        project_title = request.form.get('project_title')
        domain = request.form.get('domain')
        abstract = request.form.get('abstract')
        lead_researcher = request.form.get('lead_researcher')
        supervisor = request.form.get('supervisor')
        completion_date = request.form.get('completion_date')
        faculty = request.form.get('faculty')
        programme = request.form.get('programme')
        
        # Handle file uploads
        poster_file = request.files.get('poster')
        video_file = request.files.get('video')
        report_file = request.files.get('report')
        
        # Save paths
        poster_path = None
        video_path = None
        report_path = None
        
        try:
            # Save files if they exist
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
            
            # Insert into database
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO completed_projects 
                (project_title, domain, abstract, lead_researcher, supervisor, 
                 completion_date, poster_path, video_path, report_path, faculty, programme)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                project_title, domain, abstract, lead_researcher, supervisor,
                completion_date, poster_path, video_path, report_path, faculty, programme
            ))
            conn.commit()
            flash('Completed project uploaded successfully!', 'success')
        except Exception as e:
            flash(f'Error uploading project: {str(e)}', 'error')
        finally:
            cursor.close()
            conn.close()
        
        return redirect(url_for('admin_dashboard'))
    
    return render_template('upload_completed.html')

@app.route('/get_completed_projects')
def get_completed_projects():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM completed_projects ORDER BY completion_date DESC")
    projects = cursor.fetchall()
    cursor.close()
    conn.close()
    
    # Convert to dictionary format and format dates
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
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get completed projects
    cursor.execute("SELECT * FROM completed_projects ORDER BY id ASC")
    completed_projects = cursor.fetchall()
    
    # Get ongoing projects
    cursor.execute("SELECT * FROM ongoing_projects ORDER BY id ASC")
    ongoing_projects = cursor.fetchall()
   
    
    # Format dates
    for project in completed_projects:
        if 'completion_date' in project and project['completion_date']:
            project['completion_date'] = project['completion_date'].strftime('%B %Y')
    
    for project in ongoing_projects:
        if 'created_at' in project and project['created_at']:
            project['created_at'] = project['created_at'].strftime('%B %Y')
    
    # Get user-specific project proposals only if logged in
    proposals = []
    if 'user_id' in session:
        cursor.execute("""
            SELECT id, project_title, team_members, domain, supervisor, timeline, 
                    submission_date, status
            FROM project_proposals 
            WHERE user_id = %s
            ORDER BY submission_date DESC
        """, (session['user_id'],))
        proposals = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
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

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO ongoing_projects 
                (project_title, domain, abstract, researcher, supervisor, timeline, faculty, programme)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (project_title, domain, abstract, researcher, supervisor, timeline, faculty, programme))
            conn.commit()
            flash('Ongoing project added successfully!', 'success')
            return redirect(url_for('admin_dashboard'))
        except Exception as e:
            flash(f'Error adding project: {str(e)}', 'error')
        finally:
            cursor.close()
            conn.close()
    
    return render_template('add_ongoing_project.html')

@app.route('/get_ongoing_projects')
def get_ongoing_projects():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ongoing_projects ORDER BY created_at DESC")
    projects = cursor.fetchall()
    cursor.close()
    conn.close()
    
    # Convert to dictionary format
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
    conn = get_db_connection()
    cursor = conn.cursor()
    
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

            cursor.execute("""
                UPDATE ongoing_projects 
                SET project_title = %s, domain = %s, abstract = %s, 
                    researcher = %s, supervisor = %s, timeline = %s,
                    faculty = %s, programme = %s
                WHERE id = %s
            """, (
                project_title, domain, abstract, researcher, supervisor,
                timeline, faculty, programme, project_id
            ))
            conn.commit()
            flash('Ongoing project updated successfully!', 'success')
            return redirect(url_for('admin_dashboard'))
        except Exception as e:
            flash(f'Error updating project: {str(e)}', 'error')
        finally:
            cursor.close()
            conn.close()
    
    # GET request - show edit form
    try:
        cursor.execute("SELECT * FROM ongoing_projects WHERE id = %s", (project_id,))
        project = cursor.fetchone()
        
        if not project:
            flash('Project not found', 'error')
            return redirect(url_for('admin_dashboard'))
            
        return render_template('edit_ongoing.html', project=project)
    except Exception as e:
        flash(f'Error retrieving project: {str(e)}', 'error')
        return redirect(url_for('admin_dashboard'))
    finally:
        cursor.close()
        conn.close()

@app.route('/admin/delete_ongoing/<int:project_id>', methods=['POST'])
@login_required('admin')
def delete_ongoing_project(project_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM ongoing_projects WHERE id = %s", (project_id,))
        conn.commit()
        flash('Ongoing project deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting project: {str(e)}', 'error')
    finally:
        cursor.close()
        conn.close()
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/edit_completed/<int:project_id>', methods=['GET', 'POST'])
@login_required('admin')
def edit_completed_project(project_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
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
            
            # Handle file uploads
            poster_file = request.files.get('poster')
            video_file = request.files.get('video')
            report_file = request.files.get('report')
            
            # Get current file paths
            cursor.execute("SELECT poster_path, video_path, report_path FROM completed_projects WHERE id = %s", (project_id,))
            current_files = cursor.fetchone()
            
            poster_path = current_files['poster_path']
            video_path = current_files['video_path']
            report_path = current_files['report_path']
            
            # Update files if new ones are uploaded
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
            
            cursor.execute("""
                UPDATE completed_projects 
                SET project_title = %s, domain = %s, abstract = %s, 
                    lead_researcher = %s, supervisor = %s, completion_date = %s,
                    poster_path = %s, video_path = %s, report_path = %s,
                    faculty = %s, programme = %s
                WHERE id = %s
            """, (
                project_title, domain, abstract, lead_researcher, supervisor,
                completion_date, poster_path, video_path, report_path,
                faculty, programme, project_id
            ))
            conn.commit()
            flash('Completed project updated successfully!', 'success')
            return redirect(url_for('admin_dashboard'))
        except Exception as e:
            flash(f'Error updating project: {str(e)}', 'error')
        finally:
            cursor.close()
            conn.close()
    
    # GET request - show edit form
    try:
        cursor.execute("SELECT * FROM completed_projects WHERE id = %s", (project_id,))
        project = cursor.fetchone()
        
        if not project:
            flash('Project not found', 'error')
            return redirect(url_for('admin_dashboard'))
            
        # Format date for HTML input
        if project['completion_date']:
            project['completion_date'] = project['completion_date'].strftime('%Y-%m-%d')
            
        return render_template('edit_completed.html', project=project)
    except Exception as e:
        flash(f'Error retrieving project: {str(e)}', 'error')
        return redirect(url_for('admin_dashboard'))
    finally:
        cursor.close()
        conn.close()

@app.route('/admin/delete_completed/<int:project_id>', methods=['POST'])
@login_required('admin')
def delete_completed_project(project_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # First get file paths to delete the files
        cursor.execute("SELECT poster_path, video_path, report_path FROM completed_projects WHERE id = %s", (project_id,))
        files = cursor.fetchone()
        
        # Delete files from filesystem
        if files['poster_path'] and os.path.exists(files['poster_path']):
            os.remove(files['poster_path'])
        if files['video_path'] and os.path.exists(files['video_path']):
            os.remove(files['video_path'])
        if files['report_path'] and os.path.exists(files['report_path']):
            os.remove(files['report_path'])
        
        # Delete from database
        cursor.execute("DELETE FROM completed_projects WHERE id = %s", (project_id,))
        conn.commit()
        flash('Completed project deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting project: {str(e)}', 'error')
    finally:
        cursor.close()
        conn.close()
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/dashboard')
@login_required('admin')
def admin_dashboard():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get proposals for chart and first tab
    cursor.execute("SELECT id, name, email, project_title, project_brief, status FROM project_proposals")
    proposals = cursor.fetchall()
    
    # Get data for chart
    cursor.execute("SELECT status, COUNT(*) as count FROM project_proposals GROUP BY status")
    data = cursor.fetchall()
    
    # Get ongoing projects
    cursor.execute("SELECT * FROM ongoing_projects ORDER BY id ASC")
    ongoing_projects = cursor.fetchall()
    
    # Get completed projects
    cursor.execute("SELECT * FROM completed_projects ORDER BY id ASC")
    completed_projects = cursor.fetchall()
    
    # Get all resource requests
    # For pending requests:
    cursor.execute("""
        SELECT r.*, u.username, p.project_title,
               TIME_FORMAT(r.start_time, '%H:%i') as start_time_str,
               TIME_FORMAT(r.end_time, '%H:%i') as end_time_str
        FROM resource_requests r 
        JOIN users u ON r.user_id = u.id 
        LEFT JOIN ongoing_projects p ON r.project_id1 = p.id 
        WHERE r.status = 'pending' 
        ORDER BY r.request_date DESC, r.start_time DESC
    """)

    cursor.execute("""
        SELECT r.*, u.username, p.project_title,
               TIME_FORMAT(r.start_time, '%H:%i') as start_time_str,
               TIME_FORMAT(r.end_time, '%H:%i') as end_time_str
        FROM resource_requests r 
        JOIN users u ON r.user_id = u.id 
        LEFT JOIN ongoing_projects p ON r.project_id1 = p.id 
        ORDER BY r.request_date DESC, r.start_time DESC
    """)

    
    
    all_requests = cursor.fetchall()
    
     # Get events
    
    cursor.execute("SELECT * FROM events ORDER BY created_at ASC")

    events = cursor.fetchall()
    
    # Get gallery items
    cursor.execute("SELECT * FROM gallery_items ORDER BY created_at ASC")
    gallery_items = cursor.fetchall()
    
    
    
    cursor.close()
    conn.close()

    # Generate chart
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
    conn = get_db_connection()
    cursor = conn.cursor()
  
    cursor.execute("SELECT * FROM events ORDER BY created_at ASC")
    events = cursor.fetchall()
    
    # Parse form_fields JSON for each event
    for event in events:
        if event['form_fields']:
            try:
                event['form_fields'] = json.loads(event['form_fields'])
            except json.JSONDecodeError:
                event['form_fields'] = []
        else:
            event['form_fields'] = []
    
    cursor.execute("SELECT * FROM gallery_items ORDER BY created_at ASC")
    gallery_items = cursor.fetchall()

    cursor.close()
    conn.close()
    
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
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get user's projects for dropdown
    cursor.execute("SELECT id, project_title FROM ongoing_projects")
    user_projects = cursor.fetchall()
    
    # Get user's requests
    

    
    cursor.execute("""
        SELECT r.*, p.project_title, 
               TIME_FORMAT(r.start_time, '%%H:%%i') AS start_time_str,
               TIME_FORMAT(r.end_time, '%%H:%%i') AS end_time_str
        FROM resource_requests r 
        LEFT JOIN ongoing_projects p ON r.project_id1 = p.id 
        WHERE r.user_id = %s 
        ORDER BY r.request_date DESC
    """, (session['user_id'],))

    
    user_requests = cursor.fetchall()
    
    # Admin data
    pending_requests = None
    all_requests = None
    
    if session.get('role') == 'admin':
        # Get pending requests
        cursor.execute("""
            SELECT r.*, u.username, p.project_title 
            FROM resource_requests r 
            JOIN users u ON r.user_id = u.id 
            LEFT JOIN ongoing_projects p ON r.project_id1 = p.id 
            WHERE r.status = 'pending' 
            ORDER BY r.request_date, r.start_time
        """)
        pending_requests = cursor.fetchall()
        
        # Get all requests
        cursor.execute("""
            SELECT r.*, u.username, p.project_title 
            FROM resource_requests r 
            JOIN users u ON r.user_id = u.id 
            LEFT JOIN ongoing_projects p ON r.project_id1 = p.id 
            ORDER BY r.request_date DESC, r.start_time DESC
        """)
        all_requests = cursor.fetchall()
        
        
    
    cursor.close()
    conn.close()
    
    return render_template('resource_hub.html',
                         user_requests=user_requests,
                         pending_requests=pending_requests,
                         all_requests=all_requests,
                         user_projects=user_projects)

@app.route('/submit_resource_request', methods=['POST'])
@login_required('user')
def submit_resource_request():
    if request.method == 'POST':
        conn = None
        cursor = None
        try:
            # Get form data
            has_project = request.form.get('has_project') == 'yes'
            project_id1 = request.form.get('project_id1') if has_project and request.form.get('project_id1') else None
            purpose = request.form.get('purpose') if not has_project else None
            
            # Validate required fields
            if has_project and not project_id1:
                flash('Please select a project', 'error')
                return redirect(url_for('resource_hub'))
            if not has_project and not purpose:
                flash('Please provide a purpose for your request', 'error')
                return redirect(url_for('resource_hub'))
            
            # Get resource types (as list)
            resource_types = request.form.getlist('resource_types')
            
            # Resource-specific data
            hardware_resources = ','.join(request.form.getlist('hardware_resources')) if 'hardware' in resource_types else None
            software_resources = ','.join(request.form.getlist('software_resources')) if 'software' in resource_types else None
            lab_area = request.form.get('lab_area') if 'lab' in resource_types else None
            
            # Handle "Other" options
            if hardware_resources and 'Other' in request.form.getlist('hardware_resources') and request.form.get('hardware_other'):
                # Replace "Other" with the custom value
                resources = request.form.getlist('hardware_resources')
                resources[resources.index('Other')] = request.form.get('hardware_other')
                hardware_resources = ','.join(resources)
                
            if software_resources and 'Other' in request.form.getlist('software_resources') and request.form.get('software_other'):
                # Replace "Other" with the custom value
                resources = request.form.getlist('software_resources')
                resources[resources.index('Other')] = request.form.get('software_other')
                software_resources = ','.join(resources)
            
            # Request details
            needs_mentorship = request.form.get('needs_mentorship') == 'yes'
            mentor_name = request.form.get('mentor_name') if needs_mentorship else None
            request_date = request.form.get('request_date')
            
            # Validate required fields
            if not request_date:
                flash('Request date is required', 'error')
                return redirect(url_for('resource_hub'))
            
            # Handle time fields
            start_time_str = request.form.get('start_time')
            end_time_str = request.form.get('end_time')
            
            # Convert time strings to time objects
            start_time = datetime.strptime(start_time_str, '%H:%M').time() if start_time_str else None
            end_time = datetime.strptime(end_time_str, '%H:%M').time() if end_time_str else None
            
            justification = request.form.get('justification')
            
            # Validate time fields
            if not start_time or not end_time:
                flash('Both start and end times are required', 'error')
                return redirect(url_for('resource_hub'))
            
            # Insert into database
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO resource_requests 
                (user_id, project_id1, purpose, hardware_resources, 
                 software_resources, lab_area, needs_mentorship, mentor_name, 
                 request_date, start_time, end_time, justification, status, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'pending', NOW())
            """, (
                session['user_id'],
                project_id1,
                purpose,
                hardware_resources,
                software_resources,
                lab_area,
                needs_mentorship,
                mentor_name,
                request_date,
                start_time,
                end_time,
                justification
            ))
            conn.commit()
            flash('Resource request submitted successfully!', 'success')
        except Exception as e:
            if conn:
                conn.rollback()
            flash(f'Error submitting request: {str(e)}', 'error')
            app.logger.error(f"Error submitting resource request: {str(e)}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

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
            
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE resource_requests 
                SET status = %s, admin_response = %s 
                WHERE id = %s
            """, (status, response, request_id))
            conn.commit()
            
            return jsonify({'success': True})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})
        finally:
            cursor.close()
            conn.close()
    
    return jsonify({'success': False, 'message': 'Invalid request method'})

@app.route('/admin/add_event', methods=['GET', 'POST'])
@login_required('admin')
def add_event():
    conn = None
    cursor = None
    
    if request.method == 'POST':
        try:
            # Get form data
            title = request.form.get('title', '').strip()
            excerpt = request.form.get('excerpt', '').strip()
            event_date = request.form.get('event_date', '').strip()
            event_type = request.form.get('event_type', '').strip()
            details = request.form.get('details', 'Coming Soon').strip()

            # Validate required fields
            if not all([title, event_date, event_type]):
                flash('Missing required fields', 'error')
                return redirect(url_for('add_event'))

            # Process custom form fields 
           
            field_names = request.form.getlist('field_name[]')
            field_types = request.form.getlist('field_type[]')
            field_required = request.form.getlist('field_required[]')

            form_fields = []
            for name, type, required in zip(field_names, field_types, field_required):
                if name.strip(): 
                    # The last value in field_required will be 'true' if checked, otherwise 'false'
                    is_required = required == 'true'
                    form_fields.append({
                        'name': name.strip(),
                        'type': type,
                        'required': is_required,
                        'label': name.strip().replace('_', ' ').title()
                    })
           

            # Handle file upload
            image_path = None
            if 'image' in request.files:
                image = request.files['image']
                if image and image.filename and allowed_file(image.filename):
                    filename = secure_filename(f"event_{datetime.now().timestamp()}_{image.filename}")
                    image_path = os.path.join(app.config['UPLOAD_FOLDER1'], filename)
                    image.save(image_path)

            # Database operations
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Convert form_fields to JSON string
            form_fields_json = json.dumps(form_fields) if form_fields else None
            
            cursor.execute("""
                INSERT INTO events 
                (title, excerpt, event_date, event_type, image_path, details, form_fields)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (title, excerpt, event_date, event_type, image_path, details, form_fields_json))
            
            conn.commit()
            flash('Event added successfully!', 'success')
            return redirect(url_for('admin_dashboard'))

        except Exception as e:
            flash(f'Error adding event: {str(e)}', 'error')
            app.logger.error(f"Error adding event: {str(e)}", exc_info=True)
            
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    return render_template('add_event.html')

@app.route('/admin/edit_event/<int:event_id>', methods=['GET', 'POST'])
@login_required('admin')
def edit_event(event_id):
    if request.method == 'POST':
        conn = None
        cursor = None
        try:
            # Get basic form data
            title = request.form.get('title')
            excerpt = request.form.get('excerpt')
            event_date = request.form.get('event_date')
            event_type = request.form.get('event_type')
            details = request.form.get('details', 'Coming Soon')
            
            # Process custom form fields
            field_names = request.form.getlist('field_name[]')
            field_types = request.form.getlist('field_type[]')
            
            form_fields = []
            for name, type in zip(field_names, field_types):
                if name.strip():  # Only add if field name is not empty
                    form_fields.append({
                        'name': name.strip(),
                        'type': type,
                        'required': True,  # All fields are now required
                        'label': name.strip().replace('_', ' ').title()
                    })

            # Handle file upload
            image_path = None
            if 'image' in request.files:
                image = request.files['image']
                if image and image.filename and allowed_file(image.filename):
                    # First get current image path to delete old file if exists
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute("SELECT image_path FROM events WHERE id = %s", (event_id,))
                    current_image = cursor.fetchone()
                    
                    if current_image and current_image['image_path'] and os.path.exists(current_image['image_path']):
                        os.remove(current_image['image_path'])
                    
                    # Save new image
                    filename = secure_filename(f"event_{event_id}_{datetime.now().timestamp()}_{image.filename}")
                    image_path = os.path.join(app.config['UPLOAD_FOLDER1'], filename)
                    image.save(image_path)
            
            # Database operations
            if not conn:
                conn = get_db_connection()
                cursor = conn.cursor()
            
            # If no new image uploaded, keep the existing one
            if not image_path:
                cursor.execute("SELECT image_path FROM events WHERE id = %s", (event_id,))
                existing = cursor.fetchone()
                image_path = existing['image_path'] if existing else None
            
            # Update event
            cursor.execute("""
                UPDATE events 
                SET title = %s, excerpt = %s, event_date = %s, 
                    event_type = %s, image_path = %s, details = %s,
                    form_fields = %s
                WHERE id = %s
            """, (
                title, excerpt, event_date, event_type, 
                image_path, details,
                json.dumps(form_fields) if form_fields else None, 
                event_id
            ))
            
            conn.commit()
            flash('Event updated successfully!', 'success')
            return redirect(url_for('admin_dashboard'))
            
        except Exception as e:
            if conn:
                conn.rollback()
            flash(f'Error updating event: {str(e)}', 'error')
            app.logger.error(f"Error updating event: {str(e)}", exc_info=True)
            return redirect(url_for('edit_event', event_id=event_id))
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    # GET request - show edit form
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM events WHERE id = %s", (event_id,))
        event = cursor.fetchone()
        
        if not event:
            flash('Event not found', 'error')
            return redirect(url_for('admin_dashboard'))
            
        # Parse form_fields safely
        if event['form_fields']:
            try:
                if isinstance(event['form_fields'], str):
                    event['form_fields'] = json.loads(event['form_fields'])
                elif not isinstance(event['form_fields'], (list, dict)):
                    event['form_fields'] = []
            except (json.JSONDecodeError, TypeError) as e:
                app.logger.error(f"Error parsing form_fields: {str(e)}")
                event['form_fields'] = []
        else:
            event['form_fields'] = []
            
        # Handle image path
        if event['image_path'] and event['image_path'].startswith('static/'):
            event['image_display_path'] = url_for('static', filename=event['image_path'][7:])
        else:
            event['image_display_path'] = event['image_path']
            
        return render_template('edit_event.html', event=event)
    except Exception as e:
        flash(f'Error retrieving event: {str(e)}', 'error')
        return redirect(url_for('admin_dashboard'))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        
@app.route('/submit_event_form/<int:event_id>', methods=['POST'])
@login_required()
def submit_event_form(event_id):
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'}), 401
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get event form fields
        cursor.execute("SELECT form_fields FROM events WHERE id = %s", (event_id,))
        event = cursor.fetchone()
        
        if not event:
            return jsonify({'success': False, 'message': 'Event not found'}), 404
        
        form_fields = json.loads(event['form_fields']) if event['form_fields'] else []
        
        # Process form data
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
        
        # Save submission
        cursor.execute("""
            INSERT INTO event_submissions 
            (event_id, user_id, submission_data)
            VALUES (%s, %s, %s)
        """, (event_id, session['user_id'], json.dumps(submission_data)))
        conn.commit()
        
        return jsonify({'success': True, 'message': 'Submission saved successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/admin/delete_event/<int:event_id>', methods=['POST'])
@login_required('admin')
def delete_event(event_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # First get image path to delete the file
        cursor.execute("SELECT image_path FROM events WHERE id = %s", (event_id,))
        image_path = cursor.fetchone()['image_path']
        
        # Delete image from filesystem if exists
        if image_path and os.path.exists(image_path):
            os.remove(image_path)
        
        # Delete from database
        cursor.execute("DELETE FROM events WHERE id = %s", (event_id,))
        conn.commit()
        flash('Event deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting event: {str(e)}', 'error')
    finally:
        cursor.close()
        conn.close()
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/event_submissions/<int:event_id>')
@login_required('admin')
def view_event_submissions(event_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Get event details
        cursor.execute("SELECT title FROM events WHERE id = %s", (event_id,))
        event = cursor.fetchone()
        
        if not event:
            flash('Event not found', 'error')
            return redirect(url_for('admin_dashboard'))
        
        # Get submissions
        cursor.execute("""
            SELECT es.*, u.username 
            FROM event_submissions es
            JOIN users u ON es.user_id = u.id
            WHERE es.event_id = %s
            ORDER BY es.created_at DESC
        """, (event_id,))
        submissions = cursor.fetchall()
        
        # Parse JSON data
        for sub in submissions:
            sub['data'] = json.loads(sub['submission_data'])
        
        return render_template('event_submissions.html', 
                            event=event,
                            submissions=submissions)
    except Exception as e:
        flash(f'Error retrieving submissions: {str(e)}', 'error')
        return redirect(url_for('admin_dashboard'))
    finally:
        cursor.close()
        conn.close()

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
                
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO gallery_items (title, event_date, image_path)
                    VALUES (%s, %s, %s)
                """, (title, event_date, image_path))
                conn.commit()
                
                return jsonify({'success': True})
            else:
                return jsonify({'success': False, 'message': 'Invalid file type'})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})
        finally:
            cursor.close()
            conn.close()
    return jsonify({'success': False, 'message': 'Invalid request'})

@app.route('/admin/delete_gallery_item/<int:item_id>', methods=['POST'])
@login_required('admin')
def delete_gallery_item(item_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get image path first
        cursor.execute("SELECT image_path FROM gallery_items WHERE id = %s", (item_id,))
        item = cursor.fetchone()
        
        if item and item['image_path'] and os.path.exists(item['image_path']):
            os.remove(item['image_path'])
        
        # Delete from database
        cursor.execute("DELETE FROM gallery_items WHERE id = %s", (item_id,))
        conn.commit()
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})
    finally:
        cursor.close()
        conn.close()

@app.route('/get_gallery_items')
def get_gallery_items():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM gallery_items ORDER BY event_date DESC")
    items = cursor.fetchall()
    cursor.close()
    conn.close()
    
    # Convert to dictionary format and format dates
    result = []
    for item in items:
        item_dict = dict(item)
        if 'event_date' in item_dict and item_dict['event_date']:
            item_dict['event_date'] = item_dict['event_date'].strftime('%Y-%m-%d')
        result.append(item_dict)
    
    
@app.route('/get_user_projects')
@login_required('user')
def get_user_projects():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get both ongoing projects and the user's proposals
    cursor.execute("""
    SELECT id, project_title FROM ongoing_projects
""")

    
    projects = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return jsonify(projects)   
    
 
    
@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


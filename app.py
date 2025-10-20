from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file, jsonify, make_response
import os
import pymysql
from werkzeug.utils import secure_filename
from datetime import datetime, date, timedelta
from werkzeug.exceptions import abort
from functools import wraps
import matplotlib
matplotlib.use('Agg')
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
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
from werkzeug.exceptions import HTTPException
from flask_wtf.csrf import generate_csrf, CSRFError 
from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file, jsonify, make_response, abort
from uuid import uuid4

csrf = CSRFProtect()

load_dotenv()

app = Flask(__name__, static_folder='static')

IS_PROD = os.getenv("ENV", "development").lower() in ("prod", "production", "live")
USE_DEV_SSL = os.getenv("DEV_SSL", "0").lower() in ("1","true","yes","on")

if USE_DEV_SSL and not IS_PROD:
    PREFERRED_SCHEME = "https"
    COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
else:
    PREFERRED_SCHEME = "http"
    COOKIE_SECURE = IS_PROD
    SESSION_COOKIE_SECURE = IS_PROD

CSP = {
    "default-src": ["'self'"],

    "script-src": [
        "'self'",
        "'unsafe-inline'",           
        "https://cdn.jsdelivr.net",
        "https://cdnjs.cloudflare.com",
        "https://unpkg.com"
    ],

    "style-src": [
        "'self'",
        "'unsafe-inline'",
        "https://fonts.googleapis.com",
        "https://cdn.jsdelivr.net",
        "https://cdnjs.cloudflare.com"
    ],

    # Fonts & images 
    "font-src":  ["'self'", "https://fonts.gstatic.com", "data:"],
    "img-src":   ["'self'", "data:", "https:"],

    # XHR/fetch/websocket destinations
    "connect-src": ["'self'"],

    # Clickjacking & legacy objects
    "frame-ancestors": "'none'",
    "object-src": "'none'",

    # Misc hardening
    "base-uri": "'self'",
    "form-action": "'self'",
}

IS_PROD = os.getenv("ENV", "development").lower() in ("prod","production","live")

Talisman(
    app,
    content_security_policy=CSP,
    frame_options='DENY',
    referrer_policy='strict-origin-when-cross-origin',
    permissions_policy="geolocation=(), microphone=(), camera=(), payment=(), usb=(), browsing-topics=()",
    force_https=IS_PROD,                 # False in dev
    strict_transport_security=IS_PROD    # turn off HSTS in dev
)


csrf.init_app(app) 


app.config["RATELIMIT_HEADERS_ENABLED"] = True

# IS_PROD = os.getenv("ENV", "production").lower() in ("prod", "production", "live")
app.logger.info("IS_PROD=%s  PREFERRED_URL_SCHEME=%s  SESSION_COOKIE_SECURE=%s",
                IS_PROD, app.config.get("PREFERRED_URL_SCHEME"), app.config.get("SESSION_COOKIE_SECURE"))


#  Cookie/Sessions hardening 
COOKIE_DOMAIN  = os.getenv("COOKIE_DOMAIN") or None
COOKIE_NAME    = "access_token"

# Prod defaults; allow env overrides for local/dev
COOKIE_SECURE  = IS_PROD or (os.getenv("COOKIE_SECURE", "False").lower() == "true")
COOKIE_SAMESITE = os.getenv("COOKIE_SAMESITE", "Lax")


app.config.update(
    PREFERRED_URL_SCHEME=PREFERRED_SCHEME,
    SESSION_COOKIE_SECURE=SESSION_COOKIE_SECURE,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE=os.getenv("COOKIE_SAMESITE", "Lax"),
    SEND_FILE_MAX_AGE_DEFAULT=0,
    DEBUG=False,
    TESTING=False,
    PROPAGATE_EXCEPTIONS=False,
    TRAP_HTTP_EXCEPTIONS=False,
)


app.logger.setLevel(logging.INFO if IS_PROD else logging.DEBUG)

app.secret_key = os.getenv("SECRET_KEY", "change-me")
JWT_SECRET = os.getenv("JWT_SECRET", "change-me")


limiter = Limiter(
    key_func=get_remote_address,
    app=app, 
    storage_uri=os.getenv("RATELIMIT_STORAGE_URI", "memory://"), 
    #default_limits=["400 per day", "50 per hour"],  
    default_limits=["5 per minute"],
    headers_enabled=True, 
)



app.config['MAX_CONTENT_LENGTH'] = int(os.getenv("MAX_CONTENT_MB", 20)) * 1024 * 1024

PRIVATE_UPLOAD_ROOT = os.path.join(app.instance_path, "uploads")
os.makedirs(PRIVATE_UPLOAD_ROOT, exist_ok=True)

PUBLIC_UPLOAD_ROOT = os.path.join(app.root_path, "static", "uploads")
os.makedirs(PUBLIC_UPLOAD_ROOT, exist_ok=True)

app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'doc', 'docx', 'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov', 'avi'}

# MIME allow-lists
ALLOWED_MIME_DOC = {
    "application/pdf",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}
ALLOWED_MIME_IMG = {"image/png", "image/jpeg", "image/gif"}
ALLOWED_MIME_VIDEO = {"video/mp4", "video/quicktime", "video/x-msvideo"}

@app.context_processor
def inject_csrf():
    return {"csrf_token": generate_csrf}

# Security headers 
@app.after_request
def set_security_headers(resp):
    resp.headers['X-Content-Type-Options'] = 'nosniff'
    if not IS_PROD:
        resp.headers.pop('Strict-Transport-Security', None)
    return resp

#  Generic error responses
def _wants_json():
    return (
        request.is_json
        or request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        or (request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html)
    )

GENERIC_MSG = {
    400: "Bad request.",
    401: "Not authorized.",
    403: "Access denied.",
    404: "We couldn't find that.",
    405: "Method not allowed.",
    413: "File too large.",
    415: "Unsupported media type.",
    429: "Too many requests. Please try again later.",
    500: "Something went wrong. Please try again.",
}

def _render_error(status_code, original_error=None):
    if status_code >= 500:
        app.logger.exception("Unhandled server error", exc_info=original_error)
    else:
        app.logger.warning("Handled error %s at %s", status_code, request.path)

    message = GENERIC_MSG.get(status_code, "Something went wrong.")
    if _wants_json():
        return jsonify(success=False, message=message), status_code
    return render_template("error.html", status_code=status_code, message=message), status_code

# All Werkzeug HTTP errors (404/405/413/429/…)
@app.errorhandler(HTTPException)
def handle_http_exception(e: HTTPException):
    return _render_error(e.code or 500, original_error=e)

# Anything else - 500
@app.errorhandler(Exception)
def handle_uncaught(e: Exception):
    return _render_error(500, original_error=e)

@app.errorhandler(CSRFError)              
def handle_csrf(e):
    return _render_error(403, original_error=e)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def _randomized_name(original: str) -> str:
    base = secure_filename(original) or "file"
    return f"{uuid4().hex}_{base}"

def _save_upload(file_storage, root_dir: str, allowed_mime: set, subdir: str = "") -> str:
    if file_storage.mimetype not in allowed_mime:
        raise ValueError("Invalid file type")
    target_dir = os.path.join(root_dir, subdir) if subdir else root_dir
    os.makedirs(target_dir, exist_ok=True)
    rand_name = _randomized_name(file_storage.filename)
    file_path = os.path.join(target_dir, rand_name)
    file_storage.save(file_path)
    return file_path 

def _is_under(path: str, directory: str) -> bool:
    try:
        return os.path.commonpath([os.path.realpath(path), os.path.realpath(directory)]) == os.path.realpath(directory)
    except ValueError:
        return False


def _to_static_rel(full_path: str) -> str:
    rel = os.path.relpath(full_path, app.root_path).replace("\\", "/")
    if not rel.startswith("static/"):
        raise ValueError("Public path must resolve under /static")
    return rel

def login_required(role=None):
    def wrapper(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if 'user_id' not in session:
                data = get_user_from_cookie()
                if data:
                    session['user_id'] = data['sub']
                    session['username'] = data['username']
                    session['role'] = data['role']
                else:
                    session['next'] = request.path
                    return redirect(url_for('login'))

            if role and session.get('role') != role:
                abort(403)

            return f(*args, **kwargs)
        return decorated
    return wrapper


@app.route('/')
def landing():
    return render_template('landing.html')

# strong password validator 
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
            errors['password'] = 'Use 8–64 chars with upper, lower, and number'

        if password != confirm_password:
            errors['confirm_password'] = 'Passwords do not match'

        if errors:
            # SERVER-SIDE REJECTION 
            return render_template('signup.html', errors=errors, form_data=request.form), 400

        try:
            pw_hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
            m.create_user(username, email, pw_hash)
            flash('Account created successfully! Please login', 'success')
            return redirect(url_for('login'))
        except pymysql.IntegrityError:
            errors['username'] = 'Username already exists'
            return render_template('signup.html', errors=errors, form_data=request.form), 400
        except Exception:
            flash('An unexpected error occurred. Please try again later.', 'error')
            return render_template('signup.html', errors=errors, form_data=request.form), 500

    return render_template('signup.html', errors=errors, form_data=request.form)


# login
#@limiter.limit("5 per minute; 20 per hour")
@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("3 per minute; 20 per hour")
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

            if user:
                ok = False

                if isinstance(user.get('password_hash'), str) and ':' in user['password_hash']:
                    ok = check_password_hash(user['password_hash'], password)  

                elif user.get('password_hash') == password:
                    new_hash = generate_password_hash(password, method="pbkdf2:sha256", salt_length=16)  
               
                    try:
                        m.update_user_password_hash(user['id'], new_hash)  
                        ok = True
                    except Exception:
                        ok = False  

                if ok:
                  
                    session['user_id'] = user['id']
                    session['username'] = user['username']
                    session['role'] = user['role']

                
                    payload = {
                        "sub": str(user['id']),
                        "username": user['username'],
                        "role": user['role'],
                        "iat": int(time.time()),
                        "exp": int(time.time()) + 60*60*8  # 8 hours
                    }
                    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256") 

                    resp = redirect(url_for('admin_dashboard' if user['role'] == 'admin' else 'landing'))
                    resp.set_cookie(
                        COOKIE_NAME, token,
                        httponly=True,
                        secure=COOKIE_SECURE,       
                        samesite=COOKIE_SAMESITE,   
                        path="/",
                        domain=COOKIE_DOMAIN
                    )

                    flash('Login successful!', 'success')
                    return resp

            errors['auth'] = 'Invalid username or password'

        return render_template('login.html', errors=errors, username=username)
    return render_template('login.html', errors=errors)

def create_jwt(user_id: int, username: str, role: str) -> str:
    payload = {
        'sub': user_id,
        'username': username,
        'role': role,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(hours=8)  
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

@app.route('/logout')
def logout():
    session.clear()
    resp = make_response(redirect(url_for('login')))
    resp.set_cookie(COOKIE_NAME, '', expires=0, path='/', domain=COOKIE_DOMAIN, samesite=COOKIE_SAMESITE, secure=COOKIE_SECURE, httponly=True)
    return resp

@app.route('/proposal', methods=['GET', 'POST'])
@login_required('user')
def proposal():
    return render_template('proposal.html')

@app.route('/submit_proposal', methods=['POST'])
@login_required('user')
def submit_proposal():
    file = request.files.get('file')
    if not file or file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('projects'))

    if not allowed_file(file.filename) or file.mimetype not in ALLOWED_MIME_DOC:
        flash('Invalid file type. Only PDF/DOC/DOCX allowed.', 'error')
        return redirect(url_for('projects'))

    try:
        file_path = _save_upload(file, PRIVATE_UPLOAD_ROOT, ALLOWED_MIME_DOC, subdir="proposals")
        db_path = file_path.replace("\\", "/") 

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
            name,
            email,
            project_title,
            project_brief,
            team_members_str,
            domain,
            timeline,
            needs_mentorship,  
            supervisor,
            faculty,
            programme,
            start_date,
            duration,
            resources_str,
            db_path,            
            submission_date,
            'Pending',         
            session['user_id']
        ))


        flash('Project proposal submitted successfully! Our team will review it shortly.', 'success')
        return redirect(url_for('projects'))

    except ValueError:
        flash('Invalid file type', 'error')
        return redirect(url_for('projects'))
    except Exception:
        app.logger.exception("submit_proposal: unexpected error")
        flash('Something went wrong. Please try again.', 'error')
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
    plt.close()
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    return render_template('admin_charts.html', plot_url=plot_url)

@app.route('/download_file')
@login_required()
def legacy_download():
    raw = (request.args.get('path') or '').strip()
    if not raw:
        flash('No file specified', 'error')
        return redirect(url_for('projects'))

    if os.path.isabs(raw):
        abs_path = os.path.abspath(raw)
    else:
        abs_path = os.path.abspath(os.path.join(app.root_path, raw.lstrip('/\\')))

    allowed_roots = [
        PRIVATE_UPLOAD_ROOT,
        os.path.join(app.root_path, 'static'),
        os.path.join(app.root_path, 'static', 'uploads'),
    ]
    if not any(_is_under(abs_path, root) for root in allowed_roots):
        app.logger.warning("Blocked download outside allowed roots: %s", abs_path)
        return _render_error(404)  
    if not os.path.exists(abs_path):
        return _render_error(404)

    return send_file(abs_path, as_attachment=True)


@app.route('/download/<int:proposal_id>')
@login_required('admin')
def download_file(proposal_id):
    file_path = m.get_file_path_for_proposal(proposal_id)
    if not file_path:
        abort(404)
    abs_path = os.path.abspath(file_path)
    if not _is_under(abs_path, PRIVATE_UPLOAD_ROOT) or not os.path.exists(abs_path):
        abort(404)
    return send_file(abs_path, as_attachment=True)


@app.route('/completed/<int:project_id>/download/<kind>')
# @login_required('admin')
@login_required()
def download_completed_file(project_id, kind):
    if kind not in ('video', 'report'):
        abort(400)

    files = m.get_completed_files(project_id) or {}
    path = files.get(f'{kind}_path')
    if not path:
        abort(404)

    abs_path = os.path.abspath(path)
    base_dir = os.path.join(PRIVATE_UPLOAD_ROOT, f"{kind}s")
    if not _is_under(abs_path, base_dir) or not os.path.exists(abs_path):
        abort(404)

    return send_file(abs_path, as_attachment=True)


@app.route('/admin/update_user_password/<int:user_id>', methods=['POST'])
@login_required('admin')
@limiter.limit("5 per minute")  
def admin_update_user_password(user_id):
    new_pw = (request.form.get('new_password') or '').strip()
    confirm_pw = (request.form.get('confirm_password') or '').strip()

    if not new_pw or not confirm_pw:
        flash('Both password fields are required.', 'error')
        return redirect(url_for('admin_dashboard'))

    if new_pw != confirm_pw:
        flash('Passwords do not match.', 'error')
        return redirect(url_for('admin_dashboard'))

    if not password_strong(new_pw):
        flash('Password must be 8–64 chars with upper, lower, and a number.', 'error')
        return redirect(url_for('admin_dashboard'))

    try:
        pw_hash = generate_password_hash(new_pw, method='pbkdf2:sha256', salt_length=16)
        m.update_user_password_hash(user_id, pw_hash)
        flash('Password updated successfully.', 'success')
    except Exception:
        app.logger.exception("admin_update_user_password failed")
        flash('Something went wrong. Please try again.', 'error')

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
                p_fs = _save_upload(poster_file, PUBLIC_UPLOAD_ROOT, ALLOWED_MIME_IMG, subdir="posters")
                poster_path = _to_static_rel(p_fs)  

            if video_file and allowed_file(video_file.filename):
                video_path = _save_upload(video_file, PRIVATE_UPLOAD_ROOT, ALLOWED_MIME_VIDEO, subdir="videos")

            if report_file and allowed_file(report_file.filename):
                report_path = _save_upload(report_file, PRIVATE_UPLOAD_ROOT, ALLOWED_MIME_DOC, subdir="reports")

            m.insert_completed_project((
                project_title, domain, abstract, lead_researcher, supervisor,
                completion_date, poster_path, video_path, report_path, faculty, programme
            ))
            flash('Completed project uploaded successfully!', 'success')

        except ValueError:
            flash('Invalid file type', 'error')
        except Exception:
            app.logger.exception("Error uploading request")
            flash('Something went wrong. Please try again.', 'error')

        return redirect(url_for('admin_dashboard'))

    return render_template('upload_completed.html')


@app.route('/get_completed_projects')
def get_completed_projects():
    projects = m.list_completed_projects_desc_by_date()
    result = []
    for project in projects:
        d = dict(project)
        if d.get('completion_date'):
            d['completion_date'] = d['completion_date'].strftime('%Y-%m-%d')
        d['has_video'] = bool(d.pop('video_path', None))
        d['has_report'] = bool(d.pop('report_path', None))
        result.append(d)
    return jsonify(result)





def _fmt_month(val):
    if isinstance(val, (datetime, date)):
        return val.strftime('%B %Y')
    return val or None

@app.route('/projects')
def projects():
    completed_projects = m.list_completed_projects_ordered() or []
    ongoing_projects   = m.list_ongoing_projects_ordered() or []

    for p in completed_projects:
        if 'completion_date' in p:
            p['completion_date'] = _fmt_month(p.get('completion_date'))

        p['has_video']  = bool(p.get('video_path'))
        p['has_report'] = bool(p.get('report_path'))

    for p in ongoing_projects:
        if 'created_at' in p:
            p['created_at'] = _fmt_month(p.get('created_at'))

    proposals = []
    if session.get('user_id'):
        try:
            proposals = m.get_user_proposals_brief(session['user_id']) or []
            for pr in proposals:
                sd = pr.get('submission_date')
                if isinstance(sd, str):
                    for fmt in ('%Y-%m-%d %H:%M:%S', '%Y-%m-%d'):
                        try:
                            pr['submission_date'] = datetime.strptime(sd, fmt)
                            break
                        except ValueError:
                            continue
        except Exception:
            app.logger.exception("get_user_proposals_brief failed")
            proposals = []

    return render_template(
        'projects.html',
        completed_projects=completed_projects,
        ongoing_projects=ongoing_projects,
        proposals=proposals,
        logged_in=bool(session.get('user_id'))
    )


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
            app.logger.exception("Error adding ongoing project")
            flash('Something went wrong. Please try again.', 'error')
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
            app.logger.exception("Error updating request")
            flash('Something went wrong. Please try again.', 'error')

    try:
        project = m.get_ongoing_project(project_id)
        if not project:
            flash('Project not found', 'error')
            return redirect(url_for('admin_dashboard'))
        return render_template('edit_ongoing.html', project=project)
    except Exception as e:
        app.logger.exception("Error retrieveing request")
        flash('Something went wrong. Please try again.', 'error')
        return redirect(url_for('admin_dashboard'))

@app.route('/admin/delete_ongoing/<int:project_id>', methods=['POST'])
@login_required('admin')
def delete_ongoing_project(project_id):
    try:
        m.delete_ongoing_project(project_id)
        flash('Ongoing project deleted successfully!', 'success')
    except Exception as e:
        app.logger.exception("Error deleting request")
        flash('Something went wrong. Please try again.', 'error')
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
            video_path  = current_files['video_path']  if current_files else None
            report_path = current_files['report_path'] if current_files else None

            if poster_file and allowed_file(poster_file.filename):
                base_posters = os.path.join(PUBLIC_UPLOAD_ROOT, "posters")
                if poster_path:
                    old_abs = poster_path if os.path.isabs(poster_path) else os.path.join(app.root_path, poster_path)
                    if _is_under(old_abs, base_posters) and os.path.exists(old_abs):
                        os.remove(old_abs)
                new_fs = _save_upload(poster_file, PUBLIC_UPLOAD_ROOT, ALLOWED_MIME_IMG, subdir="posters")
                poster_path = _to_static_rel(new_fs)  # store 'static/...'
            
            if video_file and allowed_file(video_file.filename):
                base_videos = os.path.join(PRIVATE_UPLOAD_ROOT, "videos")
                if video_path and _is_under(video_path, base_videos) and os.path.exists(video_path):
                    os.remove(video_path)
                video_path = _save_upload(video_file, PRIVATE_UPLOAD_ROOT, ALLOWED_MIME_VIDEO, subdir="videos")

            if report_file and allowed_file(report_file.filename):
                base_reports = os.path.join(PRIVATE_UPLOAD_ROOT, "reports")
                if report_path and _is_under(report_path, base_reports) and os.path.exists(report_path):
                    os.remove(report_path)
                report_path = _save_upload(report_file, PRIVATE_UPLOAD_ROOT, ALLOWED_MIME_DOC, subdir="reports")

            m.update_completed_project((
                project_title, domain, abstract, lead_researcher, supervisor,
                completion_date, poster_path, video_path, report_path,
                faculty, programme, project_id
            ))

            flash('Completed project updated successfully!', 'success')
            return redirect(url_for('admin_dashboard'))
        except Exception as e:
            app.logger.exception("Error updating project")
            flash('Something went wrong. Please try again.', 'error')

    try:
        project = m.get_completed_project_by_id(project_id)
        if not project:
            flash('Project not found', 'error')
            return redirect(url_for('admin_dashboard'))
        if project['completion_date']:
            project['completion_date'] = project['completion_date'].strftime('%Y-%m-%d')
        return render_template('edit_completed.html', project=project)
    except Exception as e:
        app.logger.exception("Error retrieving project")
        flash('Something went wrong. Please try again.', 'error')
        return redirect(url_for('admin_dashboard'))



@app.route('/admin/delete_completed/<int:project_id>', methods=['POST'])
@login_required('admin')
def delete_completed_project(project_id):
    try:
        files = m.get_completed_files(project_id) or {}

        def _safe_delete(stored_path: str, base_dir: str):
            """Delete only if the resolved path is under base_dir."""
            if not stored_path:
                return
            abs_p = stored_path if os.path.isabs(stored_path) else os.path.join(app.root_path, stored_path)
            if _is_under(abs_p, base_dir) and os.path.exists(abs_p):
                try:
                    os.remove(abs_p)
                except Exception:
                    app.logger.warning("Failed to remove file: %s", abs_p, exc_info=True)

        
        _safe_delete(files.get('poster_path'), os.path.join(PUBLIC_UPLOAD_ROOT, "posters"))
        _safe_delete(files.get('video_path'),  os.path.join(PRIVATE_UPLOAD_ROOT, "videos"))
        _safe_delete(files.get('report_path'), os.path.join(PRIVATE_UPLOAD_ROOT, "reports"))

        m.delete_completed_project(project_id)
        flash('Completed project deleted successfully!', 'success')
    except Exception:
        app.logger.exception("Error deleting project")
        flash('Something went wrong. Please try again.', 'error')
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
    users = m.list_users_ordered()

    statuses = [row['status'] for row in data]
    counts = [row['count'] for row in data]

    img = io.BytesIO()
    try:
        import seaborn as sns  
        plt.figure(figsize=(6, 4))
        sns.barplot(x=statuses, y=counts, hue=statuses, legend=False)
        plt.legend().remove() if plt.gca().get_legend() else None
    except Exception:
        plt.figure(figsize=(6, 4))
        plt.bar(statuses, counts)

    plt.xlabel("Status")
    plt.ylabel("Count")
    plt.title("Proposals by Status")
    plt.grid(axis='y')
    plt.tight_layout()

    plt.savefig(img, format='png')
    plt.close()             
    img.seek(0)
    chart_url = base64.b64encode(img.getvalue()).decode()


    return render_template('admin.html',
                        proposals=proposals,
                        chart_url=f"data:image/png;base64,{chart_url}",
                        ongoing_projects=ongoing_projects,
                        completed_projects=completed_projects,
                        pending_requests=_pending_requests,  
                        all_requests=all_requests,
                        events=events,
                        gallery_items=gallery_items,
                        users=users, 
                    )

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
            app.logger.exception("Error submitting request")
            flash('Something went wrong. Please try again.', 'error')
            
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
                return jsonify({'success': False, 'message': 'Invalid action'}), 400


            status = 'approved' if action == 'approve' else 'rejected'
            m.update_resource_request_status(request_id, status, response)
            return jsonify({'success': True})
        except Exception:
            app.logger.exception("process_resource_request: unexpected error")
            return jsonify({'success': False, 'message': GENERIC_MSG[500]}), 500

    return jsonify({'success': False, 'message': 'Invalid request method'}), 405

    

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
            img = request.files.get('image')
            if img and img.filename and allowed_file(img.filename):
                img_fs = _save_upload(img, PUBLIC_UPLOAD_ROOT, ALLOWED_MIME_IMG, subdir="events")
                image_path = _to_static_rel(img_fs)  # 'static/...'


            form_fields_json = json.dumps(form_fields) if form_fields else None
            m.insert_event((title, excerpt, event_date, event_type, image_path, details, form_fields_json))
            flash('Event added successfully!', 'success')
            return redirect(url_for('admin_dashboard'))

        except Exception as e:
            app.logger.exception("Error adding event")
            flash('Something went wrong. Please try again.', 'error')
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
            img = request.files.get('image')
            if img and img.filename and allowed_file(img.filename):
                base_events = os.path.join(PUBLIC_UPLOAD_ROOT, "events")
                current_image_path = m.get_event_image_path(event_id)
                if current_image_path:
                    old_abs = current_image_path if os.path.isabs(current_image_path) else os.path.join(app.root_path, current_image_path)
                    if _is_under(old_abs, base_events) and os.path.exists(old_abs):
                        os.remove(old_abs)
                img_fs = _save_upload(img, PUBLIC_UPLOAD_ROOT, ALLOWED_MIME_IMG, subdir="events")
                image_path = _to_static_rel(img_fs)


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
            app.logger.exception("Error updating event")
            flash('Something went wrong. Please try again.', 'error')
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
                    allowed_all = ALLOWED_MIME_DOC | ALLOWED_MIME_IMG | ALLOWED_MIME_VIDEO
                    saved = _save_upload(
                        file,
                        PRIVATE_UPLOAD_ROOT,
                        allowed_all,
                        subdir=f"event_submissions/{event_id}"
                    )
                    submission_data[field_name] = saved  
                elif field.get('required'):
                    return jsonify({'success': False, 'message': f'{field_name} is required'}), 400
            else:
                value = request.form.get(field_name)
                if (not value) and field.get('required'):
                    return jsonify({'success': False, 'message': f'{field_name} is required'}), 400
                submission_data[field_name] = value

        m.insert_event_submission(event_id, session['user_id'], json.dumps(submission_data))
        return jsonify({'success': True, 'message': 'Submission saved successfully'})
    except Exception:
        app.logger.exception("submit_event_form: unexpected error")
        return jsonify({'success': False, 'message': GENERIC_MSG[500]}), 500


@app.route('/admin/delete_event/<int:event_id>', methods=['POST'])
@login_required('admin')
def delete_event(event_id):
    try:
        base_events = os.path.join(PUBLIC_UPLOAD_ROOT, "events")
        image_path = m.get_event_image_path(event_id)
        if image_path:
            abs_p = image_path if os.path.isabs(image_path) else os.path.join(app.root_path, image_path)
            if _is_under(abs_p, base_events) and os.path.exists(abs_p):
                os.remove(abs_p)

        m.delete_event(event_id)
        flash('Event deleted successfully!', 'success')
    except Exception as e:
        app.logger.exception("Error deleting event")
        flash('Something went wrong. Please try again.', 'error')
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/event_submissions/<int:event_id>')
@login_required('admin')
def view_event_submissions(event_id):
    title = m.get_event_title(event_id)
    if not title:
        flash('Event not found', 'error')
        return redirect(url_for('admin_dashboard'))

    submissions = m.get_event_submissions_with_user(event_id) or []

    safe = []
    for sub in submissions:
        raw = sub.get('submission_data') if isinstance(sub, dict) else None
        try:
            parsed = json.loads(raw) if raw else {}
        except Exception:
            parsed = {}

    
        files = {}
        for k, v in list(parsed.items()):
            if isinstance(v, str) and v and (os.path.isabs(v) or v.startswith('static/')):
                files[k] = url_for('legacy_download', path=v)

        created_at_display = ''
        ca = sub.get('created_at')
        if hasattr(ca, 'strftime'):
            created_at_display = ca.strftime('%Y-%m-%d %H:%M')
        elif isinstance(ca, str):
            created_at_display = ca

        sub['data'] = parsed
        sub['files'] = files
        sub['created_at_display'] = created_at_display
        safe.append(sub)

    return render_template(
        'event_submissions.html',
        event={'id': event_id, 'title': title},
        submissions=safe
    )


@app.route('/admin/add_gallery_item', methods=['POST'])
@login_required('admin')
def add_gallery_item():
    if request.method == 'POST':
        try:
            title = request.form.get('title')
            event_date = request.form.get('event_date')

            if 'image' not in request.files:
                return jsonify({'success': False, 'message': 'No image file provided'}), 400

            image = request.files.get('image')
            if not image or image.filename == '':
                return jsonify({'success': False, 'message': 'No selected image'}), 400
            if not allowed_file(image.filename):
                return jsonify({'success': False, 'message': 'Invalid file type'}), 400

            try:
                img_fs = _save_upload(image, PUBLIC_UPLOAD_ROOT, ALLOWED_MIME_IMG, subdir="gallery")
                image_path = _to_static_rel(img_fs)  # 'static/...'
                m.insert_gallery_item(title, event_date, image_path)
                return jsonify({'success': True})
            except ValueError:
                return jsonify({'success': False, 'message': 'Invalid file type'}), 400
            except Exception:
                app.logger.exception("add_gallery_item: unexpected error (inner)")
                return jsonify({'success': False, 'message': GENERIC_MSG[500]}), 500

        except Exception:
            app.logger.exception("add_gallery_item: unexpected error (outer)")
            return jsonify({'success': False, 'message': GENERIC_MSG[500]}), 500

    return jsonify({'success': False, 'message': 'Method not allowed'}), 405


@app.route('/admin/delete_gallery_item/<int:item_id>', methods=['POST'])
@login_required('admin')
def delete_gallery_item(item_id):
    try:
        base_gallery = os.path.join(PUBLIC_UPLOAD_ROOT, "gallery")
        image_path = m.get_gallery_item_image_path(item_id)
        if image_path:
            abs_p = image_path if os.path.isabs(image_path) else os.path.join(app.root_path, image_path)
            if _is_under(abs_p, base_gallery) and os.path.exists(abs_p):
                os.remove(abs_p)

        m.delete_gallery_item(item_id)  
        return jsonify({'success': True})
    except Exception:
        app.logger.exception("delete_gallery_item: unexpected error")
        return jsonify({'success': False, 'message': GENERIC_MSG[500]}), 500

@app.route('/get_gallery_items')
def get_gallery_items():
    items = m.list_gallery_items_desc_by_event_date()
    result = []
    for item in items:
        item_dict = dict(item)
        if 'event_date' in item_dict and item_dict['event_date']:
            item_dict['event_date'] = item_dict['event_date'].strftime('%Y-%m-%d')
        result.append(item_dict)
    return jsonify(result)


@app.route('/get_user_projects')
@login_required('user')
def get_user_projects():
    projects = m.list_ongoing_id_title()
    return jsonify(projects)

@app.route('/about')
def about():
    return render_template('about.html')



if __name__ == '__main__':

    host  = os.getenv("APP_HOST", "0.0.0.0")
    port  = int(os.getenv("PORT") or os.getenv("APP_PORT") or 5000)
    debug = os.getenv("DEBUG", "False").lower() in ("1","true","yes","on")

    app.run(host=host, port=port, debug=debug)


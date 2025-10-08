from typing import Any, Dict, List, Optional, Tuple
import json
from db import get_db_connection

# ---------- Users ----------
def create_user(username: str, email: str, password_hash: str) -> None:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, email, password_hash, role) VALUES (%s, %s, %s, 'user')",
            (username, email, password_hash)
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()

def get_user_by_username(username: str) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()

# ---------- Proposals ----------
def insert_project_proposal(values: Tuple) -> None:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO project_proposals 
            (name, email, project_title, project_brief, team_members, domain, timeline, 
             supervisor, faculty, programme, status, file_path, submission_date,
             start_date, duration, resources_required, needs_mentorship, user_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            values
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()

def get_user_proposals(user_id: int) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT id, project_title, team_members, domain, supervisor, timeline, 
                   status, submission_date, file_path
            FROM project_proposals 
            WHERE user_id = %s
            ORDER BY submission_date DESC
            """,
            (user_id,)
        )
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

def approve_proposal(proposal_id: int) -> None:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE project_proposals SET status = 'Accepted' WHERE id = %s", (proposal_id,))
        conn.commit()
    finally:
        cursor.close()
        conn.close()

def reject_proposal(proposal_id: int) -> None:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE project_proposals SET status = 'Rejected' WHERE id = %s", (proposal_id,))
        conn.commit()
    finally:
        cursor.close()
        conn.close()

def proposals_status_counts() -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT status, COUNT(*) AS count FROM project_proposals GROUP BY status")
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

def get_file_path_for_proposal(proposal_id: int) -> Optional[str]:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT file_path FROM project_proposals WHERE id = %s", (proposal_id,))
        row = cursor.fetchone()
        return row["file_path"] if row and "file_path" in row else None
    finally:
        cursor.close()
        conn.close()

def update_proposal_status(proposal_id: int, status: str) -> None:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE project_proposals SET status = %s WHERE id = %s", (status, proposal_id))
        conn.commit()
    finally:
        cursor.close()
        conn.close()

def proposals_basic_list() -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, name, email, project_title, project_brief, status FROM project_proposals")
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

def get_user_proposals_brief(user_id: int) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT id, project_title, team_members, domain, supervisor, timeline, 
                    submission_date, status
            FROM project_proposals 
            WHERE user_id = %s
            ORDER BY submission_date DESC
            """,
            (user_id,)
        )
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

# ---------- Completed Projects ----------
def insert_completed_project(values: Tuple) -> None:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO completed_projects 
            (project_title, domain, abstract, lead_researcher, supervisor, 
             completion_date, poster_path, video_path, report_path, faculty, programme)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """.
            replace("\n", "\n")
            ,
            values
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()

def list_completed_projects_desc_by_date() -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM completed_projects ORDER BY completion_date DESC")
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

def list_completed_projects_ordered() -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM completed_projects ORDER BY id ASC")
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

def get_completed_files(project_id: int) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT poster_path, video_path, report_path FROM completed_projects WHERE id = %s", (project_id,))
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()

def update_completed_project(values: Tuple) -> None:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE completed_projects 
            SET project_title = %s, domain = %s, abstract = %s, 
                lead_researcher = %s, supervisor = %s, completion_date = %s,
                poster_path = %s, video_path = %s, report_path = %s,
                faculty = %s, programme = %s
            WHERE id = %s
            """,
            values
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()

def delete_completed_project(project_id: int) -> None:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM completed_projects WHERE id = %s", (project_id,))
        conn.commit()
    finally:
        cursor.close()
        conn.close()

def get_completed_project_by_id(project_id: int) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM completed_projects WHERE id = %s", (project_id,))
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()

# ---------- Ongoing Projects ----------
def insert_ongoing_project(values: Tuple) -> None:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO ongoing_projects 
            (project_title, domain, abstract, researcher, supervisor, timeline, faculty, programme)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            values
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()

def list_ongoing_projects_ordered() -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM ongoing_projects ORDER BY id ASC")
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

def list_ongoing_projects_desc_created() -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM ongoing_projects ORDER BY created_at DESC")
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

def update_ongoing_project(values: Tuple) -> None:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE ongoing_projects 
            SET project_title = %s, domain = %s, abstract = %s, 
                researcher = %s, supervisor = %s, timeline = %s,
                faculty = %s, programme = %s
            WHERE id = %s
            """,
            values
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()

def get_ongoing_project(project_id: int) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM ongoing_projects WHERE id = %s", (project_id,))
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()

def delete_ongoing_project(project_id: int) -> None:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM ongoing_projects WHERE id = %s", (project_id,))
        conn.commit()
    finally:
        cursor.close()
        conn.close()

def list_ongoing_id_title() -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, project_title FROM ongoing_projects")
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

# ---------- Resource Requests ----------
def insert_resource_request(values: Tuple) -> None:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO resource_requests 
            (user_id, project_id1, purpose, hardware_resources, 
             software_resources, lab_area, needs_mentorship, mentor_name, 
             request_date, start_time, end_time, justification, status, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'pending', NOW())
            """,
            values
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()

def update_resource_request_status(request_id: int, status: str, response: str) -> None:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE resource_requests 
            SET status = %s, admin_response = %s 
            WHERE id = %s
            """ ,
            (status, response, request_id)
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()

def user_resource_requests(user_id: int) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT r.*, p.project_title, 
                   TIME_FORMAT(r.start_time, '%%H:%%i') AS start_time_str,
                   TIME_FORMAT(r.end_time, '%%H:%%i') AS end_time_str
            FROM resource_requests r 
            LEFT JOIN ongoing_projects p ON r.project_id1 = p.id 
            WHERE r.user_id = %s 
            ORDER BY r.request_date DESC
            """ ,
            (user_id,)
        )
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

def pending_resource_requests_detailed() -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT r.*, u.username, p.project_title,
                   TIME_FORMAT(r.start_time, '%%H:%%i') as start_time_str,
                   TIME_FORMAT(r.end_time, '%%H:%%i') as end_time_str
            FROM resource_requests r 
            JOIN users u ON r.user_id = u.id 
            LEFT JOIN ongoing_projects p ON r.project_id1 = p.id 
            WHERE r.status = 'pending' 
            ORDER BY r.request_date DESC, r.start_time DESC
            """
        )
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

def all_resource_requests_detailed() -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT r.*, u.username, p.project_title,
                   TIME_FORMAT(r.start_time, '%%H:%%i') as start_time_str,
                   TIME_FORMAT(r.end_time, '%%H:%%i') as end_time_str
            FROM resource_requests r 
            JOIN users u ON r.user_id = u.id 
            LEFT JOIN ongoing_projects p ON r.project_id1 = p.id 
            ORDER BY r.request_date DESC, r.start_time DESC
            """
        )
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

# ---------- Events ----------
def insert_event(values: Tuple) -> None:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO events 
            (title, excerpt, event_date, event_type, image_path, details, form_fields)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """ ,
            values
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()

def get_event_image_path(event_id: int) -> Optional[str]:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT image_path FROM events WHERE id = %s", (event_id,))
        row = cursor.fetchone()
        return row["image_path"] if row else None
    finally:
        cursor.close()
        conn.close()

def get_event_by_id(event_id: int) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM events WHERE id = %s", (event_id,))
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()

def update_event(values: Tuple) -> None:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE events 
            SET title = %s, excerpt = %s, event_date = %s, 
                event_type = %s, image_path = %s, details = %s,
                form_fields = %s
            WHERE id = %s
            """ ,
            values
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()

def get_event_form_fields(event_id: int) -> Optional[str]:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT form_fields FROM events WHERE id = %s", (event_id,))
        row = cursor.fetchone()
        return row["form_fields"] if row else None
    finally:
        cursor.close()
        conn.close()

def list_events_created_asc() -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM events ORDER BY created_at ASC")
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

def insert_event_submission(event_id: int, user_id: int, submission_json: str) -> None:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO event_submissions (event_id, user_id, submission_data)
            VALUES (%s, %s, %s)
            """ ,
            (event_id, user_id, submission_json)
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()

def delete_event(event_id: int) -> None:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM events WHERE id = %s", (event_id,))
        conn.commit()
    finally:
        cursor.close()
        conn.close()

def get_event_title(event_id: int) -> Optional[str]:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT title FROM events WHERE id = %s", (event_id,))
        row = cursor.fetchone()
        return row["title"] if row else None
    finally:
        cursor.close()
        conn.close()

def get_event_submissions_with_user(event_id: int) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT es.*, u.username 
            FROM event_submissions es
            JOIN users u ON es.user_id = u.id
            WHERE es.event_id = %s
            ORDER BY es.created_at DESC
            """ ,
            (event_id,)
        )
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

# ---------- Gallery ----------
def insert_gallery_item(title: str, event_date: str, image_path: str) -> None:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO gallery_items (title, event_date, image_path) VALUES (%s, %s, %s)",
            (title, event_date, image_path)
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()

def get_gallery_item_image_path(item_id: int) -> Optional[str]:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT image_path FROM gallery_items WHERE id = %s", (item_id,))
        row = cursor.fetchone()
        return row["image_path"] if row else None
    finally:
        cursor.close()
        conn.close()

def delete_gallery_item(item_id: int) -> None:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM gallery_items WHERE id = %s", (item_id,))
        conn.commit()
    finally:
        cursor.close()
        conn.close()

def list_gallery_items_created_asc() -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM gallery_items ORDER BY created_at ASC")
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

def list_gallery_items_desc_by_event_date() -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM gallery_items ORDER BY event_date DESC")
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()
"""Student account storage. The route layer is in admin_students.py."""

import re
import sqlite3

from werkzeug.security import generate_password_hash

from db import get_db


STUDENT_QUERY = """
    SELECT s.id, s.user_id, s.student_number, s.full_name, u.username
    FROM students AS s
    JOIN users AS u ON u.id = s.user_id
    WHERE u.role = 'student'
"""


def list_students():
    return get_db().execute(
        STUDENT_QUERY + " ORDER BY s.student_number"
    ).fetchall()


def get_student(student_id):
    return get_db().execute(
        STUDENT_QUERY + " AND s.id = ?", (student_id,)
    ).fetchone()


def _validate_student_fields(username, student_number, full_name):
    username = username.strip()
    student_number = student_number.strip()
    full_name = full_name.strip()

    if not username or not student_number or not full_name:
        raise ValueError("Username, student number, and full name are required.")

    # Do not accept spaces or punctuation that would make an identifier ambiguous.
    if not re.fullmatch(r"[A-Za-z0-9._-]{3,50}", username):
        raise ValueError(
            "Username must be 3–50 characters (letters, numbers, dot, underscore or dash)."
        )
    if not re.fullmatch(r"[A-Za-z0-9-]{3,30}", student_number):
        raise ValueError(
            "Student number must be 3–30 characters (letters, numbers or dash)."
        )
    if len(full_name) > 120:
        raise ValueError("Student name must be 120 characters or fewer.")

    return username, student_number, full_name


def _password_hash(password, required):
    if not password:
        if required:
            raise ValueError("A password is required.")
        return None
    if not password.strip():
        raise ValueError("Password cannot be only spaces.")
    if len(password) < 8:
        raise ValueError("Password must contain at least 8 characters.")
    return generate_password_hash(password)


def create_student(username, password, student_number, full_name):
    username, student_number, full_name = _validate_student_fields(
        username, student_number, full_name
    )
    password_hash = _password_hash(password, required=True)
    database = get_db()
    try:
        with database:
            user_cursor = database.execute(
                "INSERT INTO users (username, password_hash, role) "
                "VALUES (?, ?, 'student')",
                (username, password_hash),
            )
            student_cursor = database.execute(
                "INSERT INTO students (user_id, student_number, full_name) "
                "VALUES (?, ?, ?)",
                (user_cursor.lastrowid, student_number, full_name),
            )
    except sqlite3.IntegrityError as problem:
        raise ValueError(
            "Student could not be created. The username or student "
            "number may already be in use."
        ) from problem
    return student_cursor.lastrowid


def update_student(student_id, username, student_number, full_name, password=""):
    """Atomically update a student's identity and optional password.

    Leaving the password blank keeps the current hash. Never pass existing hashes
    to the HTML template, and never render submitted passwords after an error.
    """
    student = get_student(student_id)
    if student is None:
        raise ValueError("Student account not found.")

    username, student_number, full_name = _validate_student_fields(
        username, student_number, full_name
    )
    new_hash = _password_hash(password, required=False)
    database = get_db()
    try:
        with database:
            if new_hash is None:
                database.execute(
                    "UPDATE users SET username = ? WHERE id = ?",
                    (username, student["user_id"]),
                )
            else:
                database.execute(
                    "UPDATE users SET username = ?, password_hash = ? WHERE id = ?",
                    (username, new_hash, student["user_id"]),
                )
            database.execute(
                "UPDATE students SET student_number = ?, full_name = ? WHERE id = ?",
                (student_number, full_name, student_id),
            )
    except sqlite3.IntegrityError as problem:
        raise ValueError(
            "Student could not be updated. The username or student "
            "number may already be in use."
        ) from problem

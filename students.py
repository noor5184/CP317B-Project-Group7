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


def create_student(username, password, student_number, full_name):
    username = username.strip()
    student_number = student_number.strip()
    full_name = full_name.strip()

    if not username or not student_number or not full_name:
        raise ValueError(
            "Username, student number, and full name are required."
        )

    if not password or not password.strip():
        raise ValueError("A password is required.")

    password_hash = generate_password_hash(password)
    database = get_db()

    try:
        with database:
            user_cursor = database.execute(
                "INSERT INTO users (username, password_hash, role) "
                "VALUES (?, ?, 'student')",
                (username, password_hash),
            )

            student_cursor = database.execute(
                "INSERT INTO students "
                "(user_id, student_number, full_name) "
                "VALUES (?, ?, ?)",
                (user_cursor.lastrowid, student_number, full_name),
            )

    except sqlite3.IntegrityError as problem:
        raise ValueError(
            "Student could not be created. The username or student "
            "number may already be in use."
        ) from problem

    return student_cursor.lastrowid
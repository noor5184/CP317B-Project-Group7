import sqlite3

from db import get_db


def _validate_course(code, title, description):
    code = code.strip()
    title = title.strip()
    description = description.strip()

    if not code or not title:
        raise ValueError("Course code and title are required.")

    return code, title, description


def list_courses():
    return get_db().execute(
        "SELECT id, code, title, description "
        "FROM courses ORDER BY code"
    ).fetchall()


def get_course(course_id):
    return get_db().execute(
        "SELECT id, code, title, description "
        "FROM courses WHERE id = ?",
        (course_id,),
    ).fetchone()


def create_course(code, title, description=""):
    values = _validate_course(code, title, description)
    database = get_db()

    try:
        with database:
            cursor = database.execute(
                "INSERT INTO courses (code, title, description) "
                "VALUES (?, ?, ?)",
                values,
            )
    except sqlite3.IntegrityError as error:
        raise ValueError(
            "A course with that code already exists."
        ) from error

    return cursor.lastrowid


def update_course(course_id, code, title, description=""):
    values = _validate_course(code, title, description)
    database = get_db()

    try:
        with database:
            cursor = database.execute(
                "UPDATE courses "
                "SET code = ?, title = ?, description = ? "
                "WHERE id = ?",
                (*values, course_id),
            )

            if cursor.rowcount == 0:
                raise ValueError("Course not found.")

    except sqlite3.IntegrityError as error:
        raise ValueError(
            "A course with that code already exists."
        ) from error
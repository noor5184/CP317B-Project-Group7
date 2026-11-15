"""ADM-5: create, correct, and delete fictional student course completions.

Integration contract for REG-1:
    has_completed_course(student_id, course_id) -> bool
Here `student_id` means students.id (not users.id).
"""
from datetime import date
import sqlite3

from db import get_db


COMPLETION_QUERY = """
    SELECT cc.id, cc.student_id, cc.course_id, cc.completed_on,
           s.student_number, s.full_name,
           c.code AS course_code, c.title AS course_title
      FROM course_completions AS cc
      JOIN students AS s ON s.id = cc.student_id
      JOIN courses AS c ON c.id = cc.course_id
"""


def _positive_id(value, label):
    value = str(value).strip() if value is not None else ""
    if not value.isdecimal() or int(value) < 1 or int(value) > 9223372036854775807:
        raise ValueError(f"Choose a valid {label}.")
    return int(value)


def _validated_fields(student_id, course_id, completed_on):
    student_id = _positive_id(student_id, "student")
    course_id = _positive_id(course_id, "course")
    try:
        completed = date.fromisoformat(completed_on)
    except (TypeError, ValueError):
        raise ValueError("Enter a valid completion date.") from None
    if completed > date.today():
        raise ValueError("Completion date cannot be in the future.")
    database = get_db()
    for table, identifier, label in (
        ("students", student_id, "student"),
        ("courses", course_id, "course"),
    ):
        # Only trusted fixed table names above enter the SQL string.
        if database.execute(
            f"SELECT 1 FROM {table} WHERE id = ?", (identifier,)
        ).fetchone() is None:
            raise ValueError(f"The selected {label} does not exist.")
    return student_id, course_id, completed.isoformat()


def list_completions():
    return get_db().execute(
        COMPLETION_QUERY + " ORDER BY s.student_number, c.code"
    ).fetchall()


def get_completion(completion_id):
    identifier = _positive_id(completion_id, "completion record")
    return get_db().execute(
        COMPLETION_QUERY + " WHERE cc.id = ?", (identifier,)
    ).fetchone()


def has_completed_course(student_id, course_id):
    """Called by REG-1 to determine if a prerequisite was completed."""
    return get_db().execute(
        "SELECT 1 FROM course_completions WHERE student_id = ? AND course_id = ?",
        (student_id, course_id),
    ).fetchone() is not None


def create_completion(student_id, course_id, completed_on):
    fields = _validated_fields(student_id, course_id, completed_on)
    try:
        with get_db() as database:
            cursor = database.execute(
                "INSERT INTO course_completions "
                "(student_id, course_id, completed_on) VALUES (?, ?, ?)",
                fields,
            )
    except sqlite3.IntegrityError as error:
        raise ValueError("This student already has a completion for that course.") from error
    return cursor.lastrowid


def update_completion(completion_id, student_id, course_id, completed_on):
    identifier = _positive_id(completion_id, "completion record")
    fields = _validated_fields(student_id, course_id, completed_on)
    try:
        with get_db() as database:
            cursor = database.execute(
                "UPDATE course_completions SET student_id = ?, course_id = ?, "
                "completed_on = ? WHERE id = ?",
                (*fields, identifier),
            )
            if cursor.rowcount == 0:
                raise ValueError("Completion record not found.")
    except sqlite3.IntegrityError as error:
        raise ValueError("This student already has a completion for that course.") from error


def delete_completion(completion_id):
    identifier = _positive_id(completion_id, "completion record")
    with get_db() as database:
        cursor = database.execute(
            "DELETE FROM course_completions WHERE id = ?", (identifier,)
        )
        if cursor.rowcount == 0:
            raise ValueError("Completion record not found.")

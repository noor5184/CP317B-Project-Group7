from datetime import datetime
import sqlite3

from courses import get_course
from db import get_db
from terms import get_term

DAYS = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")

SECTION_QUERY = """
    SELECT s.*, c.code AS course_code, c.title AS course_title,
           t.code AS term_code, t.name AS term_name
    FROM sections AS s
    JOIN courses AS c ON c.id = s.course_id
    JOIN terms AS t ON t.id = s.term_id
"""


def _whole_number(value, label, minimum=0):
    try:
        if not str(value).strip().isdecimal():
            raise ValueError

        number = int(value)

        # SQLite stores signed 64-bit integers.
        if number < minimum or number > 9223372036854775807:
            raise ValueError

    except (TypeError, ValueError):
        raise ValueError(
            f"{label} must be a valid whole number of at least {minimum}."
        ) from None

    return number


def _validate_section(
    course_id, term_id, code, meeting_days,
    start_time, end_time, location, capacity,
):
    course_id = _whole_number(course_id, "Course ID", 1)
    term_id = _whole_number(term_id, "Term ID", 1)
    capacity = _whole_number(capacity, "Capacity")

    code = code.strip()
    location = location.strip()

    if get_course(course_id) is None:
        raise ValueError("Select an existing course.")

    if get_term(term_id) is None:
        raise ValueError("Select an existing academic term.")

    if not code or not location:
        raise ValueError("Section code and location are required.")

    if (
        not isinstance(meeting_days, (list, tuple))
        or not meeting_days
        or any(day not in DAYS for day in meeting_days)
    ):
        raise ValueError("Select valid meeting days.")

    days = ", ".join(day for day in DAYS if day in meeting_days)

    try:
        start = datetime.strptime(start_time, "%H:%M")
        end = datetime.strptime(end_time, "%H:%M")
    except (TypeError, ValueError) as error:
        raise ValueError(
            "Enter valid times in HH:MM format."
        ) from error

    if end <= start:
        raise ValueError(
            "The end time must be later than the start time."
        )

    return (
        course_id, term_id, code, days,
        start.strftime("%H:%M"), end.strftime("%H:%M"),
        location, capacity,
    )


def list_sections(term_id=None):
    query = SECTION_QUERY
    values = ()

    if term_id is not None:
        query += " WHERE s.term_id = ?"
        values = (_whole_number(term_id, "Term ID", 1),)

    query += " ORDER BY t.start_date DESC, c.code, s.code"
    return get_db().execute(query, values).fetchall()


def get_section(section_id):
    return get_db().execute(
        SECTION_QUERY + " WHERE s.id = ?",
        (section_id,),
    ).fetchone()


def create_section(
    course_id, term_id, code, meeting_days,
    start_time, end_time, location, capacity=0,
):
    values = _validate_section(
        course_id, term_id, code, meeting_days,
        start_time, end_time, location, capacity,
    )
    database = get_db()

    try:
        with database:
            cursor = database.execute(
                "INSERT INTO sections "
                "(course_id, term_id, code, meeting_days, "
                "start_time, end_time, location, capacity) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                values,
            )
    except sqlite3.IntegrityError as error:
        raise ValueError(
            "Section could not be saved. Check for a duplicate "
            "section code or an invalid course or term."
        ) from error

    return cursor.lastrowid


def update_section(
    section_id, course_id, term_id, code, meeting_days,
    start_time, end_time, location, capacity,
):
    values = _validate_section(
        course_id, term_id, code, meeting_days,
        start_time, end_time, location, capacity,
    )
    section_id = _whole_number(section_id, "Section ID", 1)
    database = get_db()

    try:
        with database:
            cursor = database.execute(
                "UPDATE sections SET course_id = ?, term_id = ?, "
                "code = ?, meeting_days = ?, start_time = ?, "
                "end_time = ?, location = ?, capacity = ? "
                "WHERE id = ?",
                (*values, section_id),
            )

            if cursor.rowcount == 0:
                raise ValueError("Section not found.")

    except sqlite3.IntegrityError as error:
        raise ValueError(
            "Section could not be saved. Check for a duplicate "
            "section code or an invalid course or term."
        ) from error
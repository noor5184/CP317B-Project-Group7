
import sqlite3
from db import get_db


def list_student_enrollments(student_id, term_id=None):
    """Return a student's confirmed enrollments, optionally limited to a term."""
    query = """
        SELECT e.id, e.student_id, e.section_id, e.registered_at,
               s.course_id, s.term_id, s.code AS section_code,
               s.meeting_days, s.start_time, s.end_time, s.location,
               c.code AS course_code, c.title AS course_title,
               t.code AS term_code, t.name AS term_name
        FROM enrollments AS e
        JOIN sections AS s ON s.id = e.section_id
        JOIN courses AS c ON c.id = s.course_id
        JOIN terms AS t ON t.id = s.term_id
        WHERE e.student_id = ?
    """
    parameters = [student_id]

    if term_id is not None:
        query += " AND s.term_id = ?"
        parameters.append(term_id)

    query += " ORDER BY t.start_date DESC, c.code, s.code"

    return get_db().execute(query, parameters).fetchall()


def count_section_enrollments(section_id):
    """Return the number of confirmed enrollments in a section."""
    row = get_db().execute(
        "SELECT COUNT(*) AS enrollment_count "
        "FROM enrollments WHERE section_id = ?",
        (section_id,),
    ).fetchone()

    return row["enrollment_count"]




def get_section_remaining_seats(section_id):
    """Return available seats, or raise an error for an unknown section."""
    section = get_db().execute(
        "SELECT capacity FROM sections WHERE id = ?",
        (section_id,),
    ).fetchone()

    if section is None:
        raise ValueError("Section not found.")

    return max(0, section["capacity"] - count_section_enrollments(section_id))


def is_course_enrolled(student_id, course_id, term_id):
    """Check whether a student is enrolled in a course during a term."""
    return get_db().execute(
        "SELECT 1 FROM enrollments AS e "
        "JOIN sections AS s ON s.id = e.section_id "
        "WHERE e.student_id = ? AND s.course_id = ? AND s.term_id = ? "
        "LIMIT 1",
        (student_id, course_id, term_id),
    ).fetchone() is not None


def sections_conflict(first, second):
    """Check for overlapping meetings within the same academic term."""
    if first["term_id"] != second["term_id"]:
        return False

    first_days = {
        day.strip() for day in first["meeting_days"].split(",")
    }
    second_days = {
        day.strip() for day in second["meeting_days"].split(",")
    }

    return bool(first_days & second_days) and (
        first["start_time"] < second["end_time"]
        and second["start_time"] < first["end_time"]
    )


def get_section_selection_error(
    section, current_enrollments, selected_sections, remaining_seats
):
    """Return an Add-button rejection reason, or None if selection is allowed."""
    for other in current_enrollments:
        if (
            other["term_id"] == section["term_id"]
            and other["course_id"] == section["course_id"]
        ):
            return (
                f"You are already registered for "
                f"{section['course_code']} in this term."
            )

    for other in selected_sections:
        if (
            other["term_id"] == section["term_id"]
            and other["course_id"] == section["course_id"]
        ):
            return (
                f"{section['course_code']} is already "
                "in your selected courses."
            )

    if remaining_seats <= 0:
        return "This section is full."

    for other in current_enrollments:
        if sections_conflict(section, other):
            return (
                "Timetable conflict with registered course "
                f"{other['course_code']}."
            )

    for other in selected_sections:
        if sections_conflict(section, other):
            return (
                "Timetable conflict with selected course "
                f"{other['course_code']}."
            )

    return None



def _registration_id(value, label):
    text = str(value).strip()

    if not text.isdecimal() or not 1 <= int(text) <= 9223372036854775807:
        raise ValueError(f"{label} must be a valid positive identifier.")

    return int(text)


def _load_registration_sections(database, term_id, section_ids):
    placeholders = ", ".join("?" for _ in section_ids)
    rows = database.execute(
        "SELECT s.*, c.code AS course_code, c.title AS course_title, "
        "t.code AS term_code, t.name AS term_name "
        "FROM sections AS s "
        "JOIN courses AS c ON c.id = s.course_id "
        "JOIN terms AS t ON t.id = s.term_id "
        f"WHERE s.id IN ({placeholders})",
        section_ids,
    ).fetchall()

    by_id = {row["id"]: row for row in rows}

    if any(section_id not in by_id for section_id in section_ids):
        raise ValueError(
            "A selected section is no longer available. "
            "Review your selections."
        )

    selected = [by_id[section_id] for section_id in section_ids]

    if any(section["term_id"] != term_id for section in selected):
        raise ValueError(
            "Submit sections from one academic term at a time."
        )

    return selected



def register_selected_sections(
    student_id, term_id, section_ids, check_requirements
):
    """Validate and save a complete selection in one transaction.

    check_requirements(student_id, term_id, selected, current) must perform
    read-only academic checks, return None on success, and raise ValueError
    with an explanation when the student is ineligible.
    """
    student_id = _registration_id(student_id, "Student ID")
    term_id = _registration_id(term_id, "Term ID")

    if not isinstance(section_ids, (list, tuple)) or not section_ids:
        raise ValueError(
            "Select at least one section before submitting."
        )

    section_ids = [
        _registration_id(value, "Section ID")
        for value in section_ids
    ]

    if len(set(section_ids)) != len(section_ids):
        raise ValueError("The same section cannot be submitted twice.")

    if not callable(check_requirements):
        raise RuntimeError(
            "An academic requirements checker must be provided."
        )

    database = get_db()

    if database.in_transaction:
        raise RuntimeError(
            "Registration must start outside an existing transaction."
        )

    try:
        database.execute("BEGIN IMMEDIATE")

        student = database.execute(
            "SELECT 1 FROM students AS s "
            "JOIN users AS u ON u.id = s.user_id "
            "WHERE s.id = ? AND u.role = 'student'",
            (student_id,),
        ).fetchone()

        if student is None:
            raise ValueError("Student profile is missing.")

        term = database.execute(
            "SELECT 1 FROM terms WHERE id = ?",
            (term_id,),
        ).fetchone()

        if term is None:
            raise ValueError("Academic term not found.")

        selected = _load_registration_sections(
            database, term_id, section_ids
        )
        current = list_student_enrollments(student_id, term_id)

        for section in selected:
            others = [
                item for item in selected
                if item["id"] != section["id"]
            ]

            error = get_section_selection_error(
                section,
                current,
                others,
                get_section_remaining_seats(section["id"]),
            )

            if error:
                raise ValueError(
                    f"{section['course_code']} "
                    f"section {section['code']}: {error}"
                )

        result = check_requirements(
            student_id, term_id, selected, current
        )

        if result is not None:
            raise RuntimeError(
                "The academic checker must return None on success."
            )

        enrollment_ids = []

        for section in selected:
            cursor = database.execute(
                "INSERT INTO enrollments "
                "(student_id, section_id) VALUES (?, ?)",
                (student_id, section["id"]),
            )
            enrollment_ids.append(cursor.lastrowid)

        database.commit()
        return enrollment_ids

    except sqlite3.IntegrityError as problem:
        database.rollback()
        raise ValueError(
            "Registration could not be saved. Review your selections."
        ) from problem

    except sqlite3.OperationalError as problem:
        database.rollback()
        code = getattr(problem, "sqlite_errorcode", 0) & 255

        if code in (sqlite3.SQLITE_BUSY, sqlite3.SQLITE_LOCKED):
            raise ValueError(
                "Registration is busy. Please try again."
            ) from problem

        raise

    except Exception:
        database.rollback()
        raise


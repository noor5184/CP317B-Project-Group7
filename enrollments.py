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


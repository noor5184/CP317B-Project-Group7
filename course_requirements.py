import sqlite3

from db import get_db
from completions import has_completed_course


def _positive_id(value, label):
    try:
        text = str(value).strip()
        if not text.isdecimal() or int(text) < 1:
            raise ValueError
        return int(text)
    except (TypeError, ValueError):
        raise ValueError(f"{label} must be a positive number.") from None


def _validate_requirement(course_id, required_course_id, requirement_type):
    course_id = _positive_id(course_id, "Course")
    required_course_id = _positive_id(
        required_course_id, "Required course"
    )

    if course_id == required_course_id:
        raise ValueError("A course cannot require itself.")

    if requirement_type not in ("prerequisite", "corequisite"):
        raise ValueError("Choose prerequisite or corequisite.")

    database = get_db()
    for course_id_to_check in (course_id, required_course_id):
        exists = database.execute(
            "SELECT id FROM courses WHERE id = ?",
            (course_id_to_check,),
        ).fetchone()

        if exists is None:
            raise ValueError("Select two existing courses.")

    return course_id, required_course_id, requirement_type


def list_requirements():
    return get_db().execute("""
        SELECT r.id, r.requirement_type,
               c.code AS course_code,
               c.title AS course_title,
               required.code AS required_course_code,
               required.title AS required_course_title
        FROM course_requirements AS r
        JOIN courses AS c ON c.id = r.course_id
        JOIN courses AS required
            ON required.id = r.required_course_id
        ORDER BY c.code, required.code
    """).fetchall()


def get_requirement(requirement_id):
    return get_db().execute(
        "SELECT * FROM course_requirements WHERE id = ?",
        (requirement_id,),
    ).fetchone()


def create_requirement(course_id, required_course_id, requirement_type):
    values = _validate_requirement(
        course_id, required_course_id, requirement_type
    )
    database = get_db()

    try:
        with database:
            cursor = database.execute(
                "INSERT INTO course_requirements "
                "(course_id, required_course_id, requirement_type) "
                "VALUES (?, ?, ?)",
                values,
            )
    except sqlite3.IntegrityError as error:
        raise ValueError(
            "That course requirement already exists."
        ) from error

    return cursor.lastrowid


def update_requirement(
    requirement_id, course_id, required_course_id, requirement_type
):
    values = _validate_requirement(
        course_id, required_course_id, requirement_type
    )
    database = get_db()

    try:
        with database:
            cursor = database.execute(
                "UPDATE course_requirements "
                "SET course_id = ?, required_course_id = ?, "
                "requirement_type = ? WHERE id = ?",
                (*values, requirement_id),
            )

            if cursor.rowcount == 0:
                raise ValueError("Requirement not found.")

    except sqlite3.IntegrityError as error:
        raise ValueError(
            "That course requirement already exists."
        ) from error


def delete_requirement(requirement_id):
    database = get_db()

    with database:
        cursor = database.execute(
            "DELETE FROM course_requirements WHERE id = ?",
            (requirement_id,),
        )

        if cursor.rowcount == 0:
            raise ValueError("Requirement not found.")
def check_registration_requirements(student_id, term_id, selected, current):
    selected_course_ids = {
        int(section["course_id"]) for section in selected
    }

    current_course_ids = {
        int(enrollment["course_id"])
        for enrollment in current
        if int(enrollment["term_id"]) == int(term_id)
    }

    for course_id in selected_course_ids:
        requirements = get_db().execute("""
            SELECT r.requirement_type, r.required_course_id,
                   c.code AS course_code,
                   required.code AS required_course_code
            FROM course_requirements AS r
            JOIN courses AS c ON c.id = r.course_id
            JOIN courses AS required
                ON required.id = r.required_course_id
            WHERE r.course_id = ?
        """, (course_id,)).fetchall()

        for requirement in requirements:
            required_id = requirement["required_course_id"]

            if requirement["requirement_type"] == "prerequisite":
                if not has_completed_course(student_id, required_id):
                    raise ValueError(
                        f"{requirement['course_code']} requires "
                        f"completed course "
                        f"{requirement['required_course_code']}."
                    )

            elif requirement["requirement_type"] == "corequisite":
                if (
                    required_id not in selected_course_ids
                    and required_id not in current_course_ids
                ):
                    raise ValueError(
                        f"{requirement['course_code']} requires "
                        f"{requirement['required_course_code']} "
                        "to be taken in the same academic term."
                    )

    return None
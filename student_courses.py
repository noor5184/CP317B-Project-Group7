"""UI-1: student-only searchable course-section catalog."""
from flask import Blueprint, abort, g, render_template, request

from auth import role_required
from course_search import search_sections
from enrollments import (
    get_section_remaining_seats, get_section_selection_error,
    list_student_enrollments,
)
from student_registration import get_selected_sections
from students import get_student_by_user_id
from terms import list_terms    

bp = Blueprint("student_courses", __name__, url_prefix="/student/courses")


@bp.get("/")
@role_required("student")
def index():
    # Do not accept a student ID in the query string. The signed-in user
    # must have a linked student profile to browse the student portal.
    student = get_student_by_user_id(g.user["id"])
    if student is None:
        abort(403, description="Student profile is missing.")

    selected_term = request.args.get("term_id", "").strip()
    query = request.args.get("q", "").strip()
    error = None
    try:
        sections = search_sections(selected_term, query)
    except ValueError as problem:
        error = str(problem)
        sections = []

    current = list_student_enrollments(student["id"])
    selected_by_term = {}
    selection_errors = {}

    for section in sections:
        term_id = section["term_id"]

        if term_id not in selected_by_term:
            selected_by_term[term_id] = get_selected_sections(term_id)

        selection_errors[section["section_id"]] = get_section_selection_error(
            section,
            current,
            selected_by_term[term_id],
            get_section_remaining_seats(section["section_id"]),
        )

    return render_template(
        "student_courses.html",
        terms=list_terms(),
        sections=sections,
        selected_term=selected_term,
        query=query,
        error=error,
        selection_errors=selection_errors,
    )

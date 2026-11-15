"""UI-1: student-only searchable course-section catalog."""
from flask import Blueprint, abort, g, render_template, request

from auth import role_required
from course_search import search_sections
from db import get_db
from terms import list_terms

bp = Blueprint("student_courses", __name__, url_prefix="/student/courses")


@bp.get("/")
@role_required("student")
def index():
    # Do not accept a student ID in the query string. The signed-in user
    # must have a linked student profile to browse the student portal.
    student = get_db().execute(
        "SELECT 1 FROM students WHERE user_id = ?", (g.user["id"],)
    ).fetchone()
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

    return render_template(
        "student_courses.html",
        terms=list_terms(),
        sections=sections,
        selected_term=selected_term,
        query=query,
        error=error,
    )

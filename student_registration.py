from flask import (
    Blueprint, abort, flash, g, redirect, render_template, session, url_for,
)

from auth import role_required
from enrollments import (
    get_section_remaining_seats, get_section_selection_error,
    list_student_enrollments,
)
from sections import get_section
from students import get_student_by_user_id
from terms import get_term, list_terms

bp = Blueprint(
    "student_registration", __name__, url_prefix="/student/registration"
)

def _current_student():
    student = get_student_by_user_id(g.user["id"])

    if student is None:
        abort(403, description="Student profile is missing.")

    return student


def _save_selection(term_id, section_ids):
    selections = dict(session.get("registration_selections", {}))
    key = str(term_id)

    if section_ids:
        selections[key] = section_ids
    else:
        selections.pop(key, None)

    if selections:
        session["registration_selections"] = selections
    else:
        session.pop("registration_selections", None)


def get_selected_sections(term_id):
    stored_ids = session.get("registration_selections", {}).get(
        str(term_id), []
    )
    sections = [get_section(section_id) for section_id in stored_ids]
    sections = [
        section for section in sections
        if section is not None and section["term_id"] == term_id
    ]
    valid_ids = [section["id"] for section in sections]

    if valid_ids != stored_ids:
        _save_selection(term_id, valid_ids)
        flash(
            "Some selections are no longer offered in this term "
            "and were removed.",
            "error",
        )

    return sections


def _term_or_404(term_id):
    if not 0 < term_id <= 9223372036854775807:
        abort(404)

    term = get_term(term_id)

    if term is None:
        abort(404)

    return term


@bp.get("/", defaults={"term_id": None})
@bp.get("/<int:term_id>")
@role_required("student")
def selections(term_id):
    student = _current_student()
    terms = list_terms()

    if term_id is None and terms:
        return redirect(url_for(
            "student_registration.selections",
            term_id=terms[0]["id"],
        ))

    term = _term_or_404(term_id) if term_id is not None else None
    selected = get_selected_sections(term_id) if term is not None else []
    current = (
        list_student_enrollments(student["id"], term_id)
        if term is not None else []
    )
    selection_errors = {}

    for section in selected:
        others = [
            item for item in selected
            if item["id"] != section["id"]
        ]
        selection_errors[section["id"]] = get_section_selection_error(
            section, current, others,
            get_section_remaining_seats(section["id"]),
        )

    return render_template(
        "registration_selections.html",
        student=student,
        terms=terms,
        term=term,
        selected_sections=selected,
        selection_errors=selection_errors,
    )


@bp.post("/add/<int:section_id>")
@role_required("student")
def add_selection(section_id):
    student = _current_student()

    if not 0 < section_id <= 9223372036854775807:
        abort(404)

    section = get_section(section_id)

    if section is None:
        abort(404)

    term_id = section["term_id"]
    selected = get_selected_sections(term_id)
    error = get_section_selection_error(
        section,
        list_student_enrollments(student["id"], term_id),
        selected,
        get_section_remaining_seats(section_id),
    )

    if error:
        flash(error, "error")
    else:
        _save_selection(
            term_id,
            [item["id"] for item in selected] + [section_id],
        )
        flash(
            f"{section['course_code']} added to your selections.",
            "success",
        )

    return redirect(url_for(
        "student_registration.selections",
        term_id=term_id,
    ))


@bp.post("/<int:term_id>/remove/<int:section_id>")
@role_required("student")
def remove_selection(term_id, section_id):
    _current_student()
    _term_or_404(term_id)
    selected = get_selected_sections(term_id)
    remaining_ids = [
        item["id"] for item in selected
        if item["id"] != section_id
    ]

    if len(remaining_ids) == len(selected):
        flash("That section is not in your selections.", "error")
    else:
        _save_selection(term_id, remaining_ids)
        flash("Section removed from your selections.", "success")

    return redirect(url_for(
        "student_registration.selections",
        term_id=term_id,
    ))
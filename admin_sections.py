from flask import (
    Blueprint, abort, flash, redirect, render_template, request, url_for,
)

from auth import role_required
from courses import list_courses
from sections import DAYS, create_section, get_section, update_section
from terms import list_terms

bp = Blueprint("admin_sections", __name__, url_prefix="/admin/sections")


@bp.route("/new", defaults={"section_id": None}, methods=("GET", "POST"))
@bp.route("/<int:section_id>/edit", methods=("GET", "POST"))
@role_required("admin")
def section_form(section_id):
    is_edit = section_id is not None
    section = get_section(section_id) if is_edit else None

    if is_edit and section is None:
        abort(404)

    if is_edit:
        values = dict(section)
        values["meeting_days"] = [
            day.strip() for day in section["meeting_days"].split(",")
        ]
    else:
        values = {
            "course_id": "",
            "term_id": "",
            "code": "",
            "meeting_days": [],
            "start_time": "",
            "end_time": "",
            "location": "",
            "capacity": "0",
        }

    error = None

    if request.method == "POST":
        values = {
            key: request.form.get(key, "")
            for key in (
                "course_id", "term_id", "code", "start_time",
                "end_time", "location", "capacity",
            )
        }

        values["meeting_days"] = request.form.getlist("meeting_days")

        arguments = (
            values["course_id"], values["term_id"], values["code"],
            values["meeting_days"], values["start_time"],
            values["end_time"], values["location"], values["capacity"],
        )

        try:
            if is_edit:
                update_section(section_id, *arguments)
            else:
                section_id = create_section(*arguments)

        except ValueError as problem:
            error = str(problem)

        else:
            flash("Section updated." if is_edit else "Section created.")
            return redirect(
                url_for("admin_sections.section_form", section_id=section_id)
            )

    return render_template(
        "section_form.html",
        page_title="Edit section" if is_edit else "Add section",
        section=values,
        is_edit=is_edit,
        error=error,
        courses=list_courses(),
        terms=list_terms(),
        days=DAYS,
    )
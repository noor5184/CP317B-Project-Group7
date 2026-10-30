from flask import (
    Blueprint, abort, flash, redirect, render_template, request, url_for,
)

from auth import role_required
from courses import create_course, get_course, update_course

bp = Blueprint("admin_courses", __name__, url_prefix="/admin/courses")


@bp.route("/new", defaults={"course_id": None}, methods=("GET", "POST"))
@bp.route("/<int:course_id>/edit", methods=("GET", "POST"))
@role_required("admin")
def course_form(course_id):
    is_edit = course_id is not None
    course = get_course(course_id) if is_edit else None

    if is_edit and course is None:
        abort(404)

    values = (
        dict(course) if is_edit
        else {"code": "", "title": "", "description": ""}
    )
    error = None

    if request.method == "POST":
        values = {
            "code": request.form.get("code", ""),
            "title": request.form.get("title", ""),
            "description": request.form.get("description", ""),
        }
        arguments = (
            values["code"], values["title"], values["description"],
        )

        try:
            if is_edit:
                update_course(course_id, *arguments)
            else:
                course_id = create_course(*arguments)

        except ValueError as problem:
            error = str(problem)

        else:
            flash("Course updated." if is_edit else "Course created.")
            return redirect(
                url_for("admin_courses.course_form", course_id=course_id)
            )

    return render_template(
        "course_form.html",
        page_title="Edit course" if is_edit else "Add course",
        course=values,
        is_edit=is_edit,
        error=error,
    )
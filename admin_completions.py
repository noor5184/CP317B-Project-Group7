"""ADM-5: administrator-only completion management routes."""
from datetime import date

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

from auth import role_required
from completions import (
    create_completion, delete_completion, get_completion,
    list_completions, update_completion,
)
from courses import list_courses
from students import list_students

bp = Blueprint("admin_completions", __name__, url_prefix="/admin/completions")


def _form_data():
    return {
        "student_id": request.form.get("student_id", ""),
        "course_id": request.form.get("course_id", ""),
        "completed_on": request.form.get("completed_on", ""),
    }


def _show_form(completion=None, error=None):
    return render_template(
        "completion_form.html", completion=completion,
        is_edit=completion is not None and completion.get("id") is not None,
        students=list_students(), courses=list_courses(),
        today=date.today().isoformat(), error=error,
    )


@bp.get("/")
@role_required("admin")
def index():
    return render_template("completions.html", completions=list_completions())


@bp.route("/new", methods=("GET", "POST"))
@role_required("admin")
def new():
    completion = {"student_id": "", "course_id": "", "completed_on": date.today().isoformat()}
    if request.method == "POST":
        completion = _form_data()
        try:
            create_completion(**completion)
        except ValueError as problem:
            return _show_form(completion, str(problem))
        flash("Course completion saved.")
        return redirect(url_for("admin_completions.index"))
    return _show_form(completion)


@bp.route("/<int:completion_id>/edit", methods=("GET", "POST"))
@role_required("admin")
def edit(completion_id):
    existing = get_completion(completion_id)
    if existing is None:
        abort(404)
    completion = dict(existing)
    if request.method == "POST":
        completion.update(_form_data())
        try:
            update_completion(completion_id, completion["student_id"],
                              completion["course_id"], completion["completed_on"])
        except ValueError as problem:
            return _show_form(completion, str(problem))
        flash("Course completion updated.")
        return redirect(url_for("admin_completions.index"))
    return _show_form(completion)


@bp.post("/<int:completion_id>/delete")
@role_required("admin")
def remove(completion_id):
    try:
        delete_completion(completion_id)
    except ValueError as problem:
        flash(str(problem))
    else:
        flash("Course completion removed.")
    return redirect(url_for("admin_completions.index"))

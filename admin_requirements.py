from flask import (
    Blueprint, abort, flash, redirect, render_template, request, url_for,
)

from auth import role_required
from courses import list_courses
from course_requirements import (
    list_requirements, get_requirement,
    create_requirement, update_requirement, delete_requirement,
)

bp = Blueprint(
    "admin_requirements",
    __name__,
    url_prefix="/admin/requirements",
)


def show_form(requirement, error=None, is_edit=False):
    return render_template(
        "requirement_form.html",
        requirement=requirement,
        error=error,
        is_edit=is_edit,
        courses=list_courses(),
        requirement_types=("prerequisite", "corequisite"),
    )


@bp.get("/")
@role_required("admin")
def index():
    return render_template(
        "requirements.html",
        requirements=list_requirements(),
    )


@bp.route("/new", methods=("GET", "POST"))
@role_required("admin")
def new():
    requirement = {
        "course_id": "",
        "required_course_id": "",
        "requirement_type": "prerequisite",
    }

    if request.method == "POST":
        requirement = {
            "course_id": request.form.get("course_id", ""),
            "required_course_id": request.form.get(
                "required_course_id", ""
            ),
            "requirement_type": request.form.get(
                "requirement_type", ""
            ),
        }

        try:
            create_requirement(**requirement)
        except ValueError as problem:
            return show_form(requirement, str(problem))

        flash("Registration requirement added.")
        return redirect(url_for("admin_requirements.index"))

    return show_form(requirement)


@bp.route("/<int:requirement_id>/edit", methods=("GET", "POST"))
@role_required("admin")
def edit(requirement_id):
    existing = get_requirement(requirement_id)

    if existing is None:
        abort(404)

    requirement = dict(existing)

    if request.method == "POST":
        requirement.update({
            "course_id": request.form.get("course_id", ""),
            "required_course_id": request.form.get(
                "required_course_id", ""
            ),
            "requirement_type": request.form.get(
                "requirement_type", ""
            ),
        })

        try:
            update_requirement(
                requirement_id,
                requirement["course_id"],
                requirement["required_course_id"],
                requirement["requirement_type"],
            )
        except ValueError as problem:
            return show_form(requirement, str(problem), True)

        flash("Registration requirement updated.")
        return redirect(url_for("admin_requirements.index"))

    return show_form(requirement, is_edit=True)


@bp.post("/<int:requirement_id>/delete")
@role_required("admin")
def remove(requirement_id):
    try:
        delete_requirement(requirement_id)
    except ValueError as problem:
        flash(str(problem), "error")
    else:
        flash("Registration requirement removed.")

    return redirect(url_for("admin_requirements.index"))
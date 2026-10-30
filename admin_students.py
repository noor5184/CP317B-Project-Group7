"""ADM-3.2 - Admin-only student account creation and maintenance."""

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

from auth import role_required
from students import create_student, get_student, list_students, update_student

bp = Blueprint("admin_students", __name__, url_prefix="/admin/students")


@bp.get("/")
@role_required("admin")
def student_list():
    return render_template("student_list.html", students=list_students())


@bp.route("/new", defaults={"student_id": None}, methods=("GET", "POST"))
@bp.route("/<int:student_id>/edit", methods=("GET", "POST"))
@role_required("admin")
def student_form(student_id):
    is_edit = student_id is not None
    existing = get_student(student_id) if is_edit else None
    if is_edit and existing is None:
        abort(404)

    student = (
        dict(existing)
        if is_edit
        else {"username": "", "student_number": "", "full_name": ""}
    )
    error = None
    if request.method == "POST":
        student = {
            key: request.form.get(key, "")
            for key in ("username", "student_number", "full_name")
        }
        password = request.form.get("password", "")
        try:
            if is_edit:
                update_student(
                    student_id, student["username"], student["student_number"],
                    student["full_name"], password,
                )
            else:
                student_id = create_student(
                    student["username"], password, student["student_number"],
                    student["full_name"],
                )
        except ValueError as problem:
            error = str(problem)
        else:
            flash("Student account updated." if is_edit else "Student account created.")
            return redirect(url_for("admin_students.student_form", student_id=student_id))

    return render_template(
        "student_form.html",
        student=student,
        is_edit=is_edit,
        error=error,
        page_title="Edit student account" if is_edit else "Add student account",
    )

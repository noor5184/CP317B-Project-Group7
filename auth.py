from functools import wraps
import secrets

from flask import (
    Blueprint, abort, g, redirect, render_template,
    request, session, url_for,
)
from werkzeug.security import check_password_hash

from db import get_db

bp = Blueprint("auth", __name__)


@bp.before_app_request
def load_user():
    g.user = None
    user_id = session.get("user_id")

    if user_id is not None:
        g.user = get_db().execute(
            "SELECT id, username, role FROM users WHERE id = ?",
            (user_id,),
        ).fetchone()

        if g.user is None:
            session.clear()


def csrf_token():
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_urlsafe(32)
    return session["csrf_token"]


@bp.app_context_processor
def template_helpers():
    return {"csrf_token": csrf_token}


@bp.before_app_request
def check_form_token():
    if request.method == "POST":
        expected = session.get("csrf_token", "")
        supplied = request.form.get("csrf_token", "")

        if not expected or not secrets.compare_digest(
            expected.encode("utf-8"), supplied.encode("utf-8")
        ):
            abort(
                400,
                description="The form expired. Reload the page and try again.",
            )


def portal_url(role):
    endpoint = (
        "auth.admin_portal" if role == "admin"
        else "auth.student_portal"
    )
    return url_for(endpoint)


def role_required(role):
    def decorate(view):
        @wraps(view)
        def wrapped_view(*args, **kwargs):
            if g.user is None:
                return redirect(url_for("auth.login"))

            if g.user["role"] != role:
                abort(403)

            return view(*args, **kwargs)

        return wrapped_view

    return decorate


@bp.get("/")
def index():
    if g.user is None:
        return redirect(url_for("auth.login"))

    return redirect(portal_url(g.user["role"]))


@bp.route("/login", methods=("GET", "POST"))
def login():
    if g.user is not None:
        return redirect(portal_url(g.user["role"]))

    error = None
    username = ""

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username or not password:
            error = "Enter both your username and password."
        else:
            user = get_db().execute(
                "SELECT id, username, password_hash, role "
                "FROM users WHERE username = ?",
                (username,),
            ).fetchone()

            if user is None or not check_password_hash(
                user["password_hash"], password
            ):
                error = "Invalid username or password."
            else:
                session.clear()
                session["user_id"] = user["id"]
                return redirect(portal_url(user["role"]))

    return render_template(
        "login.html",
        error=error,
        username=username,
    )


@bp.get("/admin")
@role_required("admin")
def admin_portal():
    return render_template(
        "portal.html",
        title="Administrator Portal",
        student=None,
    )


@bp.get("/student")
@role_required("student")
def student_portal():
    student = get_db().execute(
        "SELECT student_number, full_name "
        "FROM students WHERE user_id = ?",
        (g.user["id"],),
    ).fetchone()

    if student is None:
        abort(403, description="Student profile is missing.")

    return render_template(
        "portal.html",
        title="Student Portal",
        student=student,
    )


@bp.post("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))


@bp.after_app_request
def prevent_page_caching(response):
    if response.mimetype == "text/html":
        response.headers["Cache-Control"] = "no-store"
    return response
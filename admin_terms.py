"""ADM-4.2 - Administrator screens for academic term management."""

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

from auth import role_required
from terms import create_term, get_term, list_terms, update_term

bp = Blueprint("admin_terms", __name__, url_prefix="/admin/terms")


@bp.get("/")
@role_required("admin")
def term_list():
    return render_template("term_list.html", terms=list_terms())


@bp.route("/new", defaults={"term_id": None}, methods=("GET", "POST"))
@bp.route("/<int:term_id>/edit", methods=("GET", "POST"))
@role_required("admin")
def term_form(term_id):
    is_edit = term_id is not None
    existing = get_term(term_id) if is_edit else None
    if is_edit and existing is None:
        abort(404)

    term = (
        dict(existing)
        if is_edit
        else {"code": "", "name": "", "start_date": "", "end_date": ""}
    )
    error = None
    if request.method == "POST":
        term = {
            key: request.form.get(key, "")
            for key in ("code", "name", "start_date", "end_date")
        }
        values = (term["code"], term["name"], term["start_date"], term["end_date"])
        try:
            if is_edit:
                update_term(term_id, *values)
            else:
                term_id = create_term(*values)
        except ValueError as problem:
            error = str(problem)
        else:
            flash("Academic term updated." if is_edit else "Academic term created.")
            return redirect(url_for("admin_terms.term_form", term_id=term_id))

    return render_template(
        "term_form.html",
        term=term,
        is_edit=is_edit,
        error=error,
        page_title="Edit academic term" if is_edit else "Add academic term",
    )

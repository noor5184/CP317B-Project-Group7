from datetime import date
import sqlite3

from db import get_db


def _validate_term(code, name, start_date, end_date):
    code = code.strip()
    name = name.strip()

    if not code or not name:
        raise ValueError("Term code and name are required.")

    try:
        start = date.fromisoformat(start_date)
        end = date.fromisoformat(end_date)
    except (TypeError, ValueError) as error:
        raise ValueError(
            "Enter valid dates in YYYY-MM-DD format."
        ) from error

    if end < start:
        raise ValueError(
            "The end date cannot be earlier than the start date."
        )

    return code, name, start.isoformat(), end.isoformat()


def list_terms():
    return get_db().execute(
        "SELECT id, code, name, start_date, end_date "
        "FROM terms ORDER BY start_date DESC, code"
    ).fetchall()


def get_term(term_id):
    return get_db().execute(
        "SELECT id, code, name, start_date, end_date "
        "FROM terms WHERE id = ?",
        (term_id,),
    ).fetchone()


def create_term(code, name, start_date, end_date):
    values = _validate_term(code, name, start_date, end_date)
    database = get_db()

    try:
        with database:
            cursor = database.execute(
                "INSERT INTO terms (code, name, start_date, end_date) "
                "VALUES (?, ?, ?, ?)",
                values,
            )
    except sqlite3.IntegrityError as error:
        raise ValueError(
            "A term with that code already exists."
        ) from error

    return cursor.lastrowid


def update_term(term_id, code, name, start_date, end_date):
    values = _validate_term(code, name, start_date, end_date)
    database = get_db()

    try:
        with database:
            cursor = database.execute(
                "UPDATE terms "
                "SET code = ?, name = ?, start_date = ?, end_date = ? "
                "WHERE id = ?",
                (*values, term_id),
            )

            if cursor.rowcount == 0:
                raise ValueError("Term not found.")

    except sqlite3.IntegrityError as error:
        raise ValueError(
            "A term with that code already exists."
        ) from error
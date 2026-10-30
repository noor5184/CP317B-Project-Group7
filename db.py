import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash


def get_db():
    """Return the database connection for the current application context."""
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(error=None):
    """Close the connection when the application context ends."""
    database = g.pop("db", None)
    if database is not None:
        database.close()


@click.command("init-db")
@with_appcontext
def init_db_command():
    """Create missing tables using schema.sql."""
    database = get_db()

    with current_app.open_resource("schema/schema.sql") as schema_file:
        database.executescript(schema_file.read().decode("utf-8"))

    database.commit()
    click.echo("Database initialized: " + current_app.config["DATABASE"])

@click.command("seed-demo")
@with_appcontext
def seed_demo_command():
    """Create fictional demo accounts, leaving existing users unchanged."""
    database = get_db()

    demo_accounts = [
        ("admin", "AdminDemo123!", "admin", None, None),
        ("student1", "StudentDemo123!", "student", "TEST1001", "Alex Cruz"),
        ("student2", "StudentDemo123!", "student", "TEST1002", "Sam Rivera"),
    ]

    created = 0

    with database:
        for username, password, role, student_number, full_name in demo_accounts:
            existing = database.execute(
                "SELECT id FROM users WHERE username = ?",
                (username,),
            ).fetchone()

            if existing is not None:
                continue

            cursor = database.execute(
                "INSERT INTO users (username, password_hash, role) "
                "VALUES (?, ?, ?)",
                (username, generate_password_hash(password), role),
            )

            if role == "student":
                database.execute(
                    "INSERT INTO students (user_id, student_number, full_name) "
                    "VALUES (?, ?, ?)",
                    (cursor.lastrowid, student_number, full_name),
                )

            created += 1

    click.echo(f"Created {created} demo account(s). Existing users were unchanged.")


def init_app(app):
    """Register database cleanup and initialization commands."""
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(seed_demo_command)
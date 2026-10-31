# REgistro

**University Course Registration System**  
**CP317B Software Engineering - Group 7 - Fall 2026**

REgistro is a university course registration project with student and administrator areas in one Flask application. Sprint 01 provides a working authentication and academic-administration prototype connected to SQLite.

**Current status:** The Sprint 01 features below are implemented and have passed development and integration checks. Formal acceptance testing results and final story acceptance remain pending.

**Team:** Ali Noormohammadi, Oneel Jaba, Milap Devang Shah  
**Product Owner:** Ali Noormohammadi

## Current Features

- Shared login with password-hash verification and redirection to the appropriate portal.
- Logout for student and administrator accounts.
- Server-side role restrictions on administrator pages and submitted actions.
- Student access to their own linked profile, showing name and student number.
- Administrator listings and creation/editing forms for academic terms, courses, sections, and student accounts.
- Section listings filtered by academic term.
- Validation of required fields, duplicate identifiers, academic dates, section meeting details, related records, capacities, and student account inputs.
- Persistent saved records and transactions that keep linked login/student changes consistent.

The current student portal displays a profile. Student search, registration, withdrawal, schedules, seat availability, and enrollment reporting are planned for later sprints.

## Requirements

- Python 3.14. The project has been verified on Windows with Python 3.14.5.
- Git or GitHub Desktop to obtain the repository.
- A web browser.

Python dependencies are pinned in [requirements.txt](requirements.txt), including Flask 3.1.3. The application uses Python's `sqlite3` module for its local database.

## Setup and Run - Windows CMD

Run the commands from the repository root, which contains `app.py` and `requirements.txt`. The commands below use the environment's Python directly, so activating the environment is unnecessary.

### 1. Clone the repository

Clone with GitHub Desktop, or run:

```bat
git clone https://github.com/noor5184/CP317B-Project-Group7.git
cd CP317B-Project-Group7
```

If you already cloned the repository, open CMD in that existing project folder and continue with the next step.

### 2. Create the Python environment and install dependencies

```bat
py -3.14 -m venv .venv
```

```bat
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 3. Initialize the database and create demonstration accounts

```bat
.\.venv\Scripts\python.exe -m flask --app app init-db
```

```bat
.\.venv\Scripts\python.exe -m flask --app app seed-demo
```

`init-db` reads `schema/schema.sql` and creates missing tables. `seed-demo` creates the fictional accounts listed below, leaving existing usernames unchanged.

**These commands do not create academic terms, courses, or sections.** A fresh database needs those records before a section can be saved; see the first-run walkthrough below.

### 4. Start the application

```bat
.\.venv\Scripts\python.exe -m flask --app app run --debug
```

Open **[http://127.0.0.1:5000](http://127.0.0.1:5000)** in your browser. Keep the terminal open while using the application. Press **Ctrl+C** in that terminal to stop the server.

This command runs the local development server for the prototype demonstration. On subsequent runs, use the same start command; recreating the environment and demonstration accounts is not required.

## Demonstration Accounts

The following credentials are created by `seed-demo` in a fresh database:

| Role | Username | Password | Student profile |
|---|---|---|---|
| Administrator | `admin` | `AdminDemo123!` | Not applicable |
| Student | `student1` | `StudentDemo123!` | Alex Cruz - TEST1001 |
| Student | `student2` | `StudentDemo123!` | Sam Rivera - TEST1002 |

These are fictional local demonstration accounts. If an existing account's details or password have been changed, running `seed-demo` again does not reset them.

## First-Run Walkthrough

For a fresh database:

1. Sign in as **admin**. The administrator dashboard links to the four management listings.
2. Open **Manage academic terms**, choose **Add term**, and create a term. Example: code `DEMO2026`, name `Demo Term`, start date `2026-09-01`, end date `2026-12-31`.
3. Open **Manage courses**, choose **Add course**, and create a course. Example: code `DEMO101`, title `Demo Programming`, with an optional fictional description.
4. Open **Manage sections**, choose **Add section**, and select that course and term. Example: section code `01`, meeting days **Mon/Wed**, start `09:00`, end `09:50`, location `Demo Room 101`, capacity `30`.
5. Confirm that the saved records appear in their listings and can be reopened through **Edit**. On the section listing, choose the term and click **Filter**; **Clear** restores the unfiltered listing.
6. Open **Manage student accounts** to inspect the fictional student records. **Add student** creates a linked login/profile; editing permits an optional new password. New passwords must have at least eight characters. Leaving the password empty during editing keeps the existing password.
7. Log out and sign in as `student1` or `student2`. The portal should display that account's own name and student number, with no administrator management links.

Academic term dates must be valid and ordered. Sections require an existing course and term, valid meeting days/times, and a non-negative integer capacity. Student usernames must be 3-50 ASCII letters, digits, dots, underscores, or hyphens; student numbers must be 3-30 ASCII letters, digits, or hyphens. Full validation details are documented in [docs/design.md](docs/design.md).

## Useful Pages

Use these paths after starting the application:

| Page | Path | Required role |
|---|---|---|
| Login | `/login` | None |
| Administrator dashboard | `/admin` | Administrator |
| Academic terms | `/admin/terms/` | Administrator |
| Courses | `/admin/courses/` | Administrator |
| Sections | `/admin/sections/` | Administrator |
| Student accounts | `/admin/students/` | Administrator |
| Own student profile | `/student` | Student |

The management listings provide Add and Edit links. Use the visible **Log out** button to end a session; logout is a POST action rather than a page to open through the address bar.

## Local Data and Git

- The application stores its database at `instance/registro.sqlite` and its persistent session-signing key at `instance/secret_key`.
- `instance/`, `.venv/`, and `__pycache__/` are excluded by `.gitignore`.
- Each developer has their own database. Pulling application changes does not copy another teammate's saved courses, terms, sections, or accounts.
- `init-db` creates missing tables without deleting existing records. It does not migrate the structure of existing tables.
- `seed-demo` creates missing demonstration accounts; it does not seed academic offerings or reset existing accounts.
- If moving to a new clone and retaining local records, copy the existing `instance/` folder while the application is stopped, and recreate the Python environment in its new location.

## Project Structure

| File or directory | Purpose |
|---|---|
| `app.py` | Application configuration and blueprint registration. |
| `auth.py` | Login/logout, portals, role checks, form-token checks, and session-derived profile access. |
| `admin_*.py` | Administrator listing and creation/editing routes. |
| `courses.py`, `sections.py`, `terms.py`, `students.py` | Validation and database operations for their record types. |
| `db.py` | SQLite connections and the database/demo initialization commands. |
| `schema/schema.sql` | Definitions and constraints for the five current tables. |
| `templates/` | Jinja pages and the shared management layout. |
| `static/site.css` | Styles used by the shared layout. |
| `requirements.txt` | Pinned Python dependencies. |
| `docs/design.md` | Current design, data model, requirements, verification summary, and planned work. |

## Verification and Troubleshooting

Development checks have covered browser workflows, Flask shell/database operations, and request-level tests. They include login/logout, persistence, duplicate rejection, linked-account rollback, administrator navigation, role restrictions on GET/POST requests, and current student profile ownership. Formal acceptance results belong in the Sprint 01 report and Excel backlog and remain pending at this revision.

| Symptom | Check or action |
|---|---|
| `ModuleNotFoundError: No module named 'flask'` | Use the `.venv` Python commands above and install `requirements.txt` into that environment. |
| SQLite reports `no such table` | Run `init-db`, then `seed-demo` where needed, using the same checkout and environment as the application. |
| The academic term or course dropdown is empty | Create the missing term/course through its management page. The demonstration-account command does not create these records. |
| A management page reports `BuildError` for `admin_courses.course_list` or `admin_sections.section_list` | Confirm the checkout includes the integrated listing routes, restart the server, and ensure it is running from the updated project folder. Reinitializing the database does not create missing Flask endpoints. |
| A form reports that it expired | Reload the form and submit it again from the current signed-in browser session. |
| Old demonstration records are absent after cloning | Check which project's `instance/registro.sqlite` is being used. Local database contents are not transferred through Git. |

## Planned Work

The Milestone 02 backlog schedules student course search, registration, prerequisite/corequisite management, and course-completion records for Sprint 02. Withdrawal, schedules, seat availability, enrollment reports, student visibility of registration requirements, and the final accessibility review are planned for Sprint 03.

Section capacity is currently stored and validated; enforcement against actual enrollment and remaining-seat calculations require the planned enrollment features. Waitlists, payments, grades/transcripts, full multi-university support, and public hosting are outside the current committed prototype scope unless the group changes its plan.

See [docs/design.md](docs/design.md) for the detailed design and open decisions. The Excel product backlog is the authoritative record of story priorities, assignments, acceptance criteria, and current statuses.

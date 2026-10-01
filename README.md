# CP317B-Project-Group7
University Course Registration System for CP317B Software Engineering 
# University Course Registration System

**CP317B Software Engineering · Group 7 · Fall 2026**

**REgistro TM:**

Collaborators:

Ali Noormohammadi, Oneel Jaba, Milap Devang Shah

A university course registration portal being developed as a group software engineering project. Students will be able to find course sections, register or withdraw, and view their schedules. Administrators will manage the information and rules that make registration possible.

> **Project status:** Planning and design. The repository does not contain a runnable application yet.

## Planned first release

**Students**

- Sign in and browse course sections by academic term.
- See section details and available seats.
- Register for or withdraw from a section.
- View a schedule of registered classes.

**Administrators**

- Manage student accounts, courses, terms, and sections.
- Set section capacities and course prerequisites.
- View enrollment counts and remaining seats.

The registration process will enforce capacity, prevent duplicate active enrollments, and check configured prerequisites. The first version will demonstrate one example institution. Features such as waitlists, grades, payments, and full multi university support are outside the initial scope.

## Provisional implementation

| Component | Current choice |
|---|---|
| Application | One Python Flask web application |
| Interface | Jinja rendered HTML and CSS, with separate student and administrator areas |
| Storage | SQLite initially |
| Access | One account system with server enforced roles |

These choices may be refined as the team works through the course milestones. A local browser demonstration is the initial deployment target; public hosting has not been decided.

## Project documentation

The current scope, draft backlog, data model, user flows, and open decisions are in [docs/design.md](docs/design.md). That document is a working draft and may change as requirements become clearer.

## Development

The application setup and run instructions will be added when the first executable version is committed. This project uses GitHub for version control and follows the course's Scrum milestones.
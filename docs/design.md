# REgistro - Design Document

**University Course Registration System**  
**Course:** CP317B Software Engineering, Fall 2026  
**Group:** 7  
**Team:** Ali Noormohammadi, Oneel Jaba, Milap Devang Shah  
**Product Owner:** Ali Noormohammadi  
**Updated:** October 30, 2026  
**Status:** Sprint 01 prototype implemented; development and integration checks completed for the current features. Formal acceptance results remain pending.  
**Repository:** [CP317B-Project-Group7](https://github.com/noor5184/CP317B-Project-Group7)

This document describes the integrated Sprint 01 implementation and the design direction for later sprints. A feature described as planned is not part of the current prototype. The Excel product backlog remains the authoritative record of story priorities, assignments, estimates, acceptance criteria, and statuses.

## 1. Project Concept

REgistro is a browser-based university course registration system with student and administrator areas in one application. Its intended complete workflow allows students to browse course sections, check requirements and availability, register or withdraw, and view their schedules. Administrators maintain the academic information and student records needed for those workflows.

Sprint 01 establishes the application foundation: shared authentication, logout, role permissions, student profile ownership, and administrator management of academic terms, courses, sections, and fictional student accounts. The student portal currently displays the profile associated with the signed-in account. Student course search and registration workflows are planned for later sprints.

The course project demonstrates one example institution. Academic terms, courses, sections, and student accounts are stored as editable data rather than being fixed in the page templates. The current schema does not include an institution table or support multiple institutions. Full multi-university support remains a possible future extension.

## 2. Core Scope

### 2.1 Implemented in Sprint 01

- One Flask application with a persistent SQLite database.
- A shared login system that verifies password hashes and redirects users to the appropriate portal.
- Logout controls for both roles that clear the authenticated session.
- Server-side administrator restrictions on management pages and submitted actions.
- A student portal that retrieves only the signed-in student's linked profile.
- Administrator listings and creation/editing forms for academic terms, courses, sections, and student accounts.
- Section listings that can be filtered by academic term.
- Validation of required fields, duplicate identifiers, academic dates, section relationships, meeting days and times, capacities, and student account inputs.
- Transactions that keep linked user and student records consistent during account creation and editing.
- Fictional demonstration accounts for local development and testing.

Sections store capacity, but the prototype does not yet store enrollments or calculate occupied and remaining seats.

### 2.2 Planned for Later Sprints

- Student course/section browsing and search by course code or name within a selected term.
- Configurable prerequisite and corequisite relationships.
- Student course-completion records for eligibility checks.
- Registration with checks for identity, capacity, duplicate course enrollment, and academic requirements.
- Withdrawal, personal schedules, seat availability, and administrator enrollment reports.
- Student visibility of configured registration requirements.
- A final accessibility review across the main workflows.

Registration failures should identify the reason for rejection. Registration and seat assignment must eventually be coordinated so that competing requests cannot both claim the final seat. These are planned requirements, not current implementation claims.

### 2.3 Possible Future Extensions

Waitlists, tuition and payments, grades, transcripts, degree audits, multi-university onboarding, automated notifications, a separate faculty role, and public hosting are outside the current committed prototype scope unless the group explicitly adds them to its plan.

## 3. Current Technical Design

### 3.1 Technology and Deployment

| Component | Current implementation |
|---|---|
| Application | One Python Flask application |
| Interface | HTML and CSS rendered with Jinja templates |
| Database | SQLite, accessed through Python's `sqlite3` module |
| Database location | `instance/registro.sqlite` |
| Authentication | Password-hash verification and Flask sessions |
| Authorization | Server-side role checks and session-derived student identity |
| Demonstration environment | Browser connected to a local Flask development server |

The implementation uses SQL queries directly; it does not use an ORM. Public deployment is not part of the current local demonstration setup.

### 3.2 Module Responsibilities

| File or directory | Responsibility |
|---|---|
| `app.py` | Creates/configures Flask, establishes the instance paths and signing key, and registers database helpers and blueprints. |
| `auth.py` | Loads the signed-in user, verifies credentials, handles portals/logout, checks roles and form tokens, and sets HTML cache-control headers. |
| `db.py` | Opens/closes SQLite connections, enables foreign keys, and provides `init-db` and `seed-demo` commands. |
| `admin_terms.py` | Administrator term listing and creation/editing routes. |
| `admin_courses.py` | Administrator course listing and creation/editing routes. |
| `admin_sections.py` | Administrator section listing, term filtering, and creation/editing routes. |
| `admin_students.py` | Administrator student listing and account creation/editing routes. |
| `terms.py`, `courses.py`, `sections.py`, `students.py` | Record lookup/listing, input validation, and database creation/update operations for each record type. |
| `schema/schema.sql` | Defines the five implemented tables and database constraints. |
| `templates/` | Login, portals, management lists, forms, and the shared management layout. |
| `static/site.css` | Styles pages that use the shared layout. |

Routes enforce permissions, read request values, call the data functions, and render feedback or redirect after a successful save. Data functions perform validation and parameterized SQL operations. Templates display the values and messages supplied by the routes.

The shared `base.html` layout is used by the management listings and term/student forms. Login, portal, course-form, and section-form templates currently remain standalone pages. The administrator dashboard links to all four management listings; each listing provides its corresponding creation and edit navigation.

### 3.3 Routes and Request Handling

| Route | Methods | Purpose |
|---|---|---|
| `/` | GET | Redirect to login or the signed-in user's portal. |
| `/login` | GET, POST | Display the login form and verify credentials. |
| `/logout` | POST | Clear the session and redirect to login; a valid form token is required. |
| `/admin` | GET | Administrator dashboard. |
| `/student` | GET | Display the authenticated student's own profile. |

Administrator resources use these prefixes:

| Resource | Prefix |
|---|---|
| Academic terms | `/admin/terms` |
| Courses | `/admin/courses` |
| Sections | `/admin/sections` |
| Student accounts | `/admin/students` |

For each resource, `GET <prefix>/` opens its listing, while `<prefix>/new` and `<prefix>/<id>/edit` support GET and POST for creation and editing. All these routes require the administrator role. The edit identifier refers to that resource's record; student management URLs use `students.id`, not `users.id`.

The section listing accepts an optional `term_id` query parameter. An empty value lists all sections; a valid positive integer filters by term. Invalid numeric input returns HTTP 400. An unknown but valid numeric term ID produces an empty listing.

With a valid form token where required, unauthenticated requests to protected routes redirect to login and requests from the wrong role receive HTTP 403. Missing records requested through authorized edit routes return HTTP 404. Invalid or missing POST form tokens return HTTP 400 before the route runs.

### 3.4 Persistence and Local Setup

`init-db` reads `schema/schema.sql` and creates missing tables. The schema uses `CREATE TABLE IF NOT EXISTS`; this command does not provide migrations for changing the structure of existing tables.

`seed-demo` creates one fictional administrator and two fictional student accounts, including their linked student profiles. Existing usernames are left unchanged. It does not create academic terms, courses, or sections. Those records must be created locally through the management forms or development data functions. A fresh database can therefore have working logins but an empty academic-term dropdown until a term is created.

Each developer's database is local. Git distributes the application and schema, not saved demonstration records. The database and persistent signing key are stored in the ignored `instance/` directory. `.venv/` and `__pycache__/` are also ignored. Installation and run commands belong in the README.

### 3.5 Validation and Saved Changes

| Record type | Current server-side checks |
|---|---|
| Academic term | Nonblank code/name; valid dates; end date not earlier than start; unique code. |
| Course | Nonblank code/title; unique code; optional description. |
| Section | Existing course/term; nonblank code/location; at least one valid meeting day; valid times with end later than start; non-negative whole-number capacity within SQLite's signed integer range; unique code within its course and term. |
| Student account | Nonblank identity fields; unique username/student number; username 3-50 ASCII letters, digits, dots, underscores, or hyphens; student number 3-30 ASCII letters, digits, or hyphens; full name at most 120 characters. |
| Student password | Required for creation; at least eight characters when supplied; cannot consist only of spaces. An empty password during editing preserves the existing hash. |

Identifier/name fields handled by these validators are trimmed. Passwords are not trimmed before hashing. Browser controls provide additional input guidance, while backend checks remain responsible for accepting or rejecting saved values.

Invalid input is displayed as a validation error. Successful saves are committed and redirect to the saved record's edit page with a confirmation message. User and student inserts/updates share one transaction: if the linked profile operation fails, changes to the login record, including a replacement password hash, are rolled back too.

## 4. Users

### 4.1 Student

Currently, a student can sign in, view their own name and student number, and log out. The profile is selected using the authenticated user's database ID rather than a supplied username, student number, or other requested identity. Student accounts cannot use administrator management routes, including direct edit URLs and submitted actions.

Later student capabilities include searching sections, viewing requirements and availability, registering, withdrawing, and viewing a personal schedule. Those future routes must also derive ownership from the authenticated account.

### 4.2 Administrator

Currently, an administrator can list, create, and edit academic terms, courses, sections, and student accounts. Student account editing supports identity changes and optional password replacement. These forms do not create administrator accounts or change a student's role.

Later administrative capabilities include registration-requirement configuration, course-completion records, and enrollment reporting. Capacity is currently editable as section data; preventing reductions below actual enrollment will require the planned enrollment functionality.

### 4.3 Additional Roles

A separate faculty/professor role is not implemented. The prototype uses the two roles permitted by the current schema: `student` and `admin`.

## 5. Data Model

### 5.1 Implemented Tables

| Table | Stored columns |
|---|---|
| `users` | `id`, `username`, `password_hash`, `role` |
| `students` | `id`, `user_id`, `student_number`, `full_name` |
| `terms` | `id`, `code`, `name`, `start_date`, `end_date` |
| `courses` | `id`, `code`, `title`, `description` |
| `sections` | `id`, `course_id`, `term_id`, `code`, `meeting_days`, `start_time`, `end_time`, `location`, `capacity` |

Every table has an integer primary key named `id`. Usernames, term codes, and course codes have case-insensitive uniqueness. Section-code uniqueness is case-insensitive within the same course and term. Student numbers are unique under the current schema's default text comparison.

The main relationships are:

- `students.user_id` references `users.id` and is unique. Each student profile belongs to one login account, and one account can have at most one student profile. Normal student creation inserts both records together; administrator accounts have no student profile.
- `sections.course_id` references `courses.id`. A course can have multiple sections.
- `sections.term_id` references `terms.id`. A term can contain multiple sections.
- `(course_id, term_id, code)` is unique. The same section code can be reused for a different course or term.

Database checks restrict roles to `student` or `admin`, require term end dates not to precede start dates, require section end times to follow start times, and require capacity to be a non-negative integer. SQLite foreign-key enforcement is enabled for application connections. Backend validation adds checks such as accepted meeting days and the existence of selected related records.

Student profile IDs and login IDs are separate identifiers. Authentication uses `users.id`; the student portal locates its profile through `students.user_id`. This distinction prevents account lookup from depending on an assumed equality between the two primary keys.

### 5.2 Planned Data Model Extensions

| Proposed entity or relationship | Purpose and current position |
|---|---|
| Prerequisite/corequisite relationships | Configurable links between courses, planned under ADM-2. Exact schema is not implemented. |
| Course-completion records | Link fictional students to completed courses for eligibility checking, planned under ADM-5. Exact schema is not implemented. |
| Enrollment | Connect a student to a section and support active enrollment/withdrawal, capacity counts, schedules, and reporting. Exact schema and withdrawal-history handling still need to be finalized. |
| Institution | A possible future name/code record if institutional configuration is expanded. No institution table or institution-management screen currently exists. |

The future enrollment model must prevent duplicate active course enrollments within a term and coordinate eligibility checks with seat assignment. The current section table's uniqueness constraint prevents duplicate section definitions; it does not implement student enrollment rules.

## 6. Main User Flows

### 6.1 Login and Own Profile - Implemented

1. The user opens the login form and submits credentials with a valid form token.
2. The server looks up the username and verifies the submitted password against its hash.
3. A successful login clears the prior session, stores the authenticated user ID, and redirects according to the database role.
4. An administrator receives the management dashboard. A student receives the profile linked to their authenticated user ID.
5. Invalid credentials display an error without authenticating the user.

### 6.2 Logout - Implemented

1. The user submits the logout form from their portal or shared navigation.
2. The server validates the form token, clears the session, and redirects to login.
3. Later requests to protected pages require authentication again.

### 6.3 Academic Term, Course, and Section Management - Implemented

1. The administrator opens the appropriate management listing from the dashboard/navigation.
2. They select Add or Edit and submit the required values.
3. For a section, they select an existing course and term and provide its meeting details, location, and capacity.
4. The server checks permissions, the form token, field validity, duplicate identifiers, and required relationships.
5. A valid save is committed and opens the edit page with confirmation. Invalid input displays feedback without saving the rejected change.
6. The administrator can return to listings and filter sections by academic term.

### 6.4 Student Account Management - Implemented

1. The administrator opens the student listing and selects Add or Edit.
2. Creation requires a username, password, student number, and full name. Editing permits a blank password to keep the existing credential.
3. The server validates the submitted fields and creates or updates the linked login and student records in one transaction.
4. A duplicate or other rejected linked change rolls back the transaction and displays an error.
5. A successful save opens the edit page with confirmation. The account can authenticate using its saved credentials, and its portal displays the linked profile.

### 6.5 Student Registration - Planned

1. The student signs in, chooses a term, and searches/browses available sections.
2. They inspect section details, configured academic requirements, and availability.
3. On a registration request, the server verifies identity, existing course enrollment within the term, prerequisite/corequisite eligibility, and remaining capacity.
4. Eligibility checks and seat assignment must be coordinated so competing requests cannot exceed capacity.
5. Success saves one enrollment and updates the schedule/counts. Rejection leaves enrollment data unchanged and explains the reason.

### 6.6 Student Withdrawal and Reporting - Planned

The student selects one of their own enrolled sections and confirms withdrawal. The server must verify ownership and apply the approved withdrawal rules before changing enrollment and releasing the seat. The schedule, availability, and administrator report must then agree with saved enrollment data.

The backlog proposes blocking a withdrawal that would break a retained course's corequisite dependency. The exact corequisite and withdrawal-history policies remain design decisions to finalize before implementation.

## 7. Product Backlog and Sprint Alignment

Sprint 01 selected six high-priority stories totaling **20 story points**:

| Story ID | Title | Points | Current implementation |
|---|---|---:|---|
| AUTH-1 | User Login | 5 | Credentials, password verification, sessions, and portal redirection implemented. |
| AUTH-2 | User Logout | 1 | Logout and subsequent protected-access restrictions implemented. |
| AUTH-3 | Role Based Access | 3 | Current page/action permissions and student profile ownership implemented. |
| ADM-4 | Manage Academic Terms | 3 | Term listings, creation/editing, validation, and persistence implemented. |
| ADM-1 | Manage Course Offerings | 5 | Course/section forms, listings, navigation, term filtering, and persistence implemented. |
| ADM-3 | Manage Student Records | 3 | Student account creation/editing, validation, linked transactions, and persistence implemented. |

Implementation and development verification do not by themselves establish final story acceptance. Oneel's formal testing results remain pending at this revision, and Ali, as Product Owner, must record acceptance against the backlog criteria. ADM-1 integration with student search will be checked when UI-1 is implemented. Ownership controls must extend to enrollment/schedule features as those are added.

The Milestone 02 backlog assigns the following later work:

| Planned sprint | Stories |
|---|---|
| Sprint 02 | UI-1 Course Search; REG-1 Course Registration; ADM-2 Manage Registration Requirements; ADM-5 Maintain Course Completion Records. |
| Sprint 03 | REG-2 Course Withdrawal; UI-2 View Schedule; UI-3 View Course Availability; REP-1 Enrollment Report; UI-4 View Registration Requirements; UI-5 Accessible Forms and Navigation. |

The Excel backlog governs any subsequent changes to this plan. Its task-level statuses and the Sprint 01 report should reflect actual completed work and acceptance evidence.

## 8. Ethical, Security, and Quality Considerations

### 8.1 Student Privacy and Role Permissions

Demonstrations use fictional student information. Administrator routes check the authenticated user's role on the server, including submitted actions. Hiding a navigation link is supplementary to these checks.

The student portal queries the profile associated with the signed-in `users.id`; query parameters cannot select another student's profile. A student account without a linked profile is rejected with HTTP 403. The same ownership principle must be applied to future schedules, enrollments, and withdrawals.

### 8.2 Account and Request Security

- Passwords are stored as hashes using Werkzeug's password helpers and verified against those hashes at login.
- Student lookup/listing functions do not return password hashes to management templates. Password fields are not repopulated with submitted passwords after validation errors.
- Flask sessions carry the authenticated user ID. The application reloads the current user and role from the database on each request; a missing user clears the session.
- Successful login clears the prior session, and logout clears the authenticated session. The configured session cookie uses `SameSite=Lax`.
- POST requests require a session-matching form token, including login, logout, and administrator saves.
- A generated signing key is persisted under `instance/` and excluded from Git with the database.
- Parameterized SQL is used for record values.
- HTML responses use `Cache-Control: no-store`.

These describe the local prototype's implemented controls, not a completed production-security assessment.

### 8.3 Correctness and Fairness

Current validation, unique constraints, foreign keys, and transactions protect the five-table model from rejected inputs and incomplete linked account changes. Rollback checks confirm that failed student creation/editing does not leave partial login or identity changes.

Future registration must apply consistent rules to every student, reject duplicate course enrollment, prevent over-capacity enrollment, and explain rejected operations. Enrollment concurrency and capacity reductions below active enrollment cannot be verified until enrollment functionality exists.

### 8.4 Usability and Accessibility

Current pages provide labelled controls, required-field guidance, text feedback, empty-list messages, and administrator navigation. Some templates use status/alert roles for messages. These are useful foundations, but a complete keyboard, focus, contrast, and error-feedback review has not been established as complete. UI-5 reserves the final accessibility review and fixes; accessibility should also be considered during ongoing development.

## 9. Open Questions

The following remain relevant for later sprints:

- Should timetable conflicts block registration, or should the initial schedule be display-only?
- What exact schema and correction workflow will represent course-completion records?
- Should withdrawal preserve historical enrollment records, and how will active/withdrawn states be represented?
- Should the proposed corequisite rule accept prior completion or concurrent enrollment in the same term? How will withdrawal dependencies be enforced?
- How will capacity reductions be checked against actual enrollment, and how will competing registration requests be coordinated?
- Will public hosting be required beyond the current local demonstration target?

These questions do not change the implemented Sprint 01 scope. Decisions should be reflected in the backlog and design before the affected features are finalized.

## 10. Development Progress and Verification

### 10.1 Current Progress

The application foundation, authentication, administrator management screens, data operations, and dashboard/listing navigation are implemented. Integration resolved missing course/section listing endpoints, connected the term/student blueprints and student-update logic, and placed the stylesheet in Flask's static directory.

Development verification has used manual browser checks, Flask shell queries, and request-level checks with Flask's test client. Checks have covered authentication/logout, saved records, validation, linked-account rollback, and management navigation. Ali's final permissions and current-profile ownership checks passed.

### 10.2 Verified Access and Ownership Behaviour

| Check | Recorded development result |
|---|---|
| Administrator dashboard, listings, creation pages, and existing edit pages | Authorized pages open. |
| Student direct requests to administrator pages | HTTP 403. |
| Logged-out requests to protected pages | Redirect to login. |
| Student POSTs to four creation and four existing-record edit endpoints, using valid form tokens | All eight rejected with HTTP 403. |
| Logged-out POSTs to the same eight endpoints, using valid form tokens | All eight redirected to login. |
| Database dump before/after those denied POSTs | Unchanged. |
| Separate sessions for the two demonstration students | Each displays its own profile. |
| Attempts to request the other student's identity through profile query parameters | The signed-in student's own profile remains displayed. |

The denied POST checks tested the role guard before record processing; they were not a substitute for valid-input acceptance tests of administrator saves. The profile checks cover the current portal, not enrollment or schedule functionality that has not yet been built.

### 10.3 Remaining Review

Oneel's formal acceptance results must be recorded against the six selected stories. Ali will review the evidence as Product Owner before marking stories accepted. Any failed or incomplete criterion remains pending, and later integration changes require rechecking affected behaviour.

The Sprint 01 report, Excel backlog, and team blog should be updated with the final evidence, task statuses, and actual work performed. Detailed test commands/results can be retained in `docs/testing.md`. This design document supports those records; it does not replace the required submission report or acceptance record.

## 11. Current Decisions

- One Python Flask web application serves both student and administrator areas.
- One shared authentication system and SQLite database support the prototype.
- Jinja templates provide the browser interface, with administrator navigation connected to all four management listings.
- The demonstration uses one example institution and fictional accounts/academic data; no multi-institution model is implemented.
- Current student functionality is login, own-profile display, and logout. Registration-related student features remain planned.
- Administrators can maintain terms, courses, sections, and student identity/login records. Prerequisite/corequisite configuration and completion records remain planned.
- Student account creation always assigns the student role. The current student-management form does not manage administrator roles.
- Local demonstration is the current deployment target; public hosting is undecided.
- Ali Noormohammadi is Product Owner for Group 7. Oneel's formal test results and final story acceptance remain pending at this revision.
- Existing FR/NFR identifiers are retained below. Backlog clarifications and implementation status are recorded separately from their requirement definitions.

## 12. Requirements Refinement and Implementation Status

The functional and non-functional definitions below retain the existing requirement IDs, titles, and wording. They describe the intended system as a whole. Sections 12.3 and 12.4 identify current coverage and the additional clarifications in the Milestone 02 backlog.

### 12.1 Functional Requirements

#### FR-01: User Authentication

The system shall allow students and administrators to securely sign in using their account credentials. The system shall identify the user's role and direct them to the appropriate student or administrator area.

#### FR-02: Course Search and Browsing

The system shall allow students to search and browse available course sections for an academic term. Students shall be able to view relevant course and section information.

#### FR-03: View Course Availability

The system shall display section capacity, enrollment information, and the number of remaining seats so that students can determine whether space is available before attempting registration.

#### FR-04: Course Registration

The system shall allow a student to register for an available course section. Before completing registration, the system shall check the student's identity, existing enrollment, prerequisites, and remaining capacity.

#### FR-05: Registration Rule Validation

The system shall prevent enrollment when a section is full, when the student already has an active enrollment in that section, or when required prerequisites have not been satisfied. If registration fails, the system shall display a clear reason.

#### FR-06: Course Withdrawal

The system shall allow students to withdraw from a section in which they are currently enrolled. After withdrawal, the system shall update the student's enrollment record and make the released seat available again.

#### FR-07: View Student Schedule

The system shall allow students to view their registered course sections and associated meeting times in a personal schedule.

#### FR-08: Manage Course Offerings

The system shall allow administrators to create and modify academic terms, courses, sections, section capacities, and course prerequisites.

#### FR-09: Manage Student Records

The system shall allow authorized administrators to create and maintain student account and record information required for course registration.

#### FR-10: Enrollment Reporting

The system shall allow administrators to view enrollment counts and remaining seats for course sections so that registration levels can be monitored.

### 12.2 Non-Functional Requirements

#### NFR-01: Security

The system shall use authenticated sessions and role-based access control. Students shall not be able to access administrator functions by manually entering administrator URLs. Passwords should be stored as hashes rather than plaintext.

#### NFR-02: Privacy

Students shall only be able to access their own schedules and enrollment information. Private student information shall only be accessible to authorized users, and demonstration data should use fictional student information.

#### NFR-03: Usability

The application shall provide clear and understandable student and administrator interfaces. Registration failures and other errors should explain what went wrong so that users understand the action required.

#### NFR-04: Accessibility

Forms and controls should use clear labels, support keyboard navigation, maintain readable visual contrast, and communicate errors without relying only on colour.

#### NFR-05: Data Integrity and Correctness

The system shall maintain consistent enrollment and capacity information. Registration and seat assignment should occur together so that two registration requests cannot both claim the final available seat.

### 12.3 Current Coverage

| Requirement | Sprint 01 position |
|---|---|
| FR-01 User Authentication | Login and role-appropriate portals implemented; logout is additionally covered by AUTH-2. Formal story acceptance pending. |
| FR-02 Course Search and Browsing | Student search/browsing planned under UI-1. Current administrator listings do not complete this student requirement. |
| FR-03 View Course Availability | Planned under UI-3. Section capacity alone is not a remaining-seat calculation. |
| FR-04 Course Registration | Planned under REG-1. |
| FR-05 Registration Rule Validation | Enrollment eligibility/capacity enforcement planned under REG-1 and ADM-2, supported by ADM-5. Current form validation does not complete this requirement. |
| FR-06 Course Withdrawal | Planned under REG-2. |
| FR-07 View Student Schedule | Planned under UI-2. The current student profile is not a class schedule. |
| FR-08 Manage Course Offerings | Partially implemented: term, course, section, and capacity management work; prerequisite/corequisite configuration remains planned under ADM-2. |
| FR-09 Manage Student Records | Student identity/login creation and editing implemented under ADM-3. Course-completion records remain planned separately under ADM-5. |
| FR-10 Enrollment Reporting | Planned under REP-1. |
| NFR-01 Security | Session, role, form-token, and password-hash controls implemented for current routes; formal acceptance pending. |
| NFR-02 Privacy | Current profile ownership verified. Future enrollment/schedule ownership must be implemented and tested with those features. |
| NFR-03 Usability | Current forms/navigation provide basic feedback; full registration-workflow feedback remains planned. |
| NFR-04 Accessibility | Labelled controls and text feedback provide a foundation; final workflow review/fixes remain planned under UI-5. |
| NFR-05 Data Integrity and Correctness | Current database constraints and linked-account transactions implemented. Enrollment consistency and concurrent final-seat handling remain planned. |

### 12.4 Backlog Clarifications for Later Implementation

The expanded Milestone 02 backlog adds detail to the original definitions without renumbering them:

- **REG-1 and ADM-2:** Academic eligibility includes configurable prerequisites and corequisites. Duplicate enrollment prevention applies to multiple sections of the same course within one term. Capacity and eligibility must be rechecked when registration is submitted.
- **ADM-5:** Course-completion records are maintained separately from student account identity/login information and provide the evidence needed for prerequisite checks.
- **REG-2:** Withdrawal requires confirmation. Blocking withdrawal when it would break a retained corequisite dependency is a proposed policy to finalize before implementation.
- **UI-4:** Students will be able to inspect configured prerequisite/corequisite information when planning their selections.
- **UI-5:** A final review will cover keyboard operation, visible focus, descriptive labels, useful validation feedback, and messages understandable without colour alone.

The proposed rule that a corequisite may be satisfied by prior completion or current enrollment in the same term remains an open policy decision. 

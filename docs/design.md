UNIVERSITY COURSE REGISTRATION SYSTEM
DESIGN AND IDEAS DOCUMENT

Status: Working draft
Course: CP317B Software Engineering, Fall 2026

1. PROJECT CONCEPT

The project is a browser based university course registration system with student and administrator areas in one application. Administrators maintain the academic information used for registration. Students can search for course sections, see available seats, register or withdraw, and view their schedules.

The system should be configurable rather than hard coded for one university's courses and policies. For the course project, the first working version can demonstrate one example institution. Full support for multiple universities is a possible future extension, not a requirement we are committing to now.


2. CORE SCOPE

The working system should allow the team to demonstrate:

- An example institution with academic terms, courses, sections, student accounts, and administrator accounts.
- One sign in system that sends students and administrators to their appropriate portal areas.
- Student course search and browsing, including section information and available seats.
- Registration for and withdrawal from course sections.
- A student schedule showing registered sections and meeting times.
- Basic registration rules, including capacity limits, duplicate enrollment prevention, and configured prerequisites.
- Administrator management of course offerings, capacities, prerequisites, and student records.
- An administrator report showing enrollment and remaining seats by section.

Registration failures should give a clear reason, such as a full section or an unmet prerequisite.

Ideas for later include waitlists, tuition, grades, transcripts, degree audits, multiple university onboarding, automated notifications, and public hosting. These should not be described as promised features unless the group decides to build them.


3. PROVISIONAL TECHNICAL DESIGN

Deployment environment: Server based web application, initially demonstrated through a browser connected to a local server.

Programming language: Python.

Web framework: Flask.

Graphical interface: HTML and CSS pages rendered with Jinja templates.

Database: SQLite initially.

Application structure: One Flask application, one account system, and one database. Student and administrator pages are separate parts of that application, with access determined by the signed in user's role.

The browser pages should handle interaction and display. Python service modules should handle registration rules. Database models and data access should handle persistent information. A student must not gain administrator access by manually entering an administrator URL.


4. USERS

Student

A student can browse sections, check availability, register, withdraw, and view their own schedule. A student must not be able to view or change another student's private enrollment information.

Administrator

An administrator can maintain institutional information, student accounts, course offerings, capacities, prerequisites, and enrollment reports. Administrator actions require an authenticated administrator account.

A separate faculty or professor role is an idea for later. For the first version, the administrator role can perform the management functions described in the assignment.


5. INITIAL DATA MODEL

Institution
- Name and code.
- The prototype can begin with one example institution.

User
- Login identifier, password hash, and role.
- Student and administrator accounts use the same authentication system.

Student
- Student number, name, and linked user account.
- A student owns enrollment records.

Term
- Academic term name and relevant dates or ordering.

Course
- Course code, title, and description.
- A course is a catalog entry, such as CP317.

Section
- A specific offering of a course in a term.
- Includes a section identifier, capacity, and meeting information.
- Students register for sections rather than for the abstract course.

Prerequisite
- A relationship between a course and a course that must be completed first.

Enrollment
- Connects a student to a section.
- Records whether the student is currently enrolled or has withdrawn.

Completed Course or Eligibility Record
- Records enough academic history to check prerequisites.
- The exact approach still needs to be chosen by the group.

The model must prevent duplicate active enrollments and enrollment beyond section capacity. Registration checks and seat assignment should happen together so that two requests cannot both claim the final seat.


6. MAIN USER FLOWS

Student registration

1. The student signs in.
2. The student chooses a term and searches or browses available sections.
3. The student selects a section and requests registration.
4. The system checks the student's identity, existing enrollment, prerequisites, and remaining capacity.
5. If registration succeeds, the system saves the enrollment and updates the schedule and seat count.
6. If registration fails, the system explains the reason.

Student withdrawal

1. The student opens their current schedule.
2. The student selects one of their enrolled sections and requests withdrawal.
3. The system verifies that the enrollment belongs to that student.
4. The system updates the enrollment and releases the seat.
5. The student's schedule and the section's availability are updated.

Administrator maintenance

1. The administrator signs in.
2. The administrator creates or edits terms, courses, sections, capacities, prerequisites, and student records.
3. The administrator views enrollment counts and available seats.
4. The system validates changes that could conflict with existing enrollments.


7. INITIAL PRODUCT BACKLOG

Story ID | Story Title | User Story

AUTH-1 | User Login | As a user, I want to securely log in to the system so that I can access features and information associated with my account.

UI-1 | Course Search | As a student, I want to search and browse available courses so that I can find courses that fit my academic needs.

REG-1 | Course Registration | As a student, I want to register for an available course section so that I can enroll in courses for the academic term.

REG-2 | Course Withdrawal | As a student, I want to withdraw from a registered course so that I can modify my course enrollment when necessary.

UI-2 | View Schedule | As a student, I want to view my current course schedule so that I can keep track of my registered classes and meeting times.

UI-3 | View Course Availability | As a student, I want to view the number of available seats in a course section so that I can determine whether I am able to register.

ADM-1 | Manage Course Offerings | As an administrator, I want to create and modify course offerings so that students have accurate course information available during registration.

ADM-2 | Manage Registration Requirements | As an administrator, I want to configure course prerequisites and class capacities so that registration follows the university's academic requirements.

ADM-3 | Manage Student Records | As an administrator, I want to create and maintain student account information so that eligible students can access and use the registration system.

REP-1 | Enrollment Report | As an administrator, I want to view course enrollment reports so that I can monitor enrollment levels and available course capacity.

This is the Milestone 1 draft of 10 stories. Milestone 2 will provide the template and instructions for story points, sprint assignments, status, and more detailed story breakdowns.


8. ETHICAL AND QUALITY CONSIDERATIONS

Student privacy
Students should see only their own schedules and private records. Administrator access should be limited by role. Demonstrations should use fictional student information.

Account security
Passwords should be stored as hashes, not plaintext. The application should use authenticated sessions, validate input, protect actions that change data, and keep secrets out of the Git repository.

Fairness and correctness
The same registration rules should apply to every student. The system should handle the final available seat consistently and explain why a registration attempt was rejected.

Accessibility
Forms and controls should have clear labels, support keyboard use, maintain readable contrast, and communicate errors without relying on color alone.


9. OPEN QUESTIONS

- Does the group agree that the first version supports one example institution, while remaining configurable enough to avoid hard-coded course data?
- Should timetable conflicts block registration in the first version, or should the schedule initially be display-only?
- How will the prototype record completed courses for prerequisite checks?
- Should withdrawn enrollments remain in the database as history?
- What should happen if an administrator lowers section capacity below the number already enrolled?
- How much student account management is needed for the demonstration?
- Is a locally demonstrated web application sufficient, or does the group want to host it publicly?
- Who will be Product Owner, and what are the group ID, member roles, and GitHub repository link?


10. DEVELOPMENT SEQUENCE IDEA

1. Agree on project scope, complete Milestone 1, establish the Git repository, and begin the team blog.
2. Define requirements and acceptance criteria; create the required UML and design diagrams.
3. Build the application shell, database, example data, authentication, and role permissions.
4. Implement administrator course and section management, then student browsing.
5. Implement registration and withdrawal, including tests for capacity, duplicates, and prerequisites.
6. Add schedules, enrollment reports, interface polish, and a repeatable demonstration dataset.

This sequence is an idea, not the official sprint plan. The team should follow the later milestone instructions when they are released.


11. CURRENT DECISIONS

Agreed direction:
- One web application with student and administrator areas.
- One shared backend, account system, and database.
- No separate Tkinter application is planned.

Provisional implementation:
- Python, Flask, Jinja rendered HTML/CSS, and SQLite.  
- Local server demonstration initially; public hosting is undecided.

Proposed scope:
- Demonstrate one configurable example institution.
- Treat full multi university support as a possible future extension.

12. REQUIREMENTS REFINEMENT

The University Course Registration System is designed to provide students and administrators with a centralized web-based system for managing university course registration. Students will be able to sign in, browse available course sections, view seat availability, register for or withdraw from sections, and view their current class schedules. Administrators will be responsible for managing courses, academic terms, sections, student accounts, registration requirements, and enrollment information.   

The system will use a single authentication system for both students and administrators. After signing in, users will be directed to the appropriate area of the application depending on their role. Registration will be controlled by rules such as section capacity, duplicate enrollment prevention, and prerequisite requirements. If registration cannot be completed, the system should clearly explain the reason to the student.    

- Functional Requirements

FR-01: User Authentication

The system shall allow students and administrators to securely sign in using their account credentials. The system shall identify the user's role and direct them to the appropriate student or administrator area.

FR-02: Course Search and Browsing

The system shall allow students to search and browse available course sections for an academic term. Students shall be able to view relevant course and section information.    

FR-03: View Course Availability

The system shall display section capacity, enrollment information, and the number of remaining seats so that students can determine whether space is available before attempting registration.    

FR-04: Course Registration

The system shall allow a student to register for an available course section. Before completing registration, the system shall check the student's identity, existing enrollment, prerequisites, and remaining capacity.    

FR-05: Registration Rule Validation

The system shall prevent enrollment when a section is full, when the student already has an active enrollment in that section, or when required prerequisites have not been satisfied. If registration fails, the system shall display a clear reason.    

FR-06: Course Withdrawal

The system shall allow students to withdraw from a section in which they are currently enrolled. After withdrawal, the system shall update the student's enrollment record and make the released seat available again.    

FR-07: View Student Schedule

The system shall allow students to view their registered course sections and associated meeting times in a personal schedule.    

FR-08: Manage Course Offerings

The system shall allow administrators to create and modify academic terms, courses, sections, section capacities, and course prerequisites.    

FR-09: Manage Student Records

The system shall allow authorized administrators to create and maintain student account and record information required for course registration.    

FR-10: Enrollment Reporting

The system shall allow administrators to view enrollment counts and remaining seats for course sections so that registration levels can be monitored.    

- Non-Functional Requirements

NFR-01: Security

The system shall use authenticated sessions and role-based access control. Students shall not be able to access administrator functions by manually entering administrator URLs. Passwords should be stored as hashes rather than plaintext.    

NFR-02: Privacy

Students shall only be able to access their own schedules and enrollment information. Private student information shall only be accessible to authorized users, and demonstration data should use fictional student information.    

NFR-03: Usability

The application shall provide clear and understandable student and administrator interfaces. Registration failures and other errors should explain what went wrong so that users understand the action required.    

NFR-04: Accessibility

Forms and controls should use clear labels, support keyboard navigation, maintain readable visual contrast, and communicate errors without relying only on colour.    

NFR-05: Data Integrity and Correctness

The system shall maintain consistent enrollment and capacity information. Registration and seat assignment should occur together so that two registration requests cannot both claim the final available seat.  

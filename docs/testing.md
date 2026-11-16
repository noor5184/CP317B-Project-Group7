TEST: (DB persistance):
----------------------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------------------
Microsoft Windows [Version 10.0.26200.9711]
(c) Microsoft Corporation. All rights reserved.

C:\Users\alinm\OneDrive\Documents\school\cs\CP317\CP317B-Project-Group7>.\.venv\Scripts\python.exe -m flask --app app init-db
Database initialized: C:\Users\alinm\OneDrive\Documents\school\cs\CP317\CP317B-Project-Group7\instance\registro.sqlite

C:\Users\alinm\OneDrive\Documents\school\cs\CP317\CP317B-Project-Group7>set PYTHON_BASIC_REPL=1

C:\Users\alinm\OneDrive\Documents\school\cs\CP317\CP317B-Project-Group7>.\.venv\Scripts\python.exe -m flask --app app shell
Python 3.14.5 (tags/v3.14.5:5607950, May 10 2026, 10:43:50) [MSC v.1944 64 bit (AMD64)] on win32
App: app
Instance: C:\Users\alinm\OneDrive\Documents\school\cs\CP317\CP317B-Project-Group7\instance
>>> from terms import create_term, get_term, list_terms, update_term
>>> term_id = create_term("DEMO2026", "Demo Term", "2026-09-01", "2026-12-31")
>>> dict(get_term(term_id))
{'id': 1, 'code': 'DEMO2026', 'name': 'Demo Term', 'start_date': '2026-09-01', 'end_date': '2026-12-31'}
>>> update_term(term_id, "DEMO2026", "Updated Demo Term", "2026-09-01", "2026-12-30")
>>> [dict(term) for term in list_terms()]
[{'id': 1, 'code': 'DEMO2026', 'name': 'Updated Demo Term', 'start_date': '2026-09-01', 'end_date': '2026-12-30'}]
>>> exit
Use exit() or Ctrl-Z plus Return to exit
>>> exit()
now exiting InteractiveConsole...

C:\Users\alinm\OneDrive\Documents\school\cs\CP317\CP317B-Project-Group7>set PYTHON_BASIC_REPL=1

C:\Users\alinm\OneDrive\Documents\school\cs\CP317\CP317B-Project-Group7>.\.venv\Scripts\python.exe -m flask --app app shell
Python 3.14.5 (tags/v3.14.5:5607950, May 10 2026, 10:43:50) [MSC v.1944 64 bit (AMD64)] on win32
App: app
Instance: C:\Users\alinm\OneDrive\Documents\school\cs\CP317\CP317B-Project-Group7\instance
>>> from terms import list_terms
>>> [dict(term) for term in list_terms()]
[{'id': 1, 'code': 'DEMO2026', 'name': 'Updated Demo Term', 'start_date': '2026-09-01', 'end_date': '2026-12-30'}]
>>>


----------------------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------------------
TEST: (Course creation and db persistance):
----------------------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------------------

Microsoft Windows [Version 10.0.26200.9711]
(c) Microsoft Corporation. All rights reserved.

C:\Users\alinm\OneDrive\Documents\school\cs\CP317\CP317B-Project-Group7>.\.venv\Scripts\python.exe -m flask --app app init-db
Database initialized: C:\Users\alinm\OneDrive\Documents\school\cs\CP317\CP317B-Project-Group7\instance\registro.sqlite

C:\Users\alinm\OneDrive\Documents\school\cs\CP317\CP317B-Project-Group7>set PYTHON_BASIC_REPL=1

C:\Users\alinm\OneDrive\Documents\school\cs\CP317\CP317B-Project-Group7>.\.venv\Scripts\python.exe -m flask --app app shell
Python 3.14.5 (tags/v3.14.5:5607950, May 10 2026, 10:43:50) [MSC v.1944 64 bit (AMD64)] on win32
App: app
Instance: C:\Users\alinm\OneDrive\Documents\school\cs\CP317\CP317B-Project-Group7\instance
>>> from courses import create_course, get_course, list_courses, update_course
>>> course_id = create_course("DEMO101", "Demo Programming", "Fictional course for prototype testing.")
>>> dict(get_course(course_id))
{'id': 1, 'code': 'DEMO101', 'title': 'Demo Programming', 'description': 'Fictional course for prototype testing.'}
>>> update_course(course_id, "DEMO101", "Updated Demo Programming", "Updated fictional course description.")
>>> [dict(course) for course in list_courses()]
[{'id': 1, 'code': 'DEMO101', 'title': 'Updated Demo Programming', 'description': 'Updated fictional course description.'}]
>>> exit()
now exiting InteractiveConsole...

C:\Users\alinm\OneDrive\Documents\school\cs\CP317\CP317B-Project-Group7>set PYTHON_BASIC_REPL=1

C:\Users\alinm\OneDrive\Documents\school\cs\CP317\CP317B-Project-Group7>.\.venv\Scripts\python.exe -m flask --app app shell
Python 3.14.5 (tags/v3.14.5:5607950, May 10 2026, 10:43:50) [MSC v.1944 64 bit (AMD64)] on win32
App: app
Instance: C:\Users\alinm\OneDrive\Documents\school\cs\CP317\CP317B-Project-Group7\instance
>>> from courses import list_courses
>>> [dict(course) for course in list_courses()]
[{'id': 1, 'code': 'DEMO101', 'title': 'Updated Demo Programming', 'description': 'Updated fictional course description.'}]
>>>
----------------------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------------------
TEST: (validated section creation and db persistance):
----------------------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------------------

Microsoft Windows [Version 10.0.26200.9711]
(c) Microsoft Corporation. All rights reserved.

C:\Users\alinm\OneDrive\Documents\school\cs\CP317\CP317B-Project-Group7>.\.venv\Scripts\python.exe -m flask --app app init-db
Database initialized: C:\Users\alinm\OneDrive\Documents\school\cs\CP317\CP317B-Project-Group7\instance\registro.sqlite

C:\Users\alinm\OneDrive\Documents\school\cs\CP317\CP317B-Project-Group7>set PYTHON_BASIC_REPL=1

C:\Users\alinm\OneDrive\Documents\school\cs\CP317\CP317B-Project-Group7>.\.venv\Scripts\python.exe -m flask --app app shell
Python 3.14.5 (tags/v3.14.5:5607950, May 10 2026, 10:43:50) [MSC v.1944 64 bit (AMD64)] on win32
App: app
Instance: C:\Users\alinm\OneDrive\Documents\school\cs\CP317\CP317B-Project-Group7\instance
>>> from sections import create_section, get_section, list_sections, update_section
>>> section_id = create_section(1, 1, "01", ["Mon", "Wed", "Fri"], "09:00", "09:50", "Demo Room 101", 30)
>>> dict(get_section(section_id))
{'id': 1, 'course_id': 1, 'term_id': 1, 'code': '01', 'meeting_days': 'Mon, Wed, Fri', 'start_time': '09:00', 'end_time': '09:50', 'location': 'Demo Room 101', 'capacity': 30, 'course_code': 'DEMO101', 'course_title': 'Updated Demo Programming', 'term_code': 'DEMO2026', 'term_name': 'Updated Demo Term'}
>>> update_section(section_id, 1, 1, "01", ["Tue", "Thu"], "10:00", "11:20", "Demo Room 202", 25)
>>> [dict(section) for section in list_sections(term_id=1)]
[{'id': 1, 'course_id': 1, 'term_id': 1, 'code': '01', 'meeting_days': 'Tue, Thu', 'start_time': '10:00', 'end_time': '11:20', 'location': 'Demo Room 202', 'capacity': 25, 'course_code': 'DEMO101', 'course_title': 'Updated Demo Programming', 'term_code': 'DEMO2026', 'term_name': 'Updated Demo Term'}]
>>> exit()
now exiting InteractiveConsole...

C:\Users\alinm\OneDrive\Documents\school\cs\CP317\CP317B-Project-Group7>set PYTHON_BASIC_REPL=1

C:\Users\alinm\OneDrive\Documents\school\cs\CP317\CP317B-Project-Group7>.\.venv\Scripts\python.exe -m flask --app app shell
Python 3.14.5 (tags/v3.14.5:5607950, May 10 2026, 10:43:50) [MSC v.1944 64 bit (AMD64)] on win32
App: app
Instance: C:\Users\alinm\OneDrive\Documents\school\cs\CP317\CP317B-Project-Group7\instance
>>> from sections import list_sections
>>> [dict(section) for section in list_sections(term_id=1)]
[{'id': 1, 'course_id': 1, 'term_id': 1, 'code': '01', 'meeting_days': 'Tue, Thu', 'start_time': '10:00', 'end_time': '11:20', 'location': 'Demo Room 202', 'capacity': 25, 'course_code': 'DEMO101', 'course_title': 'Updated Demo Programming', 'term_code': 'DEMO2026', 'term_name': 'Updated Demo Term'}]
>>>
----------------------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------------------
TEST: (validated student account creation and db persistance):
----------------------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------------------


Microsoft Windows [Version 10.0.26200.9711]
(c) Microsoft Corporation. All rights reserved.

C:\Users\alinm\OneDrive\Documents\school\cs\CP317\CP317B-Project-Group7>set PYTHON_BASIC_REPL=1

C:\Users\alinm\OneDrive\Documents\school\cs\CP317\CP317B-Project-Group7>.\.venv\Scripts\python.exe -m flask --app app shell
Python 3.14.5 (tags/v3.14.5:5607950, May 10 2026, 10:43:50) [MSC v.1944 64 bit (AMD64)] on win32
App: app
Instance: C:\Users\alinm\OneDrive\Documents\school\cs\CP317\CP317B-Project-Group7\instance
>>> from students import create_student, get_student, list_students
>>> from db import get_db
>>> from werkzeug.security import check_password_hash
>>> student_id = create_student("student3", "StudentDemo123!", "TEST1003", "Jordan Lee")
>>> dict(get_student(student_id))
{'id': 3, 'user_id': 4, 'student_number': 'TEST1003', 'full_name': 'Jordan Lee', 'username': 'student3'}
>>> account = get_db().execute("SELECT role, password_hash FROM users WHERE username = ?", ("student3",)).fetchone()
>>> account["role"]
'student'
>>> check_password_hash(account["password_hash"], "StudentDemo123!")
True
>>> account["password_hash"] == "StudentDemo123!"
False
>>> create_student("student3", "StudentDemo123!", "TEST1004", "Duplicate Username")
Traceback (most recent call last):
  File "C:\Users\alinm\OneDrive\Documents\school\cs\CP317\CP317B-Project-Group7\students.py", line 46, in create_student
    user_cursor = database.execute(
        "INSERT INTO users (username, password_hash, role) "
        "VALUES (?, ?, 'student')",
        (username, password_hash),
    )
sqlite3.IntegrityError: UNIQUE constraint failed: users.username

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "<console>", line 1, in <module>
  File "C:\Users\alinm\OneDrive\Documents\school\cs\CP317\CP317B-Project-Group7\students.py", line 60, in create_student
    raise ValueError(
    ...<2 lines>...
    ) from problem
ValueError: Student could not be created. The username or student number may already be in use.
>>> create_student("rollbacktest", "StudentDemo123!", "TEST1003", "Duplicate Number")
Traceback (most recent call last):
  File "C:\Users\alinm\OneDrive\Documents\school\cs\CP317\CP317B-Project-Group7\students.py", line 52, in create_student
    student_cursor = database.execute(
        "INSERT INTO students "
    ...<2 lines>...
        (user_cursor.lastrowid, student_number, full_name),
    )
sqlite3.IntegrityError: UNIQUE constraint failed: students.student_number

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "<console>", line 1, in <module>
  File "C:\Users\alinm\OneDrive\Documents\school\cs\CP317\CP317B-Project-Group7\students.py", line 60, in create_student
    raise ValueError(
    ...<2 lines>...
    ) from problem
ValueError: Student could not be created. The username or student number may already be in use.
>>> get_db().execute("SELECT id FROM users WHERE username = ?", ("rollbacktest",)).fetchone() is None
True
>>> exit()
now exiting InteractiveConsole...

C:\Users\alinm\OneDrive\Documents\school\cs\CP317\CP317B-Project-Group7>
----------------------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------------------

TEST: (validated registration schema):
----------------------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------------------

Microsoft Windows [Version 10.0.26200.9711]
(c) Microsoft Corporation. All rights reserved.

C:\Users\alinm\source\CP317B-Project-Group7>.\.venv\Scripts\python.exe -m flask --app app shell
Python 3.14.5 (tags/v3.14.5:5607950, May 10 2026, 10:43:50) [MSC v.1944 64 bit (AMD64)] on win32
App: app
Instance: C:\Users\alinm\source\CP317B-Project-Group7\instance
>>> import enrollments as en
>>> from students import list_students, get_student_by_user_id
>>> from sections import list_sections
>>> student = list_students()[0]
>>> section = list_sections()[0]
>>> remaining = en.get_section_remaining_seats(section["id"])
>>> print(get_student_by_user_id(student["user_id"])["student_number"])
TEST1001
>>> print(remaining)
25
>>> print(en.is_course_enrolled(student["id"], section["course_id"], section["term_id"]))
False
>>> print(en.sections_conflict(section, section))
True
>>> print(en.get_section_selection_error(section, [], [section], remaining))
DEMO101 is already in your selected courses.
>>>

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL COLLATE NOCASE UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('student', 'admin'))
);

CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL UNIQUE,
    student_number TEXT NOT NULL UNIQUE,
    full_name TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS terms (
    id INTEGER PRIMARY KEY,
    code TEXT NOT NULL COLLATE NOCASE UNIQUE,
    name TEXT NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    CHECK (end_date >= start_date)
);

CREATE TABLE IF NOT EXISTS courses (
    id INTEGER PRIMARY KEY,
    code TEXT NOT NULL COLLATE NOCASE UNIQUE,
    title TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS sections (
    id INTEGER PRIMARY KEY,
    course_id INTEGER NOT NULL,
    term_id INTEGER NOT NULL,
    code TEXT NOT NULL COLLATE NOCASE,
    meeting_days TEXT NOT NULL,
    start_time TEXT NOT NULL,
    end_time TEXT NOT NULL,
    location TEXT NOT NULL,
    capacity INTEGER NOT NULL DEFAULT 0
        CHECK (typeof(capacity) = 'integer' AND capacity >= 0),
    UNIQUE (course_id, term_id, code),
    FOREIGN KEY (course_id) REFERENCES courses(id),
    FOREIGN KEY (term_id) REFERENCES terms(id),
    CHECK (end_time > start_time)
);
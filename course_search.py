"""UI-1: student course search and browsing; independent of registration.

REG-1 may use the returned section ID to implement registration separately.
This module deliberately does not claim current seat counts; UI-3 owns those.
"""
from db import get_db


def _term_id(value):
    if value in (None, ""):
        return None
    text = str(value).strip()
    if not text.isdecimal() or not 1 <= int(text) <= 9223372036854775807:
        raise ValueError("Choose a valid academic term.")
    return int(text)


def _literal_like(text):
    """Escape SQLite LIKE wildcards so input is a literal substring search."""
    return text.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")


def search_sections(term_id=None, query=""):
    """Return course sections, filtered by academic term and course code/title.

    An empty term shows all terms; selecting a term narrows the result. An empty
    search shows all sections in that term. Both filters use SQL parameters.
    """
    term = _term_id(term_id)
    query = (query or "").strip()
    if len(query) > 100:
        raise ValueError("Search text must be 100 characters or fewer.")

    sql = """
        SELECT s.id AS section_id, s.code AS section_code,
               c.id AS course_id, c.code AS course_code,
               c.title AS course_title, c.description,
               t.id AS term_id, t.code AS term_code, t.name AS term_name,
               s.meeting_days, s.start_time, s.end_time,
               s.location, s.capacity
          FROM sections AS s
          JOIN courses AS c ON c.id = s.course_id
          JOIN terms AS t ON t.id = s.term_id
         WHERE 1 = 1
    """
    arguments = []
    if term is not None:
        sql += " AND s.term_id = ?"
        arguments.append(term)
    if query:
        pattern = "%" + _literal_like(query) + "%"
        sql += " AND (c.code LIKE ? ESCAPE '\\' OR c.title LIKE ? ESCAPE '\\')"
        arguments.extend((pattern, pattern))
    sql += " ORDER BY t.start_date DESC, c.code, s.code"
    return get_db().execute(sql, arguments).fetchall()

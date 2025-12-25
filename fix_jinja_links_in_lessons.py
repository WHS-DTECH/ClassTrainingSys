# Script: fix_jinja_links_in_lessons.py
# Description: Replace raw Jinja links in lesson content with actual URLs for affected lessons.

from app import create_app, db
from app.models import Lesson
import re

def fix_jinja_links():
    app = create_app()
    with app.app_context():
        # Map lesson IDs to correct URLs or link formats
        url_map = {
            5: [
                (r"\{\{ url_for\('courses.view_lesson', lesson_id=34\) \}\}", "/courses/lessons/5"),
                (r"\{\{ url_for\('courses.view_lesson', lesson_id=35\) \}\}", "/courses/lessons/6"),
                (r"\{\{ url_for\('courses.view_lesson', lesson_id=36\) \}\}", "/courses/lessons/7"),
                (r"\{\{ url_for\('courses.view_lesson', lesson_id=37\) \}\}", "/courses/lessons/8"),
            ],
            8: [
                (r"\{\{ url_for\('courses.view_lesson', lesson_id=lesson.id, section=1\) \}\}", "/courses/sections/16"),
                (r"\{\{ url_for\('courses.view_lesson', lesson_id=lesson.id, section=2\) \}\}", "/courses/sections/17"),
            ],
        }
        lessons = Lesson.query.filter(Lesson.id.in_([5, 6, 7, 8])).all()
        for lesson in lessons:
            original = lesson.content
            if lesson.id in url_map:
                for pattern, url in url_map[lesson.id]:
                    original = re.sub(pattern, url, original)
            # Remove any remaining raw Jinja url_for links
            original = re.sub(r"\{\{\s*url_for\([^)]+\)\s*\}\}", "#broken-link#", original)
            lesson.content = original
            print(f"Fixed links in lesson ID: {lesson.id} | Title: {lesson.title}")
        db.session.commit()
        print("All affected lesson links have been fixed.")

if __name__ == "__main__":
    fix_jinja_links()

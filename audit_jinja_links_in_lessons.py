# Script: audit_jinja_links_in_lessons.py
# Description: Find lessons with raw Jinja code in their content field (e.g., {{ url_for(...) }})

from app import create_app
from app.models import Lesson
import re

def audit_jinja_links():
    app = create_app()
    with app.app_context():
        pattern = re.compile(r"\{\{\s*url_for\(")
        lessons = Lesson.query.all()
        found = False
        for lesson in lessons:
            if lesson.content and pattern.search(lesson.content):
                print(f"Lesson ID: {lesson.id} | Title: {lesson.title}\nRaw Jinja link found in content:\n{lesson.content}\n{'-'*60}")
                found = True
        if not found:
            print("No lessons with raw Jinja links found.")

if __name__ == "__main__":
    audit_jinja_links()

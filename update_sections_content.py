
# Script to update all key fields for Section records 5–17
import os
from app import db, create_app
from app.models import Section

# Define the correct data for each section (id, lesson_id, title, html_path)
SECTION_DATA = [
    # Lesson 1: Commenting
    dict(id=5, lesson_id=3, title="1. Introduction to Code Comments", html_path="app/templates/lessons/lesson1/l1section_intro.html"),
    dict(id=6, lesson_id=3, title="2. Section 1: Python Comments - Best Practices", html_path="app/templates/lessons/lesson1/l1section1.html"),
    dict(id=7, lesson_id=3, title="3. Section 2: JavaScript Comments - Best Practices", html_path="app/templates/lessons/lesson1/l1section2.html"),
    dict(id=8, lesson_id=3, title="4. Section 3: HTML and CSS Comments - Best Practices", html_path="app/templates/lessons/lesson1/l1section3.html"),
    # Lesson 2: Debugging
    dict(id=9, lesson_id=4, title="1. Introduction to Code Debugging", html_path="app/templates/lessons/lesson2/l2section_intro.html"),
    dict(id=10, lesson_id=4, title="2. Section 1: Python Debugging - Best Practices", html_path="app/templates/lessons/lesson2/l2section1.html"),
    dict(id=11, lesson_id=4, title="3. Section 2: JavaScript Debugging - Best Practices", html_path="app/templates/lessons/lesson2/l2section2.html"),
    dict(id=12, lesson_id=4, title="4. Section 3: HTML and CSS Debugging - Best Practices", html_path="app/templates/lessons/lesson2/l2section3.html"),
    # Lesson 3: Assessment Checking
    dict(id=13, lesson_id=7, title="0. Checking Overview", html_path="app/templates/lessons/lesson3/l3section_intro.html"),
    dict(id=14, lesson_id=7, title="1. Lesson 1: Comment Checker", html_path="app/templates/lessons/lesson3/l3section1.html"),
    dict(id=15, lesson_id=7, title="2. Lesson 2: Debug Checker", html_path="app/templates/lessons/lesson3/l3section2.html"),
    # Lesson 4: AI
    dict(id=16, lesson_id=8, title="1. Coding with AI", html_path="app/templates/lessons/lesson4/l4section1.html"),
    dict(id=17, lesson_id=8, title="2. Assessment Specific and AI", html_path="app/templates/lessons/lesson4/l4section2.html"),
]

def read_html(path):
    with open(path, encoding='utf-8') as f:
        return f.read()

def update_sections_all_fields():
    app = create_app(skip_socketio=True)
    with app.app_context():
        print("SQLAlchemy DB URI:", app.config['SQLALCHEMY_DATABASE_URI'])
        for sec in SECTION_DATA:
            section = Section.query.get(sec['id'])
            if not section:
                print(f"Section ID {sec['id']} not found, skipping.")
                continue
            # Update lesson_id and title
            section.lesson_id = sec['lesson_id']
            section.title = sec['title']
            # Update content
            if not os.path.exists(sec['html_path']):
                print(f"File not found: {sec['html_path']}")
                continue
            section.content = read_html(sec['html_path'])
            # Update template_path (relative to templates/)
            rel_path = sec['html_path'].replace('app/templates/', '')
            section.template_path = rel_path
            print(f"Updated Section_ID={sec['id']} (lesson_id={sec['lesson_id']}) with title, content, template_path={rel_path}")
        db.session.commit()
        print("Section records 5–17 updated: lesson_id, title, content, template_path.")

if __name__ == "__main__":
    update_sections_all_fields()

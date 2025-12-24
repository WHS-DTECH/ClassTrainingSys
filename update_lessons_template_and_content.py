# Script to update lesson template_path and content fields
import os
from app import db, create_app
from app.models import Lesson

# Map lesson_id to template path and content HTML file
LESSON_DATA = [
    # Lessons 1–8, update as needed for your actual lesson IDs and files
    dict(id=1, template_path="lessons/lesson1/l1_contents.html", html_path="app/templates/lessons/lesson1/l1_contents.html"),
    dict(id=2, template_path="lessons/lesson2/l2_contents.html", html_path="app/templates/lessons/lesson2/l2_contents.html"),
    dict(id=3, template_path="lessons/lesson3/l3_contents.html", html_path="app/templates/lessons/lesson3/l3_contents.html"),
    dict(id=4, template_path="lessons/lesson4/l4_contents.html", html_path="app/templates/lessons/lesson4/l4_contents.html"),
    dict(id=5, template_path="lessons/lesson1/l1_contents.html", html_path="app/templates/lessons/lesson1/l1_contents.html"),
    dict(id=6, template_path="lessons/lesson2/l2_contents.html", html_path="app/templates/lessons/lesson2/l2_contents.html"),
    dict(id=7, template_path="lessons/lesson3/l3_contents.html", html_path="app/templates/lessons/lesson3/l3_contents.html"),
    dict(id=8, template_path="lessons/lesson4/l4_contents.html", html_path="app/templates/lessons/lesson4/l4_contents.html"),
]

def read_html(path):
    with open(path, encoding='utf-8') as f:
        return f.read()

def update_lessons_template_and_content():
    app = create_app(skip_socketio=True)
    with app.app_context():
        print("SQLAlchemy DB URI:", app.config['SQLALCHEMY_DATABASE_URI'])
        for lesson_info in LESSON_DATA:
            lesson = Lesson.query.get(lesson_info['id'])
            if not lesson:
                print(f"Lesson ID {lesson_info['id']} not found, skipping.")
                continue
            # Update template_path
            lesson.template_path = lesson_info['template_path']
            # Update content
            if os.path.exists(lesson_info['html_path']):
                lesson.content = read_html(lesson_info['html_path'])
                print(f"Updated Lesson_ID={lesson_info['id']} with template_path={lesson_info['template_path']} and content from {lesson_info['html_path']}")
            else:
                print(f"File not found: {lesson_info['html_path']}")
        db.session.commit()
        print("Lesson records updated: template_path and content.")

if __name__ == "__main__":
    update_lessons_template_and_content()

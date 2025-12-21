# list_lessons.py
from app import create_app
from app.models import Lesson

def list_lessons():
    app = create_app()
    with app.app_context():
        lessons = Lesson.query.all()
        for lesson in lessons:
            print(f"ID: {lesson.id} | Title: {lesson.title}")

if __name__ == "__main__":
    list_lessons()

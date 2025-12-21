# print_lesson27_content.py
from app import create_app
from app.models import Lesson

def print_lesson27():
    app = create_app()
    with app.app_context():
        lesson = Lesson.query.get(27)
        if lesson:
            print('Lesson 27 content (first 2000 chars):\n')
            print(lesson.content[:2000])
        else:
            print('Lesson 27 not found.')

if __name__ == "__main__":
    print_lesson27()

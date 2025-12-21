# print_lesson28_content.py
from app import create_app
from app.models import Lesson

def print_lesson28():
    app = create_app()
    with app.app_context():
        lesson = Lesson.query.get(28)
        if lesson:
            content = lesson.content or ''
            print('Lesson 28 content (first 2000 chars):\n')
            print(content[:2000])
        else:
            print('Lesson 28 not found.')

if __name__ == "__main__":
    print_lesson28()

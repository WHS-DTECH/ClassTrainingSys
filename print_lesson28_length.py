from app import create_app
from app.models import Lesson

app = create_app()
with app.app_context():
    lesson = Lesson.query.get(28)
    if lesson and lesson.content:
        print('Lesson 28 content length:', len(lesson.content))
    else:
        print('Lesson 28 not found or empty.')

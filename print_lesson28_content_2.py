from app import create_app
from app.models import Lesson

app = create_app()
with app.app_context():
    lesson = Lesson.query.get(28)
    if lesson and lesson.content:
        print('Lesson 28 content (chars 2001-4000):\n')
        print(lesson.content[2000:4000])
    else:
        print('Lesson 28 not found or empty.')

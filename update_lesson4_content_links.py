# Script to update lesson content links for Lesson 4
# Replaces /courses/sections/16 with /lessons/sections/9 and /courses/sections/17 with /lessons/sections/10

from app import create_app, db
from app.models import Lesson

app = create_app()

with app.app_context():
    # Find the lesson (adjust the filter as needed for your DB)
    lesson = Lesson.query.filter_by(id=8).first()  # Change 8 to the correct lesson ID if needed
    if lesson and lesson.content:
        original = lesson.content
        updated = original.replace('/courses/sections/16', '/lessons/sections/16')
        updated = updated.replace('/courses/sections/17', '/lessons/sections/17')
        if updated != original:
            lesson.content = updated
            db.session.commit()
            print('Lesson content updated successfully.')
        else:
            print('No changes needed.')
    else:
        print('Lesson not found or has no content.')

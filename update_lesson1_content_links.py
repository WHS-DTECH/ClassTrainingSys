# Script to update lesson 1 content links for section IDs 5 to 8
# Replaces /courses/sections/5-8 with /lessons/sections/5-8 in lesson 1 content

from app import create_app, db
from app.models import Lesson

app = create_app()

with app.app_context():
    lesson = Lesson.query.filter_by(id=5).first()  # Updated to correct lesson ID
    if lesson and lesson.content:
        original = lesson.content
        updated = original
        for sid in range(5, 9):
            updated = updated.replace(f'/courses/sections/{sid}', f'/lessons/sections/{sid}')
        if updated != original:
            lesson.content = updated
            db.session.commit()
            print('Lesson 1 content updated successfully.')
        else:
            print('No changes needed.')
    else:
        print('Lesson 1 not found or has no content.')

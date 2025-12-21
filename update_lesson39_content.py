import os
import sys
from app import create_app, db
from app.models import Lesson

# Set up Flask app context
app = create_app()

NEW_CONTENT = """
<h2>Universal Commenting Best Practices</h2>
<p>These principles apply to both Python and JavaScript (and most programming languages):</p>
<!-- The rest of your summary/intro here, or leave blank if you want only the flexbox block to show -->
<!-- Place marker for summary conventions block below -->
SUMMARY_CONVENTIONS
"""

def update_lesson_content(lesson_id, new_content):
    with app.app_context():
        lesson = Lesson.query.get(lesson_id)
        if not lesson:
            print(f"Lesson with id {lesson_id} not found.")
            return
        lesson.content = new_content
        db.session.commit()
        print(f"Lesson {lesson_id} content updated.")

if __name__ == "__main__":
    LESSON_ID = 39  # Update this if your lesson id is different
    update_lesson_content(LESSON_ID, NEW_CONTENT)

import os
from app import create_app, db
from app.models import Lesson, Course

# Set up Flask app context
app = create_app()

MODULE3_TITLE = "Module 3: Checking for Assessment Purposes"
MODULE3_CONTENT = '{% include "includes/module3_checking_assessment.html" %}'
MODULE3_DESCRIPTION = "Learn best practices and tips for checking student work for assessment purposes."
MODULE3_ORDER = 3  # Adjust as needed
COURSE_ID = 1  # Change this to the correct course ID for your curriculum


def add_module3_lesson():
    with app.app_context():
        # Check if lesson already exists
        existing = Lesson.query.filter_by(title=MODULE3_TITLE).first()
        if existing:
            print(f"Lesson '{MODULE3_TITLE}' already exists (id={existing.id}).")
            return
        # Optionally, check if course exists
        course = Course.query.get(COURSE_ID)
        if not course:
            print(f"Course with id {COURSE_ID} not found.")
            return
        lesson = Lesson(
            title=MODULE3_TITLE,
            content=MODULE3_CONTENT,
            description=MODULE3_DESCRIPTION,
            order=MODULE3_ORDER,
            course_id=COURSE_ID
        )
        db.session.add(lesson)
        db.session.commit()
        print(f"Lesson '{MODULE3_TITLE}' added to course '{course.title}' (id={lesson.id}).")

if __name__ == "__main__":
    add_module3_lesson()

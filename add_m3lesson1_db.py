from app import create_app, db
from app.models import Lesson, Course

app = create_app()
with app.app_context():
    course = Course.query.filter_by(title="Module 3: Checking for Assessment Purposes").first()
    if not course:
        print("Module 3 course not found.")
    else:
        lesson = Lesson(
            title="Lesson 1: Comment Checker",
            content="",
            order=1,
            course_id=course.id,
            template_path="modules/module3/m3lesson1.html"
        )
        db.session.add(lesson)
        db.session.commit()
        print(f"Lesson created with id: {lesson.id}")

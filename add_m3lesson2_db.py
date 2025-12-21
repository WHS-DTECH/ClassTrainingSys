from app import create_app, db
from app.models import Lesson, Course

app = create_app()
with app.app_context():
    course = Course.query.filter_by(title="Module 3: Checking for Assessment Purposes").first()
    if not course:
        print("Module 3 course not found.")
    else:
        lesson = Lesson(
            title="Lesson 2: Debug Checker",
            content="",
            order=2,
            course_id=course.id,
            template_path="modules/module3/m3lesson2.html"
        )
        db.session.add(lesson)
        db.session.commit()
        print(f"Lesson created with id: {lesson.id}")

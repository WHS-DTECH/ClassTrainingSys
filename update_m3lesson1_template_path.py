from app import create_app, db
from app.models import Course, Lesson

MODULE3_COURSE_TITLE = "Module 3: Checking for Assessment Purposes"
MODULE3_LESSON_TITLE = "Assessment Checking Overview"
NEW_TEMPLATE_PATH = "modules/module3/m3lesson1.html"

app = create_app()
with app.app_context():
    course = Course.query.filter_by(title=MODULE3_COURSE_TITLE).first()
    if not course:
        print(f"Course '{MODULE3_COURSE_TITLE}' not found.")
    else:
        lesson = Lesson.query.filter_by(title=MODULE3_LESSON_TITLE, course_id=course.id).first()
        if not lesson:
            print(f"Lesson '{MODULE3_LESSON_TITLE}' not found in course '{MODULE3_COURSE_TITLE}'.")
        else:
            lesson.template_path = NEW_TEMPLATE_PATH
            db.session.commit()
            print(f"Updated template_path for lesson '{lesson.title}' to '{NEW_TEMPLATE_PATH}'.")
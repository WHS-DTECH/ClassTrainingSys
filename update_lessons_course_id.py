# Script to update course_id for specific lessons in the database
from app import db, create_app
from app.models import Lesson

def update_course_id():
    lesson_ids = [5, 6, 7, 8]
    app = create_app()
    with app.app_context():
        lessons = Lesson.query.filter(Lesson.id.in_(lesson_ids)).all()
        for lesson in lessons:
            lesson.course_id = 4
            print(f"Updated Lesson_ID={lesson.id} to course_id=4")
        db.session.commit()
        print("Update complete.")

if __name__ == "__main__":
    update_course_id()

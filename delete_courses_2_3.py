from app import create_app, db
from app.models import Course

def delete_courses():
    app = create_app()
    with app.app_context():
        for course_id in [2, 3]:
            course = Course.query.get(course_id)
            if course:
                db.session.delete(course)
                print(f"Deleted Course ID {course_id}: {course.title}")
            else:
                print(f"Course ID {course_id} not found.")
        db.session.commit()
        print("Done.")

if __name__ == "__main__":
    delete_courses()

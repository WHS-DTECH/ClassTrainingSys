
from app import db, create_app
from app.models import Course

# Change these values as needed
course_name = "Sample Course"
course_description = "This is a sample course created via script."

app = create_app()
with app.app_context():
    existing = Course.query.filter_by(title=course_name).first()
    if existing:
        print(f"Course '{course_name}' already exists (id={existing.id}).")
    else:
        new_course = Course(title=course_name, description=course_description)
        db.session.add(new_course)
        db.session.commit()
        print(f"Course '{course_name}' created with id={new_course.id}.")

from app import db, create_app
from app.models import Course

app = create_app()
with app.app_context():
    title = "Programming Documentation"
    description = "Course for programming documentation best practices."
    course = Course.query.filter_by(title=title).first()
    if not course:
        course = Course(title=title, description=description)
        db.session.add(course)
        db.session.commit()
        print(f"Course '{title}' created.")
    else:
        print(f"Course '{title}' already exists.")

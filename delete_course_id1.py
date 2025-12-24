from app import db, create_app
from app.models import Course

app = create_app()
with app.app_context():
    course = Course.query.get(1)
    if course:
        db.session.delete(course)
        db.session.commit()
        print("Course with id 1 deleted.")
    else:
        print("Course with id 1 not found.")

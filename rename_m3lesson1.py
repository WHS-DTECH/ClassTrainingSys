# Script to rename Lesson 1 in Module 3 to 'Lesson 1: Comment Checker'
from app import create_app, db
from app.models import Course, Lesson

app = create_app()

with app.app_context():
    course = Course.query.filter(Course.title.like('%Module 3%')).first()
    if not course:
        print('Module 3 course not found.')
    else:
        lesson = Lesson.query.filter_by(course_id=course.id, order=1).first()
        if lesson:
            lesson.title = 'Lesson 1: Comment Checker'
            db.session.commit()
            print('Lesson title updated successfully.')
        else:
            print('Lesson 1 not found in Module 3.')

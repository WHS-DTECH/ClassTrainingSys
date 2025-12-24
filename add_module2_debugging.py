"""
Add Module 2: Debugging to the database
This module teaches students what debugging is and why it is important.
"""

from app import create_app, db
from app.models import User, Course, Lesson

def add_debugging_module():
    app = create_app()
    with app.app_context():
        teacher = User.query.filter_by(username='teacher').first()
        if not teacher:
            print("Error: Teacher account not found. Please run init_db.py first.")
            return

        print("Creating Module 2: Debugging...")
        module2 = Course.query.filter_by(title='Module 2: Debugging', teacher_id=teacher.id).first()
        if not module2:
            module2 = Course(
                title='Module 2: Debugging',
                description='Learn what debugging is, why it is a critical skill for programmers, and how to approach finding and fixing errors in your code. This module covers the debugging mindset, common techniques, and the importance of persistence and problem-solving.',
                teacher_id=teacher.id
            )
            db.session.add(module2)
            db.session.commit()
        else:
            # Delete all existing sections for this module (robust)
            sections_to_delete = Lesson.query.filter_by(course_id=module2.id).all()
            for section in sections_to_delete:
                db.session.delete(section)
            db.session.commit()

        # Section 1: Introduction to Debugging (example)
        section1 = Lesson(
            course_id=module2.id,
            title='Introduction to Debugging',
            content='',
            order=1,
            template_path='modules/module2/m2lesson_intro.html'
        )
        db.session.add(section1)
        # ...repeat for additional sections as needed...
        db.session.commit()
        print(f"Module 2 created with id {module2.id}.")

if __name__ == '__main__':
    add_debugging_module()

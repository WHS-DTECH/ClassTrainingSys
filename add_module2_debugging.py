"""
Add Module 2: Debugging to the database
This module teaches students what debugging is and why it is important.
"""

from app import create_app, db
from app.models import User, Course

def add_debugging_module():
    app = create_app()
    with app.app_context():
        teacher = User.query.filter_by(username='teacher').first()
        if not teacher:
            print("Error: Teacher account not found. Please run init_db.py first.")
            return

        print("Creating Module 2: Debugging...")
        module2 = Course(
            title='Module 2: Debugging',
            description='Learn what debugging is, why it is a critical skill for programmers, and how to approach finding and fixing errors in your code. This module covers the debugging mindset, common techniques, and the importance of persistence and problem-solving.',
            teacher_id=teacher.id
        )
        db.session.add(module2)
        db.session.commit()
        print(f"Module 2 created with id {module2.id}.")

if __name__ == '__main__':
    add_debugging_module()

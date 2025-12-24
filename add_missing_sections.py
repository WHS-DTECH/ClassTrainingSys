# Script to add missing sections for Assessment Checking and AI modules
from app import db, create_app
from app.models import Section

def add_missing_sections():
    app = create_app()
    with app.app_context():
        new_sections = [
            # Module 3: Assessment Checking (lesson_id=7)
            {"lesson_id": 7, "title": "0. Checking Overview", "order": 1},
            {"lesson_id": 7, "title": "1. Lesson 1: Comment Checker", "order": 2},
            {"lesson_id": 7, "title": "2. Lesson 2: Debug Checker", "order": 3},
            # Module 4: Realtime Commenting and Debugging With AI (lesson_id=8)
            {"lesson_id": 8, "title": "1. Coding with AI", "order": 1},
            {"lesson_id": 8, "title": "2. Assessment Specific and AI", "order": 2}
        ]
        for section_data in new_sections:
            section = Section(**section_data)
            db.session.add(section)
            print(f"Added Section: lesson_id={section.lesson_id}, title='{section.title}', order={section.order}")
        db.session.commit()
        print("Missing sections for Assessment Checking and AI modules added.")

if __name__ == "__main__":
    add_missing_sections()

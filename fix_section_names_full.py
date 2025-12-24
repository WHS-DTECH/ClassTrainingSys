# Script to update Section names for all modules shown in screenshots
from app import db, create_app
from app.models import Section

def fix_section_names_full():
    app = create_app()
    with app.app_context():
        section_updates = [
            # Module 1: Commenting (lesson_id=3)
            (5, 3, "1. Introduction to Code Comments"),
            (6, 3, "2. Section 1: Python Comments - Best Practices"),
            (7, 3, "3. Section 2: JavaScript Comments - Best Practices"),
            (8, 3, "4. Section 3: HTML and CSS Comments - Best Practices"),
            # Module 2: Debugging (lesson_id=4)
            (9, 4, "1. Introduction to Code Debugging"),
            (10, 4, "2. Section 1: Python Debugging - Best Practices"),
            (11, 4, "3. Section 2: JavaScript Debugging - Best Practices"),
            (12, 4, "4. Section 3: HTML and CSS Debugging - Best Practices"),
            # Module 3: Assessment Checking (lesson_id=7)
            (13, 7, "0. Checking Overview"),
            (14, 7, "1. Lesson 1: Comment Checker"),
            (15, 7, "2. Lesson 2: Debug Checker"),
            # Module 4: Realtime Commenting and Debugging With AI (lesson_id=8)
            (16, 8, "1. Coding with AI"),
            (17, 8, "2. Assessment Specific and AI")
        ]
        for section_id, lesson_id, title in section_updates:
            section = Section.query.get(section_id)
            if section:
                section.lesson_id = lesson_id
                section.title = title
                print(f"Updated Section_ID={section_id}: lesson_id={lesson_id}, title='{title}'")
        db.session.commit()
        print("All section names and lesson links updated.")

if __name__ == "__main__":
    fix_section_names_full()

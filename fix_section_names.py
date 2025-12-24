# Script to update Section names to match those shown in the screenshots
from app import db, create_app
from app.models import Section

def fix_section_names():
    app = create_app()
    with app.app_context():
        # Lesson 5: Introduction of Code Comments
        section_updates = [
            # Lesson 5
            (5, "1. Introduction to Code Comments"),
            (6, "2. Section 1: Python Comments - Best Practices"),
            (7, "3. Section 2: JavaScript Comments - Best Practices"),
            (8, "4. Section 3: HTML and CSS Comments - Best Practices"),
            # Lesson 6
            (9, "1. Introduction to Code Debugging"),
            (10, "2. Section 1: Python Debugging - Best Practices"),
            (11, "3. Section 2: JavaScript Debugging - Best Practices"),
            (12, "4. Section 3: HTML and CSS Debugging - Best Practices"),
            # Lesson 7
            (13, "0. Checking Overview"),
            (14, "1. Lesson 1: Comment Checker"),
            (15, "2. Lesson 2: Debug Checker"),
            # Lesson 8
            (16, "1. Coding with AI"),
            (17, "2. Assessment Specific and AI")
        ]
        for section_id, title in section_updates:
            section = Section.query.get(section_id)
            if section:
                section.title = title
                print(f"Updated Section_ID={section_id}: title='{title}'")
        db.session.commit()
        print("Section names update complete.")

if __name__ == "__main__":
    fix_section_names()

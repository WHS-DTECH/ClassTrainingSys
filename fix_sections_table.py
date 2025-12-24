# Script to fix Section table: update titles and lesson_id links for rows 9-12
from app import db, create_app
from app.models import Section

def fix_sections():
    app = create_app()
    with app.app_context():
        # Section IDs 9-12 correspond to lessons 5-8
        updates = [
            (9, 5, "Module 1: Commenting"),
            (10, 6, "Module 2: Debugging"),
            (11, 7, "Module 3: Checking for Assessment"),
            (12, 8, "Lesson 4: Realtime Commenting & AI")
        ]
        for section_id, lesson_id, title in updates:
            section = Section.query.get(section_id)
            if section:
                section.lesson_id = lesson_id
                section.title = title
                print(f"Updated Section_ID={section_id}: lesson_id={lesson_id}, title='{title}'")
        db.session.commit()
        print("Section table update complete.")

if __name__ == "__main__":
    fix_sections()

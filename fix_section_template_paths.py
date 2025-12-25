# Script: fix_section_template_paths.py
# Description: Update template_path for AI sections to correct template locations.

from app import create_app, db
from app.models import Section

def fix_section_template_paths():
    app = create_app()
    with app.app_context():
        section_updates = [
            (16, 'lessons/lesson4/l4section1.html'),
            (17, 'lessons/lesson4/l4section2.html'),
        ]
        for section_id, template_path in section_updates:
            section = Section.query.get(section_id)
            if section:
                section.template_path = template_path
                print(f"Updated Section {section_id} template_path to {template_path}")
        db.session.commit()
        print("Section template paths updated.")

if __name__ == "__main__":
    fix_section_template_paths()

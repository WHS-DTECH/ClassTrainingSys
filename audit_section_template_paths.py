# Script: audit_section_template_paths.py
# Description: List all Section records and their template_path values for review.

from app import create_app
from app.models import Section

def audit_section_template_paths():
    app = create_app()
    with app.app_context():
        sections = Section.query.order_by(Section.id).all()
        print("Section ID | Lesson ID | Title | template_path")
        print("-"*70)
        for section in sections:
            print(f"{section.id:>3} | {section.lesson_id:>9} | {section.title} | {section.template_path}")
        print("Audit complete.")

if __name__ == "__main__":
    audit_section_template_paths()

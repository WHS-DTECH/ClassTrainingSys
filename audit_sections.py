# Script to audit Section table for all lessons
from app import create_app
from app.models import Section, Lesson

def audit_sections():
    app = create_app()
    with app.app_context():
        print("Section Table Audit:")
        sections = Section.query.order_by(Section.lesson_id, Section.order).all()
        for section in sections:
            lesson = Lesson.query.get(section.lesson_id)
            print(f"Section_ID={section.id} | Lesson_ID={section.lesson_id} | Lesson='{lesson.title if lesson else 'N/A'}' | Title='{section.title}' | Order={section.order} | Template='{section.template_path}' | Content length={len(section.content) if section.content else 0}")
        print(f"Total sections: {len(sections)}")

if __name__ == "__main__":
    audit_sections()

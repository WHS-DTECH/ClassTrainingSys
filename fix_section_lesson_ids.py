from app import create_app, db
from app.models import Section

def fix_section_lesson_ids():
    app = create_app()
    with app.app_context():
        updated_3 = Section.query.filter_by(lesson_id=3).update({Section.lesson_id: 5})
        updated_4 = Section.query.filter_by(lesson_id=4).update({Section.lesson_id: 6})
        db.session.commit()
        print(f"Updated {updated_3} sections from lesson_id=3 to lesson_id=5.")
        print(f"Updated {updated_4} sections from lesson_id=4 to lesson_id=6.")
        print("Done.")

if __name__ == "__main__":
    fix_section_lesson_ids()

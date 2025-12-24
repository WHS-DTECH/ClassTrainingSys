from app import create_app, db
from app.models import Section

def fix_section_orders():
    app = create_app()
    with app.app_context():
        # For lesson_id 5 (should be 1,2,3,4)
        ids_5 = [5,6,7,8]
        for idx, sid in enumerate(ids_5, 1):
            section = Section.query.get(sid)
            if section:
                section.order = idx
        # For lesson_id 6 (should be 1,2,3,4)
        ids_6 = [9,10,11,12]
        for idx, sid in enumerate(ids_6, 1):
            section = Section.query.get(sid)
            if section:
                section.order = idx
        # For lesson_id 7 (should be 1,2,3)
        ids_7 = [13,14,15]
        for idx, sid in enumerate(ids_7, 1):
            section = Section.query.get(sid)
            if section:
                section.order = idx
        # For lesson_id 8 (should be 1,2)
        ids_8 = [16,17]
        for idx, sid in enumerate(ids_8, 1):
            section = Section.query.get(sid)
            if section:
                section.order = idx
        db.session.commit()
        print("Section orders updated.")

if __name__ == "__main__":
    fix_section_orders()

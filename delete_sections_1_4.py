from app import create_app, db
from app.models import Section

def delete_sections():
    app = create_app()
    with app.app_context():
        for section_id in [1, 2, 3, 4]:
            section = Section.query.get(section_id)
            if section:
                db.session.delete(section)
                print(f"Deleted Section ID {section_id}: {section.title}")
            else:
                print(f"Section ID {section_id} not found.")
        db.session.commit()
        print("Done.")

if __name__ == "__main__":
    delete_sections()

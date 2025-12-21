# Script to delete duplicate Section and Summary lessons for Module 1
from app import create_app, db
from app.models import Lesson

def delete_duplicates():
    app = create_app()
    with app.app_context():
        # Duplicate Section 3: HTML and CSS Comments - Best Practices (should only keep one for Module 1)
        section3_dupes = Lesson.query.filter_by(title='Section 3: HTML and CSS Comments - Best Practices', course_id=7).all()
        if len(section3_dupes) > 1:
            # Keep the first, delete the rest
            for lesson in section3_dupes[1:]:
                db.session.delete(lesson)
        # Duplicate Commenting Best Practices - Summary (should only keep one for Module 1)
        summary_dupes = Lesson.query.filter_by(title='Commenting Best Practices - Summary', course_id=7).all()
        if len(summary_dupes) > 1:
            for lesson in summary_dupes[1:]:
                db.session.delete(lesson)
        db.session.commit()
        print(f"Deleted {len(section3_dupes)-1} Section 3 duplicate(s) and {len(summary_dupes)-1} Summary duplicate(s) for Module 1.")

if __name__ == "__main__":
    delete_duplicates()

# Script to delete '99. Commenting Best Practices - Summary' lesson for Module 1
from app import create_app, db
from app.models import Lesson

def delete_summary():
    app = create_app()
    with app.app_context():
        summary = Lesson.query.filter_by(title='Commenting Best Practices - Summary', course_id=7).first()
        if summary:
            db.session.delete(summary)
            db.session.commit()
            print("Deleted '99. Commenting Best Practices - Summary' lesson for Module 1.")
        else:
            print("No '99. Commenting Best Practices - Summary' lesson found for Module 1.")

if __name__ == "__main__":
    delete_summary()

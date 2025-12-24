from app import create_app, db
from app.models import Lesson

def delete_lessons():
    app = create_app()
    with app.app_context():
        for lesson_id in [1, 2, 3, 4]:
            lesson = Lesson.query.get(lesson_id)
            if lesson:
                db.session.delete(lesson)
                print(f"Deleted Lesson ID {lesson_id}: {lesson.title}")
            else:
                print(f"Lesson ID {lesson_id} not found.")
        db.session.commit()
        print("Done.")

if __name__ == "__main__":
    delete_lessons()

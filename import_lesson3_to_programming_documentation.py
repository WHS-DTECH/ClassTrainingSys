import json
from app import db, create_app
from app.models import Course, Lesson, Section

json_path = "bulk_upload_json/lesson3.json"
course_title = "Programming Documentation"

app = create_app()
with app.app_context():
    course = Course.query.filter_by(title=course_title).first()
    if not course:
        print(f"Course '{course_title}' not found.")
        exit(1)
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        lesson = Lesson(
            course_id=course.id,
            title=data["title"],
            description=data.get("description", ""),
            order=3
        )
        db.session.add(lesson)
        db.session.commit()
        print(f"Lesson '{lesson.title}' added to course '{course_title}' (id={lesson.id}).")
        # Add sections if present
        for idx, section in enumerate(data.get("sections", []), start=1):
            sec = Section(
                lesson_id=lesson.id,
                title=section["title"],
                content=section["content"],
                order=idx
            )
            db.session.add(sec)
        db.session.commit()
        print(f"Sections added to lesson '{lesson.title}'.")

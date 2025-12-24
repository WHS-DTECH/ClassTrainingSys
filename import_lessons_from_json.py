import json
from app import db, create_app
from app.models import Course, Lesson

# Path to your lesson JSON file
json_path = "bulk_upload_json/module1_commenting.json"  # Change as needed

app = create_app()
with app.app_context():
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        # Support both list of modules/courses and single lesson/course
        if isinstance(data, list):
            entries = data
        else:
            entries = [data]
        for entry in entries:
            c = entry.get("course")
            lessons = entry.get("lessons")
            if not c or not lessons:
                print("Error: JSON entry missing 'course' or 'lessons' keys.")
                continue
            course = Course.query.filter_by(title=c["title"]).first()
            if not course:
                course = Course(title=c["title"], description=c.get("description", ""))
                db.session.add(course)
                db.session.commit()
            for l in lessons:
                lesson = Lesson(
                    course_id=course.id,
                    title=l["title"],
                    content=l.get("content", ""),
                    order=int(l.get("order", 0)),
                    template_path=l.get("template_path", ""),
                    video_url=l.get("video_url", "")
                )
                db.session.add(lesson)
        db.session.commit()
        print("Import complete.")

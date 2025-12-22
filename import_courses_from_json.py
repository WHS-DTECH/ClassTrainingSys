"""
import_courses_from_json.py
Bulk import or update a course and its lessons from a JSON file.
- If a course with the same title exists, update its description and lessons.
- If a lesson with the same title/order exists in the course, update it; otherwise, add it.
- Usage: python import_courses_from_json.py module1.json
"""
import sys
import json
from app import create_app, db
from app.models import Course, Lesson, User

DEFAULT_TEACHER_EMAIL = 'vanessapringle@westlandhigh.school.nz'  # Changed to match admin user

def import_course_from_json(json_path):
    app = create_app()
    with app.app_context():
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)[0]
        course_data = data['course']
        lessons_data = data['lessons']

        # Find or create teacher
        teacher = User.query.filter_by(email=DEFAULT_TEACHER_EMAIL).first()
        if not teacher:
            print(f"Teacher with email {DEFAULT_TEACHER_EMAIL} not found. Aborting.")
            return

        # Find or create course
        course = Course.query.filter_by(title=course_data['title']).first()
        if not course:
            course = Course(
                title=course_data['title'],
                description=course_data.get('description', ''),
                teacher_id=teacher.id
            )
            db.session.add(course)
            db.session.commit()
            print(f"Created new course: {course.title}")
        else:
            course.description = course_data.get('description', course.description)
            course.teacher_id = teacher.id
            db.session.commit()
            print(f"Updated existing course: {course.title}")

        # Import lessons
        for lesson_json in lessons_data:
            lesson = Lesson.query.filter_by(course_id=course.id, order=lesson_json['order']).first()
            if not lesson:
                lesson = Lesson(
                    course_id=course.id,
                    title=lesson_json['title'],
                    content=lesson_json.get('content', ''),
                    order=lesson_json['order'],
                    template_path=lesson_json.get('template_path', ''),
                    video_url=lesson_json.get('video_url', '')
                )
                db.session.add(lesson)
                print(f"  Added lesson: {lesson.title}")
            else:
                lesson.title = lesson_json['title']
                lesson.content = lesson_json.get('content', lesson.content)
                lesson.template_path = lesson_json.get('template_path', lesson.template_path)
                lesson.video_url = lesson_json.get('video_url', lesson.video_url)
                print(f"  Updated lesson: {lesson.title}")
        db.session.commit()
        print(f"Course '{course.title}' and lessons imported/updated successfully.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python import_courses_from_json.py <json_file>")
    else:
        import_course_from_json(sys.argv[1])

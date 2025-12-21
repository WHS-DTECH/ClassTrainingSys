import os
from app import create_app, db
from app.models import Course, Lesson

app = create_app()

MODULE3_COURSE_TITLE = "Module 3: Checking for Assessment Purposes"
MODULE3_COURSE_DESCRIPTION = "Learn best practices and tips for checking student work for assessment purposes."
MODULE3_LESSON_TITLE = "Assessment Checking Overview"
MODULE3_LESSON_CONTENT = '{% include "includes/module3_checking_assessment.html" %}'
MODULE3_LESSON_DESCRIPTION = "Overview and best practices for assessment checking."
MODULE3_COURSE_ORDER = 3  # Adjust as needed
MODULE3_LESSON_ORDER = 1


def add_module3_course():
    with app.app_context():
        # Check if course already exists
        existing_course = Course.query.filter_by(title=MODULE3_COURSE_TITLE).first()
        if existing_course:
            print(f"Course '{MODULE3_COURSE_TITLE}' already exists (id={existing_course.id}).")
            course = existing_course
        else:
            # Find the default teacher user
            from app.models import User
            teacher = User.query.filter_by(username='teacher').first()
            if not teacher:
                print("Error: Teacher account not found. Please run init_db.py first.")
                return
            course = Course(
                title=MODULE3_COURSE_TITLE,
                description=MODULE3_COURSE_DESCRIPTION,
                teacher_id=teacher.id
            )
            db.session.add(course)
            db.session.commit()
            print(f"Course '{MODULE3_COURSE_TITLE}' added (id={course.id}).")

        # Add Lesson 1 if it doesn't exist
        existing_lesson = Lesson.query.filter_by(title=MODULE3_LESSON_TITLE, course_id=course.id).first()
        if existing_lesson:
            print(f"Lesson '{MODULE3_LESSON_TITLE}' already exists in course '{course.title}' (id={existing_lesson.id}).")
        else:
            lesson = Lesson(
                title=MODULE3_LESSON_TITLE,
                content=MODULE3_LESSON_CONTENT,
                order=MODULE3_LESSON_ORDER,
                course_id=course.id,
                template_path="modules/module3/m3lesson1.html"
            )
            db.session.add(lesson)
            db.session.commit()
            print(f"Lesson '{MODULE3_LESSON_TITLE}' added to course '{course.title}' (id={lesson.id}).")

if __name__ == "__main__":
    add_module3_course()

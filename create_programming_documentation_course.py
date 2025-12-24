from app import create_app, db
from app.models import Course, Lesson, User

app = create_app()
with app.app_context():
    teacher = User.query.filter_by(username='vanessapringle').first()
    if not teacher:
        print("Teacher user not found.")
    else:
        course = Course(
            title="Programming Documentation",
            description="A course covering key programming documentation skills.",
            teacher_id=teacher.id
        )
        db.session.add(course)
        db.session.commit()

        lessons = [
            ("Commenting", "Learn about code comments.", 1, "modules/module1/m1lesson_intro.html"),
            ("Debugging", "Learn about debugging code.", 2, "modules/module2/m2lesson_intro.html"),
            ("Assessment Checking", "Learn about assessment checking.", 3, "modules/module3/m3lesson0.html"),
            ("Using AI", "Realtime Commenting and Debugging With AI", 4, "modules/module4/m4lesson_intro.html"),
        ]

        for title, content, order, template_path in lessons:
            section = Lesson(
                title=title,
                content=content,
                order=order,
                course_id=course.id,
                template_path=template_path
            )
            db.session.add(section)
        db.session.commit()
        print("Programming Documentation course and sections created.")

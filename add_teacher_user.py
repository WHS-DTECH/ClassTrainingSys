
from app import create_app, db
from app.models import User

app = create_app()
with app.app_context():
    # Add yourself as a teacher
    teacher_username = "vanessapringle"
    teacher_email = "vanessapringle@westlandhigh.school.nz"
    teacher_password = "YourSecurePassword"  # Change to a secure password

    teacher = User.query.filter_by(username=teacher_username).first()
    if teacher:
        print(f"Teacher user '{teacher_username}' already exists.")
    else:
        teacher = User(username=teacher_username, email=teacher_email, role="teacher")
        teacher.set_password(teacher_password)
        db.session.add(teacher)
        db.session.commit()
        print(f"Teacher user '{teacher_username}' created successfully.")

    # Add a student user for testing
    student_username = "student1"
    student_email = "student1@example.com"
    student_password = "StudentPassword"  # Change to a secure password

    student = User.query.filter_by(username=student_username).first()
    if student:
        print(f"Student user '{student_username}' already exists.")
    else:
        student = User(username=student_username, email=student_email, role="student")
        student.set_password(student_password)
        db.session.add(student)
        db.session.commit()
        print(f"Student user '{student_username}' created successfully.")

from app import create_app, db
from app.models import User

app = create_app()
with app.app_context():
    # Replace these values as needed
    username = "teacher"
    email = "teacher@example.com"
    password = "your_secure_password"

    # Check if user already exists
    user = User.query.filter_by(username=username).first()
    if user:
        print("Teacher user already exists.")
    else:
        teacher = User(username=username, email=email, is_teacher=True)
        teacher.set_password(password)  # Assumes User model has set_password method
        db.session.add(teacher)
        db.session.commit()
        print("Teacher user created successfully.")

from app import create_app
from app.models import User

app = create_app()
with app.app_context():
    teachers = User.query.filter_by(is_teacher=True).all()
    if not teachers:
        print("No teacher users found.")
    else:
        for t in teachers:
            print(f"Username: {t.username}, Email: {t.email}, ID: {t.id}, is_teacher: {t.is_teacher}")

from app import create_app
from app.models import User

app = create_app()
with app.app_context():
    users = User.query.all()
    for u in users:
        # Try both, depending on your model definition
        try:
            is_teacher = u.is_teacher()  # If it's a method
        except TypeError:
            is_teacher = u.is_teacher    # If it's a property/column
        print(f"Username: {u.username}, Email: {u.email}, is_teacher: {is_teacher}")

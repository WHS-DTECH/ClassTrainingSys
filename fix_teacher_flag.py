from app import create_app, db
from app.models import User

app = create_app()
with app.app_context():
    user = User.query.filter_by(username="teacher").first()
    if user:
        user.is_teacher = True
        db.session.commit()
        print("Teacher user updated to is_teacher=True.")
    else:
        print("Teacher user not found.")

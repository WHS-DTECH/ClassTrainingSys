from app import db, create_app
from app.models import User

# Update this to your email
user_email = "vanessapringle@westlandhigh.school.nz"

app = create_app()
with app.app_context():
    user = User.query.filter_by(email=user_email).first()
    if user:
        user.role = "teacher"  # or "admin" if you want admin access
        db.session.commit()
        print(f"Role updated for {user_email} to {user.role}")
    else:
        print(f"User with email {user_email} not found.")

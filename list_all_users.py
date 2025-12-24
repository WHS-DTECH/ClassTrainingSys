from app import create_app
from app.models import User

app = create_app()
with app.app_context():
    users = User.query.order_by(User.username).all()
    for user in users:
        print(f"Username: {user.username}, Email: {user.email}, Role: {user.role}")

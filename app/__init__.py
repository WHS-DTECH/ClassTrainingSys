from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user
from flask_migrate import Migrate
from flask_dance.contrib.google import make_google_blueprint, google
import os

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    from config import config
    config_name = os.environ.get('FLASK_CONFIG', 'default')
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    
    # Register blueprints
    from app.routes import auth, main, courses, assignments, quizzes, admin
    
    app.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(courses.bp)
    app.register_blueprint(assignments.bp)
    app.register_blueprint(quizzes.bp)
    app.register_blueprint(admin.bp)
    
    # Google OAuth blueprint
    google_bp = make_google_blueprint(
        client_id=os.environ.get("GOOGLE_OAUTH_CLIENT_ID"),
        client_secret=os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET"),
        scope=[
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/userinfo.profile",
            "openid"
        ]
    )
    app.register_blueprint(google_bp, url_prefix="/login")
    
    # Handle the authorized event from Flask-Dance
    from flask_dance.consumer import oauth_authorized
    
    @oauth_authorized.connect_via(google_bp)
    def google_logged_in(blueprint, token):
        try:
            from app.models import User
            
            # Get user info from Google
            resp = blueprint.session.get("/oauth2/v2/userinfo")
            if not resp.ok:
                return False
            
            user_info = resp.json()
            user_email = user_info.get("email")
            
            if not user_email:
                return False
            
            # Find or create user
            user = User.query.filter_by(email=user_email).first()
            if not user:
                username = user_email.split("@")[0]
                user = User(
                    username=username,
                    email=user_email,
                    role="student"
                )
                db.session.add(user)
                db.session.commit()
            
            login_user(user)
            return True
        except Exception as e:
            return False
    
    # Create database tables
    with app.app_context():
        db.create_all()
        # --- Permanent admin bootstrap ---
        from app.models import User
        admin_email = os.environ.get("ADMIN_EMAIL")
        admin_username = "vanessapringle"
        admin_password = os.environ.get("ADMIN_PASSWORD")
        if admin_password is None:
            admin_password = "defaultpassword"  # Or raise an error if you want to force setting it
        user = User.query.filter_by(email=admin_email).first()
        if not user:
            print("[ADMIN BOOTSTRAP] Creating admin user...")
            user = User(
                username=admin_username,
                email=admin_email,
                first_name="Vanessa",
                last_name="Pringle",
                role="teacher"
            )
            db.session.add(user)
        else:
            print("[ADMIN BOOTSTRAP] Admin user exists. Resetting password and role...")
        # Always set password and role for admin user
        user.set_password(str(admin_password))
        user.role = "teacher"
        db.session.commit()
        print(f"[ADMIN BOOTSTRAP] Admin user {admin_email} ensured with password (hidden) and role teacher.")
        # --- End permanent admin bootstrap ---
    
    # Ensure code_hash column exists in comment_feedback table
    with app.app_context():
        try:
            from sqlalchemy import text, inspect
            inspector = inspect(db.engine)
            if 'comment_feedback' in inspector.get_table_names():
                columns = [col['name'] for col in inspector.get_columns('comment_feedback')]
                if 'code_hash' not in columns:
                    print("[DB INIT] Adding code_hash column to comment_feedback table...")
                    with db.engine.begin() as conn:
                        conn.execute(text('ALTER TABLE comment_feedback ADD COLUMN code_hash VARCHAR(64) DEFAULT \'unknown\''))
                    print("[DB INIT] code_hash column added successfully")
        except Exception as e:
            print(f"[DB INIT] Warning: {e}")
    
    return app

# Expose app instance for Gunicorn (so 'gunicorn app:app' works)
app = create_app()

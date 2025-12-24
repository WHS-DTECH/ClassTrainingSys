from flask import Flask, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user
from flask_migrate import Migrate
from flask_dance.contrib.google import make_google_blueprint, google
import os

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app(skip_socketio=False):
    app = Flask(__name__)
    
    # Configuration
    from config import config
    config_name = os.environ.get('FLASK_CONFIG', 'default')
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    # Only initialize socketio if not skipped
    if not skip_socketio:
        from flask_socketio import SocketIO
        socketio = SocketIO(
            cors_allowed_origins="*",
            async_mode='eventlet',  # Use eventlet for production
            ping_timeout=60,
            ping_interval=25,
            engineio_logger=False
        )
        socketio.init_app(app)
    
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    
    # Register blueprints
    from app.routes import auth, main, courses, assignments, quizzes, notifications
    from app.routes.admin_routes import bp as admin_bp
    from app.routes.admin.db_export import admin_db_export
    app.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(courses.bp)
    app.register_blueprint(assignments.bp)
    app.register_blueprint(quizzes.bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(notifications.bp)
    app.register_blueprint(admin_db_export, url_prefix='/admin')
    
    # Google OAuth blueprint
    google_bp = make_google_blueprint(
        client_id=os.environ.get("GOOGLE_OAUTH_CLIENT_ID"),
        client_secret=os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET"),
        scope=[
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/userinfo.profile",
            "https://www.googleapis.com/auth/gmail.send",
            "openid"
        ]
    )
    app.register_blueprint(google_bp, url_prefix="/login")
    
    # Handle the authorized event from Flask-Dance
    from flask_dance.consumer import oauth_authorized
    
    @oauth_authorized.connect_via(google_bp)
    def google_logged_in(blueprint, token):
        import logging
        from flask import flash
        from app.models import User
        try:
            # Get user info from Google
            resp = blueprint.session.get("/oauth2/v2/userinfo")
            if not resp.ok:
                logging.error(f"Google OAuth userinfo fetch failed: {resp.text}")
                flash("Google login failed: could not fetch user info.", "danger")
                return False

            user_info = resp.json()
            user_email = user_info.get("email")

            if not user_email:
                logging.error("Google OAuth did not return an email address.")
                flash("Google login failed: no email address returned.", "danger")
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
            flash("Successfully logged in with Google!", "success")
            return True
        except Exception as e:
            logging.exception("Exception during Google OAuth login:")
            flash(f"Google login error: {str(e)}", "danger")
            return False
    
    # Admin bootstrap moved to CLI command
    # Flask CLI command to create or update the admin user
    from flask.cli import with_appcontext
    import click

    @click.command("create-admin")
    @with_appcontext
    def create_admin():
        from app.models import User
        admin_email = os.environ.get("ADMIN_EMAIL")
        admin_username = "vanessapringle"
        admin_password = os.environ.get("ADMIN_PASSWORD")
        if admin_password is None:
            admin_password = "defaultpassword"  # Or raise an error if you want to force setting it
        user = User.query.filter((User.email == admin_email) | (User.username == admin_username)).first()
        if not user:
            print("[ADMIN BOOTSTRAP] Creating admin user...")
            user = User(
                username=admin_username,
                email=admin_email,
                first_name="Vanessa",
                last_name="Pringle",
                role="teacher"
            )
            user.set_password(str(admin_password))
            db.session.add(user)
            db.session.commit()
            print(f"[ADMIN BOOTSTRAP] Admin user {admin_email} created.")
        else:
            print("[ADMIN BOOTSTRAP] Admin user exists. Resetting password and role...")
            user.set_password(str(admin_password))
            user.role = "teacher"
            db.session.commit()
            print(f"[ADMIN BOOTSTRAP] Admin user {admin_email} ensured with password (hidden) and role teacher.")

    def register_cli_commands(app):
        app.cli.add_command(create_admin)
    
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
    
    # Register error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500
    
    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template('errors/403.html'), 403
    
    # Context processor to provide admin email for contact form
    @app.context_processor
    def inject_admin_info():
        admin_email = os.environ.get("ADMIN_EMAIL", "teacher@example.com")
        return {'admin_email': admin_email}
    
    register_cli_commands(app)
    return app


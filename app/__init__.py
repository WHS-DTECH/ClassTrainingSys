from flask import Flask, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, current_user
from flask_migrate import Migrate
from flask_dance.contrib.google import make_google_blueprint
from sqlalchemy.exc import IntegrityError
import os
import re
import secrets

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app(skip_socketio=False):
    app = Flask(__name__, static_folder='../static', static_url_path='/static')
    
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
    from app.routes import auth, main, courses, assignments, quizzes, notifications, lessons
    from app.routes.admin_routes import bp as admin_bp
    from app.routes.admin.db_export import admin_db_export
    app.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(courses.bp)
    app.register_blueprint(assignments.bp)
    app.register_blueprint(quizzes.bp)
    app.register_blueprint(lessons.lessons_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(notifications.bp)
    app.register_blueprint(admin_db_export, url_prefix='/admin')
    
    # Google OAuth blueprints
    google_bp = make_google_blueprint(
        client_id=os.environ.get("GOOGLE_OAUTH_CLIENT_ID"),
        client_secret=os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET"),
        scope=[
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/userinfo.profile",
            "openid"
        ]
    )
    google_gmail_bp = None
    try:
        google_gmail_bp = make_google_blueprint(
            client_id=os.environ.get("GOOGLE_OAUTH_CLIENT_ID"),
            client_secret=os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET"),
            scope=[
                "https://www.googleapis.com/auth/userinfo.email",
                "https://www.googleapis.com/auth/userinfo.profile",
                "https://www.googleapis.com/auth/gmail.send",
                "openid"
            ],
            name="google_gmail"
        )
    except TypeError:
        # Older Flask-Dance versions do not support the `name` argument.
        pass
    app.register_blueprint(google_bp, url_prefix="/login")
    if google_gmail_bp is not None:
        app.register_blueprint(google_gmail_bp, url_prefix="/login-gmail")
    
    # Handle the authorized event from Flask-Dance
    from flask_dance.consumer import oauth_authorized

    def _allowed_google_domains():
        domains = app.config.get("GOOGLE_OAUTH_ALLOWED_DOMAINS", [])
        return {d.strip().lower() for d in domains if d and d.strip()}

    def _is_domain_allowed(email_value):
        allowed = _allowed_google_domains()
        if not allowed:
            return True
        domain = email_value.rsplit("@", 1)[-1].lower() if "@" in email_value else ""
        return domain in allowed

    def _build_unique_username(User, email_value):
        local_part = email_value.split("@", 1)[0]
        base = re.sub(r"[^a-z0-9_]+", "_", local_part.lower()).strip("_") or "student"
        base = base[:70]

        candidate = base
        suffix = 1
        while User.query.filter_by(username=candidate).first():
            suffix_text = f"_{suffix}"
            candidate = f"{base[:80 - len(suffix_text)]}{suffix_text}"
            suffix += 1
        return candidate

    def _handle_google_login(blueprint, allow_auto_create):
        import logging
        from flask import flash
        from app.models import User

        resp = blueprint.session.get("/oauth2/v2/userinfo")
        if not resp.ok:
            logging.error("Google OAuth userinfo fetch failed: %s", resp.text)
            flash("Google login failed: could not fetch profile.", "danger")
            return False

        user_info = resp.json()
        user_email = (user_info.get("email") or "").strip().lower()
        is_verified = bool(user_info.get("verified_email"))

        if not user_email:
            flash("Google login failed: no email address returned.", "danger")
            return False
        if not is_verified:
            flash("Google login failed: email is not verified.", "danger")
            return False
        if not _is_domain_allowed(user_email):
            flash("This Google account is not allowed for this site.", "danger")
            return False

        if current_user.is_authenticated and current_user.email.lower() != user_email:
            flash("Google account does not match your current session.", "danger")
            return False

        user = User.query.filter_by(email=user_email).first()
        if not user and not allow_auto_create:
            flash("Please sign in first before connecting Gmail access.", "warning")
            return False

        if not user:
            username = _build_unique_username(User, user_email)
            user = User(username=username, email=user_email, role="student")
            user.set_password(secrets.token_urlsafe(32))
            db.session.add(user)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                user = User.query.filter_by(email=user_email).first()
                if not user:
                    flash("Google login failed: account creation conflict.", "danger")
                    return False

        if not current_user.is_authenticated:
            login_user(user)

        return True
    
    @oauth_authorized.connect_via(google_bp)
    def google_logged_in(blueprint, token):
        try:
            from flask import flash
            if _handle_google_login(blueprint, allow_auto_create=True):
                flash("Successfully logged in with Google!", "success")
                return True
            return False
        except Exception:
            import logging
            from flask import flash
            logging.exception("Exception during Google OAuth login")
            flash("Google login error. Please try again.", "danger")
            return False

    if google_gmail_bp is not None:
        @oauth_authorized.connect_via(google_gmail_bp)
        def google_gmail_authorized(blueprint, token):
            try:
                from flask import flash
                if _handle_google_login(blueprint, allow_auto_create=False):
                    flash("Google Gmail access granted.", "success")
                    return True
                return False
            except Exception:
                import logging
                from flask import flash
                logging.exception("Exception during Gmail OAuth authorization")
                flash("Could not connect Gmail access.", "danger")
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


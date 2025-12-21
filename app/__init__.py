from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
import os

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///class_training.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
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
    
    # Create database tables
    with app.app_context():
        db.create_all()
        # --- TEMPORARY: Make user admin if email matches ---
        from app.models import User
        admin_email = "vanessapringle@westlandhigh.school.nz"
        user = User.query.filter_by(email=admin_email).first()
        if user and user.role != "teacher":
            user.role = "teacher"
            db.session.commit()
        # --- END TEMPORARY ---
    
    return app

# Expose app instance for Gunicorn (so 'gunicorn app:app' works)
app = create_app()

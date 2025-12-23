# ...existing code...

from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

# CommentCheck model must be defined after db is imported
class CommentCheck(db.Model):
    __tablename__ = 'comment_checks'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    checked_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<CommentCheck user_id={self.user_id} filename={self.filename}>'

# DebugCheck model for debug checker attempts
class DebugCheck(db.Model):
    __tablename__ = 'debug_checks'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    checked_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<DebugCheck user_id={self.user_id} filename={self.filename}>'
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    try:
        user_id_int = int(user_id)
        # SQLite INTEGER max value: 9223372036854775807
        if user_id_int < 1 or user_id_int > 9223372036854775807:
            return None
        return User.query.get(user_id_int)
    except (ValueError, OverflowError):
        return None

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='student')  # 'student' or 'teacher'
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    enrollments = db.relationship('Enrollment', backref='student', lazy=True, cascade='all, delete-orphan')
    submissions = db.relationship('Submission', backref='student', lazy=True, cascade='all, delete-orphan')
    quiz_attempts = db.relationship('QuizAttempt', backref='student', lazy=True, cascade='all, delete-orphan')
    courses_created = db.relationship('Course', backref='teacher', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_teacher(self):
        return self.role == 'teacher'
    
    def __repr__(self):
        return f'<User {self.username}>'

class Course(db.Model):
    __tablename__ = 'courses'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    order = db.Column(db.Integer, default=0)  # For custom ordering
    
    # Relationships
    lessons = db.relationship('Lesson', backref='course', lazy=True, cascade='all, delete-orphan', order_by='Lesson.order', foreign_keys='Lesson.course_id')
    enrollments = db.relationship('Enrollment', backref='course', lazy=True, cascade='all, delete-orphan')
    assignments = db.relationship('Assignment', backref='course', lazy=True, cascade='all, delete-orphan')
    quizzes = db.relationship('Quiz', backref='course', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Course {self.title}>'

class Lesson(db.Model):
    """3rd level (formerly 2nd): Content sections within lessons
    
    NOTE: This model is temporarily named 'Lesson' for backward compatibility.
    After Phase 2, this will be renamed to 'Section' in the code.
    Database table name is now 'sections' after Phase 1.2 migration.
    
    Structure after Phase 1.2:
    - courses.id -> lessons2.course_id
    - lessons2.id -> sections.lesson_id (will be added in Phase 1.3)
    - sections represent individual content sections/pages with exercises
    """
    __tablename__ = 'sections'  # Changed from 'lessons' in Phase 1.2
    
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text)
    order = db.Column(db.Integer, default=0)
    template_path = db.Column(db.String(255))  # Path to the section's HTML template
    video_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    progress = db.relationship('LessonProgress', backref='lesson', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Lesson {self.title}>'

class Lesson2(db.Model):
    """2nd level: Lessons within a Course (e.g., 'Commenting', 'Debugging')
    
    This is the new 2nd level in the 3-level hierarchy:
    Course (level 1) > Lesson2 (level 2) > Lesson (level 3, will be renamed to Section)
    
    This model will eventually replace the structure where lessons are direct children of courses.
    """
    __tablename__ = 'lessons2'
    
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships - will eventually link to Lesson (renamed to Section)
    # course = db.relationship('Course', backref='lessons2')
    
    def __repr__(self):
        return f'<Lesson2 {self.title}>'

# New model for robust feedback persistence
class CommentFeedback(db.Model):
    __tablename__ = 'comment_feedback'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    line_num = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=False)
    feedback = db.Column(db.Text, nullable=False)
    code_hash = db.Column(db.String(64), nullable=False)  # SHA256 hash of code
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Enrollment(db.Model):
    __tablename__ = 'enrollments'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    enrolled_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='active')  # 'active', 'completed', 'dropped'
    
    def __repr__(self):
        return f'<Enrollment Student:{self.student_id} Course:{self.course_id}>'

class LessonProgress(db.Model):
    __tablename__ = 'lesson_progress'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id'), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime)
    
    student = db.relationship('User', backref='lesson_progress')
    
    def __repr__(self):
        return f'<LessonProgress Student:{self.student_id} Lesson:{self.lesson_id}>'

class Assignment(db.Model):
    __tablename__ = 'assignments'
    
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    due_date = db.Column(db.DateTime)
    max_points = db.Column(db.Integer, default=100)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    submissions = db.relationship('Submission', backref='assignment', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Assignment {self.title}>'

class Submission(db.Model):
    __tablename__ = 'submissions'
    
    id = db.Column(db.Integer, primary_key=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignments.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text)
    file_path = db.Column(db.String(500))
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    graded = db.Column(db.Boolean, default=False)
    score = db.Column(db.Integer)
    feedback = db.Column(db.Text)
    graded_at = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<Submission Assignment:{self.assignment_id} Student:{self.student_id}>'

class Quiz(db.Model):
    __tablename__ = 'quizzes'
    
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    time_limit = db.Column(db.Integer)  # in minutes
    max_attempts = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    questions = db.relationship('QuizQuestion', backref='quiz', lazy=True, cascade='all, delete-orphan')
    attempts = db.relationship('QuizAttempt', backref='quiz', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Quiz {self.title}>'

class QuizQuestion(db.Model):
    __tablename__ = 'quiz_questions'
    
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(20), default='multiple_choice')  # 'multiple_choice', 'true_false', 'short_answer'
    options = db.Column(db.Text)  # JSON string for multiple choice options
    correct_answer = db.Column(db.Text)
    points = db.Column(db.Integer, default=1)
    order = db.Column(db.Integer, default=0)
    
    def __repr__(self):
        return f'<QuizQuestion {self.id}>'

class QuizAttempt(db.Model):
    __tablename__ = 'quiz_attempts'
    
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    score = db.Column(db.Float)
    answers = db.Column(db.Text)  # JSON string storing all answers
    
    def __repr__(self):
        return f'<QuizAttempt Quiz:{self.quiz_id} Student:{self.student_id}>'

class LessonFeedback(db.Model):
    __tablename__ = 'lesson_feedback'
    
    id = db.Column(db.Integer, primary_key=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    clarity = db.Column(db.Integer)  # 1-5: How clear was the lesson?
    difficulty = db.Column(db.Integer)  # 1-5: How difficult was the lesson?
    engagement = db.Column(db.Integer)  # 1-5: How engaging was the lesson?
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    lesson = db.relationship('Lesson', backref='feedback', lazy=True)
    student = db.relationship('User', backref='lesson_feedback', lazy=True)
    
    def __repr__(self):
        return f'<LessonFeedback Lesson:{self.lesson_id} Student:{self.student_id} Rating:{self.rating}>'


class AssignmentRubric(db.Model):
    __tablename__ = 'assignment_rubrics'
    
    id = db.Column(db.Integer, primary_key=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignments.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    total_points = db.Column(db.Integer, default=100)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    criteria = db.relationship('RubricCriterion', backref='rubric', lazy=True, cascade='all, delete-orphan')
    assignment = db.relationship('Assignment', backref='rubrics', lazy=True)
    
    def __repr__(self):
        return f'<AssignmentRubric {self.title} Assignment:{self.assignment_id}>'


class RubricCriterion(db.Model):
    __tablename__ = 'rubric_criteria'
    
    id = db.Column(db.Integer, primary_key=True)
    rubric_id = db.Column(db.Integer, db.ForeignKey('assignment_rubrics.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    points = db.Column(db.Integer, nullable=False)
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<RubricCriterion {self.name} {self.points}pts>'


class GradeDetail(db.Model):
    __tablename__ = 'grade_details'
    
    id = db.Column(db.Integer, primary_key=True)
    submission_id = db.Column(db.Integer, db.ForeignKey('submissions.id'), nullable=False)
    criterion_id = db.Column(db.Integer, db.ForeignKey('rubric_criteria.id'), nullable=False)
    points_awarded = db.Column(db.Integer, default=0)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    submission = db.relationship('Submission', backref='grade_details', lazy=True)
    criterion = db.relationship('RubricCriterion', lazy=True)
    
    def __repr__(self):
        return f'<GradeDetail Submission:{self.submission_id} Criterion:{self.criterion_id} Points:{self.points_awarded}>'


class Notification(db.Model):
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    notification_type = db.Column(db.String(50), nullable=False)  # 'assignment_submitted', 'assignment_graded', 'message', 'system'
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    related_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # Who initiated the notification
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignments.id'), nullable=True)
    submission_id = db.Column(db.Integer, db.ForeignKey('submissions.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', foreign_keys=[user_id], backref='notifications')
    related_user = db.relationship('User', foreign_keys=[related_user_id])
    assignment = db.relationship('Assignment', backref='notifications')
    submission = db.relationship('Submission', backref='notifications')
    
    def to_dict(self):
        """Convert notification to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'notification_type': self.notification_type,
            'title': self.title,
            'message': self.message,
            'is_read': self.is_read,
            'related_user': f"{self.related_user.first_name} {self.related_user.last_name}".strip() if self.related_user else None,
            'assignment_id': self.assignment_id,
            'submission_id': self.submission_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Notification user_id={self.user_id} type={self.notification_type} title={self.title}>'

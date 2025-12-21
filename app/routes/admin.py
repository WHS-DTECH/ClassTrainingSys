# TEMPORARY DEBUG ROUTE
@bp.route('/admin-debug')
def admin_debug():
    from app.models import User
    admin_email = "vanessapringle@westlandhigh.school.nz"
    user = User.query.filter_by(email=admin_email).first()
    if not user:
        return "Admin user not found."
    return f"Admin user: {user.email}<br>Username: {user.username}<br>Role: {user.role}<br>Password hash: {user.password_hash}"

# All imports at the top
import csv
import json
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import User, Course, Enrollment, Lesson
from functools import wraps

# Blueprint definition
bp = Blueprint('admin', __name__, url_prefix='/admin')

def teacher_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_teacher():
            flash('You must be a teacher to access this page.', 'danger')
            return redirect(url_for('main.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

# Bulk upload route
@bp.route('/bulk_upload', methods=['POST'])
@login_required
@teacher_required
def bulk_upload():
    upload_message = None
    file = request.files.get('bulkfile')
    if not file:
        upload_message = 'No file uploaded.'
        return redirect(url_for('admin.index', upload_message=upload_message))
    filename = secure_filename(file.filename)
    ext = filename.rsplit('.', 1)[-1].lower()
    try:
        if ext == 'csv':
            # Expecting: course_title, course_description, lesson_title, lesson_content, lesson_order, lesson_template_path, lesson_video_url
            reader = csv.DictReader(file.read().decode('utf-8').splitlines())
            for row in reader:
                # Find or create course
                course = Course.query.filter_by(title=row['course_title']).first()
                if not course:
                    course = Course(title=row['course_title'], description=row.get('course_description', ''), teacher_id=current_user.id)
                    db.session.add(course)
                    db.session.commit()
                # Add lesson
                lesson = Lesson(
                    course_id=course.id,
                    title=row['lesson_title'],
                    content=row.get('lesson_content', ''),
                    order=int(row.get('lesson_order', 0)),
                    template_path=row.get('lesson_template_path', ''),
                    video_url=row.get('lesson_video_url', '')
                )
                db.session.add(lesson)
            db.session.commit()
            upload_message = 'CSV upload successful.'
        elif ext == 'json':
            # Expecting: list of {course: {...}, lessons: [...]}
            data = json.load(file)
            for entry in data:
                c = entry['course']
                course = Course.query.filter_by(title=c['title']).first()
                if not course:
                    course = Course(title=c['title'], description=c.get('description', ''), teacher_id=current_user.id)
                    db.session.add(course)
                    db.session.commit()
                for l in entry['lessons']:
                    lesson = Lesson(
                        course_id=course.id,
                        title=l['title'],
                        content=l.get('content', ''),
                        order=int(l.get('order', 0)),
                        template_path=l.get('template_path', ''),
                        video_url=l.get('video_url', '')
                    )
                    db.session.add(lesson)
            db.session.commit()
            upload_message = 'JSON upload successful.'
        else:
            upload_message = 'Unsupported file type.'
    except Exception as e:
        upload_message = f'Error: {str(e)}'
    # Show message on admin dashboard
    users = User.query.all()
    courses = Course.query.filter_by(teacher_id=current_user.id).all()
    user_enrollments = {}
    for user in users:
        enrolled_courses = [enrollment.course for enrollment in user.enrollments]
        user_enrollments[user.id] = enrolled_courses
    return render_template('admin/index.html', users=users, courses=courses, user_enrollments=user_enrollments, upload_message=upload_message)

def teacher_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_teacher():
            flash('You must be a teacher to access this page.', 'danger')
            return redirect(url_for('main.dashboard'))
        return f(*args, **kwargs)
    return decorated_function


from flask import request

@bp.route('/', methods=['GET', 'POST'])
@login_required
@teacher_required
def index():
    users = User.query.all()
    courses = Course.query.filter_by(teacher_id=current_user.id).all()
    # Build a dict: user_id -> list of enrolled course titles
    user_enrollments = {}
    for user in users:
        enrolled_courses = [enrollment.course for enrollment in user.enrollments]
        user_enrollments[user.id] = enrolled_courses
    message = None
    if request.method == 'POST':
        user_id = int(request.form['user_id'])
        course_id = int(request.form['course_id'])
        action = request.form['action']
        user = User.query.get(user_id)
        course = Course.query.get(course_id)
        if not user or not course:
            message = 'Invalid user or course.'
        else:
            enrollment = Enrollment.query.filter_by(student_id=user_id, course_id=course_id).first()
            if action == 'enrol':
                if enrollment:
                    message = f'{user.username} is already enrolled in {course.title}.'
                else:
                    new_enrollment = Enrollment(student_id=user_id, course_id=course_id)
                    db.session.add(new_enrollment)
                    db.session.commit()
                    message = f'{user.username} enrolled in {course.title}.'
            elif action == 'unenrol':
                if enrollment:
                    db.session.delete(enrollment)
                    db.session.commit()
                    message = f'{user.username} unenrolled from {course.title}.'
                else:
                    message = f'{user.username} is not enrolled in {course.title}.'
    return render_template('admin/index.html', users=users, courses=courses, user_enrollments=user_enrollments, message=message)

@bp.route('/students')
@login_required
@teacher_required
def students():
    students = User.query.filter_by(role='student').all()
    return render_template('admin/students.html', students=students)

@bp.route('/student/<int:student_id>')
@login_required
@teacher_required
def student_detail(student_id):
    student = User.query.get_or_404(student_id)
    enrollments = Enrollment.query.filter_by(student_id=student_id).all()
    
    return render_template('admin/student_detail.html', 
                         student=student, 
                         enrollments=enrollments)

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import User, Course, Enrollment
from functools import wraps

bp = Blueprint('admin', __name__, url_prefix='/admin')

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

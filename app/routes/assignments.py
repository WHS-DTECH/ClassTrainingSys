from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Assignment, Submission, Course, Enrollment
from app.forms import AssignmentForm, SubmissionForm
from datetime import datetime

bp = Blueprint('assignments', __name__, url_prefix='/assignments')

@bp.route('/course/<int:course_id>')
@login_required
def list_assignments(course_id):
    course = Course.query.get_or_404(course_id)
    assignments = Assignment.query.filter_by(course_id=course_id).all()
    
    # Get submission status for students
    submissions = {}
    if not current_user.is_teacher():
        for assignment in assignments:
            sub = Submission.query.filter_by(
                assignment_id=assignment.id,
                student_id=current_user.id
            ).first()
            submissions[assignment.id] = sub
    
    return render_template('assignments/list.html', 
                         course=course, 
                         assignments=assignments,
                         submissions=submissions)

@bp.route('/create/<int:course_id>', methods=['GET', 'POST'])
@login_required
def create_assignment(course_id):
    course = Course.query.get_or_404(course_id)
    
    if course.teacher_id != current_user.id:
        flash('You do not have permission to create assignments for this course.', 'danger')
        return redirect(url_for('courses.view_course', course_id=course_id))
    
    form = AssignmentForm()
    if form.validate_on_submit():
        assignment = Assignment(
            course_id=course_id,
            title=form.title.data,
            description=form.description.data,
            due_date=form.due_date.data,
            max_points=form.max_points.data
        )
        db.session.add(assignment)
        db.session.commit()
        flash('Assignment created successfully!', 'success')
        return redirect(url_for('assignments.list_assignments', course_id=course_id))
    
    return render_template('assignments/create.html', form=form, course=course)

@bp.route('/<int:assignment_id>')
@login_required
def view_assignment(assignment_id):
    assignment = Assignment.query.get_or_404(assignment_id)
    course = assignment.course
    
    # Check access
    if not current_user.is_teacher():
        enrollment = Enrollment.query.filter_by(
            student_id=current_user.id,
            course_id=course.id
        ).first()
        if not enrollment:
            flash('You are not enrolled in this course.', 'danger')
            return redirect(url_for('courses.list_courses'))
        
        # Get student's submission
        submission = Submission.query.filter_by(
            assignment_id=assignment_id,
            student_id=current_user.id
        ).first()
        
        return render_template('assignments/view_student.html', 
                             assignment=assignment,
                             submission=submission)
    else:
        # Teacher view - show all submissions
        submissions = Submission.query.filter_by(assignment_id=assignment_id).all()
        return render_template('assignments/view_teacher.html',
                             assignment=assignment,
                             submissions=submissions)

@bp.route('/<int:assignment_id>/submit', methods=['GET', 'POST'])
@login_required
def submit_assignment(assignment_id):
    assignment = Assignment.query.get_or_404(assignment_id)
    
    # Check if already submitted
    existing = Submission.query.filter_by(
        assignment_id=assignment_id,
        student_id=current_user.id
    ).first()
    
    form = SubmissionForm()
    if form.validate_on_submit():
        if existing:
            existing.content = form.content.data
            existing.submitted_at = datetime.utcnow()
        else:
            submission = Submission(
                assignment_id=assignment_id,
                student_id=current_user.id,
                content=form.content.data
            )
            db.session.add(submission)
        
        db.session.commit()
        flash('Assignment submitted successfully!', 'success')
        return redirect(url_for('assignments.view_assignment', assignment_id=assignment_id))
    
    # Pre-fill form if resubmitting
    if existing and request.method == 'GET':
        form.content.data = existing.content
    
    return render_template('assignments/submit.html', form=form, assignment=assignment)

@bp.route('/submission/<int:submission_id>/grade', methods=['POST'])
@login_required
def grade_submission(submission_id):
    if not current_user.is_teacher():
        flash('Only teachers can grade submissions.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    submission = Submission.query.get_or_404(submission_id)
    
    score = request.form.get('score', type=int)
    feedback = request.form.get('feedback', '')
    
    submission.score = score
    submission.feedback = feedback
    submission.graded = True
    submission.graded_at = datetime.utcnow()
    
    db.session.commit()
    flash('Submission graded successfully!', 'success')
    
    return redirect(url_for('assignments.view_assignment', assignment_id=submission.assignment_id))

from flask import Blueprint, render_template, request, session, redirect, url_for
from flask import send_file, flash
from flask_login import login_required, current_user
from app.models import Course, Enrollment, Assignment, Submission, Quiz, QuizAttempt, User, CommentCheck
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from sqlalchemy import func
from datetime import datetime

bp = Blueprint('main', __name__)

# PDF download for extracted debug blocks and feedback (Lesson 2)
@bp.route('/lesson2/download_debug_feedback')
@login_required
def download_lesson2_debug_feedback():
    # Get debug blocks and feedback from session
    extracted_debug_blocks = session.get('lesson2_debug_blocks')
    uploaded_filename = session.get('uploaded_filename', 'Debug_Feedback')
    from datetime import datetime
    import io
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    if not extracted_debug_blocks:
        flash('No extracted debug blocks found. Please extract debug blocks first.', 'danger')
        return redirect(url_for('main.practice_debug_checker'))
    today = datetime.now().strftime('%Y-%m-%d')
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    y = height - 50
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, y, f"{uploaded_filename}")
    y -= 30
    p.setFont("Helvetica", 12)
    p.drawString(50, y, f"Date: {today}")
    y -= 30
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, y, "Lesson 2: Debug Checker - Extracted Debug Blocks")
    y -= 40
    p.setFont("Helvetica", 12)
    from reportlab.lib.utils import simpleSplit
    max_width = width - 100
    for block in extracted_debug_blocks:
        if y < 80:
            p.showPage()
            y = height - 50
            p.setFont("Helvetica", 12)
        block_lines = simpleSplit(block, "Helvetica", 12, max_width)
        for line in block_lines:
            p.drawString(50, y, line)
            y -= 16
        # Automatic feedback logic
        feedback = []
        block_lower = block.lower()
        if '# debug:' in block_lower and ('test' not in block_lower and 'issue' not in block_lower and 'fix' not in block_lower):
            feedback.append('Add a test, issue, and fix description to your DEBUG block.')
        else:
            missing = []
            if 'test' not in block_lower:
                missing.append('TEST')
            if 'issue' not in block_lower:
                missing.append('ISSUE')
            if 'fix' not in block_lower:
                missing.append('FIX')
            if not missing:
                feedback.append('Great! Your DEBUG block is complete.')
            else:
                feedback.append(f"Add a {', '.join(missing)} to your DEBUG block for full marks.")
        p.setFillColorRGB(0.2,0.2,0.7)
        for fb in feedback:
            fb_lines = simpleSplit(f"Feedback: {fb}", "Helvetica", 12, max_width - 20)
            for line in fb_lines:
                p.drawString(70, y, line)
                y -= 16
        p.setFillColorRGB(0,0,0)
        y -= 10
    p.save()
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name=f"{uploaded_filename}_debug_blocks_{today}.pdf", mimetype="application/pdf")

# Extract debug blocks utility (move to top-level, not nested)
def extract_debug_blocks(code):
    """
    Extracts debug blocks in a flexible way, handling both # DEBUG: and # DEBUG TEST: starters,
    and sub-lines with or without DEBUG, in any order, case-insensitive.
    """
    import re
    debug_blocks = []
    lines = code.splitlines()
    i = 0
    debug_line_regex = re.compile(r'#\s*DEBUG(\b|\s|:)', re.IGNORECASE)
    while i < len(lines):
        line = lines[i].strip()
        # Start of a debug block: any line starting with # DEBUG (with or without subtype/colon/word)
        if debug_line_regex.match(line):
            block = [f"{i+1}: {lines[i].strip()}"]
            j = i + 1
            # Collect subsequent lines that also start with # DEBUG (with or without subtype/colon/word)
            while j < len(lines):
                subline = lines[j].strip()
                if debug_line_regex.match(subline):
                    block.append(f"{j+1}: {lines[j].strip()}")
                    j += 1
                else:
                    break
            debug_blocks.append('\n'.join(block))
            i = j
        else:
            i += 1
    return debug_blocks

# Debug Checker Route (Practice)
@bp.route('/practice/debug_checker', methods=['GET', 'POST'])
def practice_debug_checker():
    code = None
    debug_blocks = []
    already_checked = False
    filename = request.args.get('filename')
    uploaded_filename = None
    upload_status = None
    can_extract = False
    username = current_user.username if current_user.is_authenticated else None
    if request.method == 'POST':
        print(f"[DEBUG] POST received. form: {dict(request.form)}, files: {request.files.keys()}", flush=True)
        # Handle file upload only (no extraction yet)
        if 'file' in request.files and request.files['file'].filename:
            file = request.files['file']
            uploaded_filename = file.filename
            code = file.read().decode('utf-8')
            # Normalize line endings for uploaded files
            code = code.replace('\r\n', '\n').replace('\r', '\n')
            # Only restrict for students (DebugCheck)
            from app.models import DebugCheck
            if current_user.is_authenticated and uploaded_filename and not current_user.is_teacher():
                existing = DebugCheck.query.filter_by(user_id=current_user.id, filename=uploaded_filename).first()
                if existing:
                    already_checked = True
                    upload_status = f"User '{username}' has already uploaded/checked this file in the Debug Checker. Only one upload/check is allowed."
                else:
                    can_extract = True
                    upload_status = f"File '{uploaded_filename}' uploaded by user '{username}'. Ready to extract."
            else:
                can_extract = True
                upload_status = f"File '{uploaded_filename}' uploaded by user '{username}'. Ready to extract."
            # Ensure code is always set in template context after upload
            # (so the hidden field in the extraction form is populated)
            # This is critical for extraction to work after upload
        # Handle extraction after upload
        elif 'extract_file' in request.form:
            uploaded_filename = request.form.get('uploaded_filename')
            code = request.form.get('uploaded_code')
            # Only restrict for students (DebugCheck)
            from app.models import DebugCheck
            if current_user.is_authenticated and uploaded_filename and not current_user.is_teacher():
                existing = DebugCheck.query.filter_by(user_id=current_user.id, filename=uploaded_filename).first()
                if existing:
                    already_checked = True
                    upload_status = f"User '{username}' has already uploaded/checked this file in the Debug Checker. Only one upload/check is allowed."
                else:
                    from app import db
                    new_check = DebugCheck(user_id=current_user.id, filename=uploaded_filename)
                    db.session.add(new_check)
                    db.session.commit()
                    can_extract = True
                    upload_status = f"File '{uploaded_filename}' extracted and checked for user '{username}'."
            else:
                can_extract = True
                upload_status = f"File '{uploaded_filename}' extracted for user '{username}'."
            # Extract debug blocks
            if can_extract and code:
                print("[DEBUG] Code received for extraction (file upload):\n" + code, flush=True)
                debug_blocks = extract_debug_blocks(code)
                print(f"[DEBUG] Extracted debug blocks: {debug_blocks}", flush=True)
                # Store in session for debug checker view
                session['extracted_debug_blocks'] = debug_blocks
                # Also persist for lesson 2 view
                session['lesson2_debug_blocks'] = debug_blocks
                session['uploaded_filename'] = uploaded_filename
                # Redirect to anchor after extraction
                return redirect(url_for('main.practice_debug_checker') + '#extracted-debug-blocks')
        # Handle paste/submit as before
        else:
            code = request.form.get('code', '')
            if code:
                print("[DEBUG] Code received for extraction (paste box):\n" + code, flush=True)
                debug_blocks = extract_debug_blocks(code)
                print(f"[DEBUG] Extracted debug blocks: {debug_blocks}", flush=True)
                session['extracted_debug_blocks'] = debug_blocks
                session['lesson2_debug_blocks'] = debug_blocks
                session['uploaded_filename'] = uploaded_filename


    if already_checked:
        code = None
        debug_blocks = []
        can_extract = False

    # Only set debug_blocks from session if not just extracted (i.e., not POST with extraction)
    if request.method != 'POST' and 'extracted_debug_blocks' in session:
        debug_blocks = session['extracted_debug_blocks']

    # Add a message if no debug blocks are found after extraction (file or paste)
    debug_message = None
    if can_extract and request.method == 'POST' and (not debug_blocks or len(debug_blocks) == 0):
        debug_message = "No DEBUG code blocks were found. You must include at least <b>three</b> DEBUG code blocks in your code to meet the requirement."

    # Gather checked files for this user (for sidebar grid)
    checked_files_grid = []
    if current_user.is_authenticated:
        from app.models import CommentCheck, DebugCheck
        comment_files = {c.filename for c in CommentCheck.query.filter_by(user_id=current_user.id).all()}
        debug_files = {d.filename for d in DebugCheck.query.filter_by(user_id=current_user.id).all()}
        all_files = sorted(comment_files | debug_files)
        for fname in all_files:
            checked_files_grid.append({
                'filename': fname,
                'comment': '✔️' if fname in comment_files else '',
                'debug': '✔️' if fname in debug_files else ''
            })
    return render_template('main/practice_debug_checker.html', code=code, debug_blocks=debug_blocks, already_checked=already_checked, uploaded_filename=uploaded_filename, upload_status=upload_status, can_extract=can_extract, username=username, checked_files_grid=checked_files_grid, debug_message=debug_message)

# Practice: Code Comments Extractor (copy/paste version)
@bp.route('/lesson1/download_feedback')
@login_required
def download_lesson1_feedback():
    from app.models import CommentFeedback
    from datetime import datetime
    from reportlab.lib.pagesizes import A4
    lesson_id = 46
    # Use session comments if available, else DB
    extracted_comments = None
    feedback_entries = []
    if 'extracted_comments' in session:
        extracted_comments = session['extracted_comments']
        # Ensure all entries are (line_num, comment, feedback)
        if extracted_comments and len(extracted_comments) > 0 and len(extracted_comments[0]) == 2:
            extracted_comments = [(ln, c, '') for ln, c in extracted_comments]
        session.pop('extracted_comments')  # Clear after PDF is generated
    else:
        feedback_entries = CommentFeedback.query.filter_by(user_id=current_user.id, lesson_id=lesson_id).order_by(CommentFeedback.timestamp.desc()).all()
        if feedback_entries:
            extracted_comments = [(entry.line_num, entry.comment, entry.feedback) for entry in feedback_entries]
    if not extracted_comments:
        return redirect(url_for('courses.view_lesson', lesson_id=46))

    # Get filename from first entry (all entries have same filename)
    filename = "unknown"
    # Try to get filename from session comments if available
    if 'extracted_comments' in session and extracted_comments and len(extracted_comments) > 0:
        # If session comments, try to get filename from uploaded_filename in session
        filename = session.get('uploaded_filename', 'unknown')
    elif not 'extracted_comments' in session and feedback_entries:
        filename = feedback_entries[0].filename if feedback_entries else "Comment Feedback"
    today = datetime.now().strftime('%Y-%m-%d')

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    y = height - 50
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, y, f"{filename}")
    y -= 30
    p.setFont("Helvetica", 12)
    p.drawString(50, y, f"Date: {today}")
    y -= 30
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, y, "Lesson 1: Comment Checker - Feedback")
    y -= 40
    p.setFont("Helvetica", 12)
    from reportlab.lib.utils import simpleSplit
    max_width = width - 100
    for line_num, comment, feedback in extracted_comments:
        if y < 80:
            p.showPage()
            y = height - 50
            p.setFont("Helvetica", 12)
        # Word-wrap comment
        comment_lines = simpleSplit(f"Line {line_num}: {comment}", "Helvetica", 12, max_width)
        for line in comment_lines:
            p.drawString(50, y, line)
            y -= 16
        # Word-wrap feedback
        p.setFillColorRGB(0.2,0.2,0.7)
        feedback_lines = simpleSplit(f"Feedback: {feedback}", "Helvetica", 12, max_width - 20)
        for line in feedback_lines:
            p.drawString(70, y, line)
            y -= 16
        p.setFillColorRGB(0,0,0)
        y -= 10
    p.save()
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name=f"{filename}_feedback_{today}.pdf", mimetype="application/pdf")
@bp.route('/practice/code-comments', methods=['GET', 'POST'])
def practice_code_comments():
    from flask import flash
    from app.models import CommentCheck, DebugCheck
    code = None
    comment_lines = []
    already_checked = False
    filename = request.args.get('filename')  # Pass filename as query param if needed
    uploaded_filename = None
    upload_status = None
    can_extract = False
    username = current_user.username if current_user.is_authenticated else None
    extracted_comments_for_session = []  # Always define at the start
    if request.method == 'POST':
        # Handle file upload only (no extraction yet)
        if 'file' in request.files and request.files['file'].filename:
            file = request.files['file']
            uploaded_filename = file.filename
            code = file.read().decode('utf-8')
            if current_user.is_authenticated and uploaded_filename:
                # Restrict only students to one check per file
                is_teacher = hasattr(current_user, 'is_teacher') and current_user.is_teacher()
                if not is_teacher:
                    existing = CommentCheck.query.filter_by(user_id=current_user.id, filename=uploaded_filename).first()
                    if existing:
                        already_checked = True
                        upload_status = f"User '{username}' has already uploaded/checked this file. Only one upload/check is allowed."
                    else:
                        from app import db
                        new_check = CommentCheck(user_id=current_user.id, filename=uploaded_filename)
                        db.session.add(new_check)
                        db.session.commit()
                        can_extract = True
                        upload_status = f"File '{uploaded_filename}' uploaded by user '{username}'. Ready to extract."
                else:
                    # Teachers can always check/upload
                    from app import db
                    new_check = CommentCheck(user_id=current_user.id, filename=uploaded_filename)
                    db.session.add(new_check)
                    db.session.commit()
                    can_extract = True
                    upload_status = f"File '{uploaded_filename}' uploaded by user '{username}'. Ready to extract."
            else:
                can_extract = True
                upload_status = f"File '{uploaded_filename}' uploaded by user '{username}'. Ready to extract."
        # Handle extraction after upload
        elif 'extract_file' in request.form:
            uploaded_filename = request.form.get('uploaded_filename')
            code = request.form.get('uploaded_code')
            if current_user.is_authenticated and uploaded_filename:
                is_teacher = hasattr(current_user, 'is_teacher') and current_user.is_teacher()
                if not is_teacher:
                    existing = CommentCheck.query.filter_by(user_id=current_user.id, filename=uploaded_filename).first()
                    if existing:
                        already_checked = True
                        upload_status = f"User '{username}' has already uploaded/checked this file. Only one upload/check is allowed."
                    else:
                        from app import db
                        new_check = CommentCheck(user_id=current_user.id, filename=uploaded_filename)
                        db.session.add(new_check)
                        db.session.commit()
                        can_extract = True
                        upload_status = f"File '{uploaded_filename}' extracted and checked for user '{username}'."
                else:
                    from app import db
                    new_check = CommentCheck(user_id=current_user.id, filename=uploaded_filename)
                    db.session.add(new_check)
                    db.session.commit()
                # Save extracted comments with feedback and filename to session for lesson view and PDF
                if extracted_comments_for_session:
                    session['extracted_comments'] = extracted_comments_for_session
                    if uploaded_filename:
                        session['uploaded_filename'] = uploaded_filename
                can_extract = True
                upload_status = f"File '{uploaded_filename}' extracted for user '{username}'."
            # Extract all comments (lines starting with # or inline after code)
            if can_extract and code:
                from app import db
                from app.models import CommentFeedback
                lesson_id = 46  # Lesson 1: Comment Checker
                save_filename = uploaded_filename or filename or "unknown"
                extracted_comments_for_session.clear()
                for idx, line in enumerate(code.splitlines(), start=1):
                    if '#' in line:
                        comment_index = line.find('#')
                        comment = line[comment_index:].strip()
                        if comment:
                            # Feedback logic
                            if 'http' in comment or 'www.' in comment:
                                feedback = "This comment appears to be a pasted URL. Comments should explain your code, not just link to resources."
                            elif 'print(' in comment:
                                feedback = "This comment is just a commented-out line of code. Good comments should explain why the code is there or what it does, not just repeat the code."
                            elif len(comment) < 15:
                                feedback = "This comment is too short or vague. Try to be more descriptive and explain the purpose of the code."
                            else:
                                feedback = "This comment is clear and descriptive. Well done!"
                            comment_lines.append((idx, comment))
                            extracted_comments_for_session.append((idx, comment, feedback))
                            # Save to DB
                            if current_user.is_authenticated:
                                exists = CommentFeedback.query.filter_by(user_id=current_user.id, lesson_id=lesson_id, filename=save_filename, line_num=idx).first()
                                if not exists:
                                    db.session.add(CommentFeedback(
                                        user_id=current_user.id,
                                        lesson_id=lesson_id,
                                        filename=save_filename,
                                        line_num=idx,
                                        comment=comment,
                                        feedback=feedback
                                    ))
                db.session.commit()
                # Save extracted comments with feedback to session for lesson view
                if extracted_comments_for_session:
                    session['extracted_comments'] = extracted_comments_for_session
                # If the extract was triggered and go_to_lesson is present, redirect to lesson 1
                if 'go_to_lesson' in request.form:
                    return redirect(url_for('courses.view_lesson', lesson_id=46) + '#extracted-comments')
        # Handle paste/submit as before
        else:
            code = request.form.get('code', '')
            # Extract all comments (lines starting with # or inline after code)
            if code:
                from app import db
                from app.models import CommentFeedback
                lesson_id = 46  # Lesson 1: Comment Checker
                save_filename = filename or "unknown"
                for idx, line in enumerate(code.splitlines(), start=1):
                    if '#' in line:
                        comment_index = line.find('#')
                        comment = line[comment_index:].strip()
                        if comment:
                            # Feedback logic
                            if 'http' in comment or 'www.' in comment:
                                feedback = "This comment appears to be a pasted URL. Comments should explain your code, not just link to resources."
                            elif 'print(' in comment:
                                feedback = "This comment is just a commented-out line of code. Good comments should explain why the code is there or what it does, not just repeat the code."
                            elif len(comment) < 15:
                                feedback = "This comment is too short or vague. Try to be more descriptive and explain the purpose of the code."
                            else:
                                feedback = "This comment is clear and descriptive. Well done!"
                            comment_lines.append((idx, comment))
                            # Save to DB
                            if current_user.is_authenticated:
                                exists = CommentFeedback.query.filter_by(user_id=current_user.id, lesson_id=lesson_id, filename=save_filename, line_num=idx).first()
                                if not exists:
                                    db.session.add(CommentFeedback(
                                        user_id=current_user.id,
                                        lesson_id=lesson_id,
                                        filename=save_filename,
                                        line_num=idx,
                                        comment=comment,
                                        feedback=feedback
                                    ))
                db.session.commit()
            # Restriction: Only allow one check per user per filename (on submit/paste)
            if current_user.is_authenticated and filename:
                is_teacher = hasattr(current_user, 'is_teacher') and current_user.is_teacher()
                if not is_teacher:
                    existing = CommentCheck.query.filter_by(user_id=current_user.id, filename=filename).first()
                    if existing:
                        already_checked = True
                        upload_status = f"User '{username}' has already checked this file. Only one check is allowed."
                    else:
                        from app import db
                        new_check = CommentCheck(user_id=current_user.id, filename=filename)
                        db.session.add(new_check)
                        db.session.commit()
                else:
                    from app import db
                    new_check = CommentCheck(user_id=current_user.id, filename=filename)
                    db.session.add(new_check)
                    db.session.commit()
            # If user clicked Go to Lesson 1, store comments and feedback in session and redirect
            if 'go_to_lesson' in request.form and not already_checked:
                extracted_comments_for_session = []
                for idx, comment in comment_lines:
                    # Find feedback for this line
                    feedback = ""
                    # Try to match feedback logic as above
                    if 'http' in comment or 'www.' in comment:
                        feedback = "This comment appears to be a pasted URL. Comments should explain your code, not just link to resources."
                    elif 'print(' in comment:
                        feedback = "This comment is just a commented-out line of code. Good comments should explain why the code is there or what it does, not just repeat the code."
                    elif len(comment) < 15:
                        feedback = "This comment is too short or vague. Try to be more descriptive and explain the purpose of the code."
                    else:
                        feedback = "This comment is clear and descriptive. Well done!"
                    extracted_comments_for_session.append((idx, comment, feedback))
                session['extracted_comments'] = extracted_comments_for_session
                return redirect(url_for('courses.view_lesson', lesson_id=46))
    # If already checked, do not show code or comments
    if already_checked:
        code = None
        comment_lines = []
        can_extract = False
    # Gather checked files for this user (student or teacher)
    checked_files_grid = []
    is_teacher = False
    if current_user.is_authenticated:
        from app.models import DebugCheck
        is_teacher = hasattr(current_user, 'is_teacher') and current_user.is_teacher()
        if is_teacher:
            # Show only debug checks the teacher has done themselves
            debug_files = {d.filename for d in DebugCheck.query.filter_by(user_id=current_user.id).all()}
            all_files = sorted(debug_files)
            for fname in all_files:
                checked_files_grid.append({
                    'filename': fname,
                    'comment': '',
                    'debug': '✔️'
                })
        else:
            from app.models import CommentCheck
            # Show only files the student has checked themselves
            comment_files = {c.filename for c in CommentCheck.query.filter_by(user_id=current_user.id).all()}
            debug_files = {d.filename for d in DebugCheck.query.filter_by(user_id=current_user.id).all()}
            all_files = sorted(comment_files | debug_files)
            for fname in all_files:
                checked_files_grid.append({
                    'filename': fname,
                    'comment': '✔️' if fname in comment_files else '',
                    'debug': '✔️' if fname in debug_files else ''
                })
    return render_template('main/practice_code_comments.html', code=code, comment_lines=comment_lines, already_checked=already_checked, uploaded_filename=uploaded_filename, upload_status=upload_status, can_extract=can_extract, username=username, checked_files_grid=checked_files_grid, is_teacher=is_teacher)

@bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('index.html')

@bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_teacher():
        # Teacher dashboard
        courses = Course.query.filter_by(teacher_id=current_user.id).all()
        total_students = db.session.query(func.count(Enrollment.id.distinct())).\
            join(Course).filter(Course.teacher_id == current_user.id).scalar()

        # Always preview as the user with username 'student'
        preview_user = User.query.filter_by(username='student').first()
        enrollments = []
        pending_assignments = []
        if preview_user:
            enrollments = Enrollment.query.filter_by(student_id=preview_user.id).all()
            # Get pending assignments for preview user
            for enrollment in enrollments:
                assignments = Assignment.query.filter_by(course_id=enrollment.course_id).all()
                for assignment in assignments:
                    submission = Submission.query.filter_by(
                        assignment_id=assignment.id,
                        student_id=preview_user.id
                    ).first()
                    if not submission:
                        pending_assignments.append(assignment)

        return render_template('dashboard/teacher.html',
            courses=courses,
            total_students=total_students,
            preview_enrollments=enrollments,
            preview_pending_assignments=pending_assignments[:5],
            preview_user=preview_user
        )
    else:
        # Student dashboard
        enrollments = Enrollment.query.filter_by(student_id=current_user.id).all()
        # Get pending assignments
        pending_assignments = []
        for enrollment in enrollments:
            assignments = Assignment.query.filter_by(course_id=enrollment.course_id).all()
            for assignment in assignments:
                submission = Submission.query.filter_by(
                    assignment_id=assignment.id, 
                    student_id=current_user.id
                ).first()
                if not submission:
                    pending_assignments.append(assignment)
        return render_template('dashboard/student_dashboard_page.html',
            preview_user=current_user,
            preview_enrollments=enrollments,
            preview_pending_assignments=pending_assignments[:5]
        )

# Standalone student dashboard route for macro-based rendering
@bp.route('/student_dashboard')
@login_required
def student_dashboard():
    enrollments = Enrollment.query.filter_by(student_id=current_user.id).all()
    pending_assignments = []
    for enrollment in enrollments:
        assignments = Assignment.query.filter_by(course_id=enrollment.course_id).all()
        for assignment in assignments:
            submission = Submission.query.filter_by(
                assignment_id=assignment.id, 
                student_id=current_user.id
            ).first()
            if not submission:
                pending_assignments.append(assignment)
    return render_template('dashboard/student_dashboard_page.html',
        preview_user=current_user,
        preview_enrollments=enrollments,
        preview_pending_assignments=pending_assignments[:5]
    )

from flask import redirect, url_for
from app import db

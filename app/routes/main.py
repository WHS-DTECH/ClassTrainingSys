from flask import Blueprint, render_template, request, session, redirect, url_for
from flask import send_file, flash
from flask_login import login_required, current_user
from app.models import Course, Enrollment, Assignment, Submission, Quiz, QuizAttempt, User, CommentCheck
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from sqlalchemy import func
from datetime import datetime
import hashlib

bp = Blueprint('main', __name__)

# PDF download for extracted comments and feedback
@bp.route('/download_comments_pdf', methods=['POST'])
@login_required
def download_comments_pdf():
    from flask import make_response
    code = request.form.get('code', '')
    code_str = str(code) if code is not None else ""
    uploaded_filename = request.form.get('uploaded_filename', 'Extracted_Comments')
    today_str = datetime.now().strftime('%Y-%m-%d')
    pdf_filename = f"{uploaded_filename}_comments_{today_str}.pdf"
    # Compute code hash for strict filtering
    code_hash = hashlib.sha256(code_str.encode('utf-8')).hexdigest()
    # Unified logic: match web view
    comment_lines = []
    feedback_dict = {}
    already_checked = False
    from app.models import CommentFeedback, Lesson
    template_path = "modules/module3/m3lesson1.html"
    lesson = Lesson.query.filter_by(template_path=template_path).first()
    if lesson:
        lesson_id = lesson.id
        feedback_entries = CommentFeedback.query.filter_by(
            user_id=current_user.id,
            lesson_id=lesson_id,
            filename=uploaded_filename,
            code_hash=code_hash
        ).order_by(CommentFeedback.line_num).all()
        if feedback_entries:
            already_checked = True
            for entry in feedback_entries:
                comment_lines.append((entry.line_num, entry.comment))
                feedback_dict[entry.line_num] = entry.feedback
    if not already_checked:
        # Use session data if not checked
        comment_lines = session.get('comment_lines', [])
        feedback_dict = session.get('feedback_dict', {})
    # Generate PDF
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    y = height - 40
    p.setFont("Helvetica-Bold", 14)
    p.drawString(40, y, f"Extracted Comments for: {uploaded_filename}")
    y -= 24
    p.setFont("Helvetica", 12)
    p.drawString(40, y, f"Date: {today_str}")
    y -= 30
    p.setFont("Helvetica", 11)
    p.drawString(40, y, "Code:")
    y -= 18
    p.setFont("Courier", 9)
    for line in code.splitlines():
        if y < 60:
            p.showPage()
            y = height - 40
            p.setFont("Courier", 9)
        p.drawString(50, y, line)
        y -= 12
    y -= 18
    p.setFont("Helvetica-Bold", 12)
    p.drawString(40, y, "Extracted Comments and Feedback:")
    y -= 18
    p.setFont("Helvetica", 10)
    if comment_lines:
        for idx, (line_num, comment) in enumerate(comment_lines):
            if y < 60:
                p.showPage()
                y = height - 40
                p.setFont("Helvetica", 10)
            p.drawString(50, y, f"Line {line_num}: {comment}")
            y -= 12
            p.setFont("Helvetica-Oblique", 9)
            feedback = feedback_dict.get(line_num, '(No feedback available)')
            p.drawString(70, y, f"Feedback: {feedback}")
            y -= 16
            p.setFont("Helvetica", 10)
    else:
        p.drawString(50, y, "No comments found.")
    p.save()
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name=pdf_filename, mimetype='application/pdf')

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
            from app.models import DebugCheck
            if current_user.is_authenticated and uploaded_filename:
                if current_user.is_teacher():
                    can_extract = True
                    upload_status = f"File '{uploaded_filename}' uploaded by user '{username}'. Ready to extract."
                else:
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
            from app.models import DebugCheck
            from app import db
            if current_user.is_authenticated and uploaded_filename:
                if current_user.is_teacher():
                    # Always create a DebugCheck record for teachers on extraction attempt
                    existing = DebugCheck.query.filter_by(user_id=current_user.id, filename=uploaded_filename).first()
                    if not existing:
                        new_check = DebugCheck(user_id=current_user.id, filename=uploaded_filename)
                        db.session.add(new_check)
                        db.session.commit()
                    can_extract = True
                    upload_status = f"File '{uploaded_filename}' extracted for user '{username}'."
                else:
                    existing = DebugCheck.query.filter_by(user_id=current_user.id, filename=uploaded_filename).first()
                    if existing:
                        already_checked = True
                        upload_status = f"User '{username}' has already uploaded/checked this file in the Debug Checker. Only one upload/check is allowed."
                    else:
                        new_check = DebugCheck(user_id=current_user.id, filename=uploaded_filename)
                        db.session.add(new_check)
                        db.session.commit()
                        can_extract = True
                        upload_status = f"File '{uploaded_filename}' extracted and checked for user '{username}'."
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
        # Do not clear code for teachers, only for students who have already checked
        if not (current_user.is_authenticated and current_user.is_teacher()):
            code = None
            debug_blocks = []
            can_extract = False
    # If already checked, fetch comments and feedback from DB for display
    if already_checked:
        # Don't clear code/comments; fetch from DB
        comment_lines = []
        feedback_entries = []
        if current_user.is_authenticated and (uploaded_filename or filename):
            from app.models import CommentFeedback, Lesson
            template_path = "modules/module3/m3lesson1.html"
            lesson = Lesson.query.filter_by(template_path=template_path).first()
            if lesson:
                lesson_id = lesson.id
                file_to_check = uploaded_filename or filename or "unknown"
                feedback_entries = CommentFeedback.query.filter_by(user_id=current_user.id, lesson_id=lesson_id, filename=file_to_check).order_by(CommentFeedback.line_num).all()
                for entry in feedback_entries:
                    comment_lines.append((entry.line_num, entry.comment))
        can_extract = False

    # Only set debug_blocks from session if not just extracted (i.e., not POST with extraction)
    if request.method != 'POST' and 'extracted_debug_blocks' in session:
        debug_blocks = session['extracted_debug_blocks']

    # Add a message if no debug blocks are found after extraction (file or paste)
    debug_message = None
    # Only show the message if the user just tried to extract (not on upload or GET)
    if request.method == 'POST' and 'extract_file' in request.form and (not debug_blocks or len(debug_blocks) == 0):
        debug_message = "No DEBUG code blocks were found. You must include at least <b>three</b> DEBUG code blocks in your code to meet the requirement."

    # Gather checked files for this user (for sidebar grid)
    checked_files_grid = []
    if current_user.is_authenticated:
        from app.models import CommentCheck, DebugCheck
        comment_files = {c.filename for c in CommentCheck.query.filter_by(user_id=current_user.id).all()}
        # For teachers, always show all files they've checked (all DebugCheck records)
        if current_user.is_teacher():
            debug_files = {d.filename for d in DebugCheck.query.filter_by(user_id=current_user.id).all()}
        else:
            debug_files = {d.filename for d in DebugCheck.query.filter_by(user_id=current_user.id).all()}
        all_files = sorted(comment_files | debug_files)
        for fname in all_files:
            checked_files_grid.append({
                'filename': fname,
                'comment': '✔️' if fname in comment_files else '',
                'debug': '✔️' if fname in debug_files else ''
            })

    return render_template('main/practice_debug_checker.html', code=code, debug_blocks=debug_blocks, already_checked=already_checked, uploaded_filename=uploaded_filename, upload_status=upload_status, can_extract=can_extract, username=username, checked_files_grid=checked_files_grid, debug_message=debug_message)

# PDF download for extracted debug blocks and feedback
@bp.route('/download_debug_blocks_pdf', methods=['POST'])
@login_required
def download_debug_blocks_pdf():
    from flask import make_response
    code = request.form.get('code', '')
    if not code:
        code = session.get('uploaded_code', '')
    uploaded_filename = request.form.get('uploaded_filename', '').strip()
    if not uploaded_filename or uploaded_filename == 'None':
        uploaded_filename = session.get('uploaded_filename', 'Extracted_DebugBlocks')
    debug_blocks = session.get('extracted_debug_blocks', [])
    today_str = datetime.now().strftime('%Y-%m-%d')
    pdf_filename = f"{uploaded_filename}_debug_blocks_{today_str}.pdf"
    # Generate PDF
    buffer = io.BytesIO()
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    from reportlab.lib.utils import simpleSplit
    width, height = letter
    y = height - 40
    p = canvas.Canvas(buffer, pagesize=letter)
    p.setFont("Helvetica-Bold", 16)
    p.drawString(40, y, f"{uploaded_filename}")
    y -= 28
    p.setFont("Helvetica", 12)
    p.drawString(40, y, f"Date: {today_str}")
    y -= 30
    p.setFont("Helvetica-Bold", 13)
    p.drawString(40, y, "Lesson 2: Debug Checker - Extracted Debug Blocks")
    y -= 28
    p.setFont("Helvetica", 11)
    p.drawString(40, y, "Code:")
    y -= 18
    p.setFont("Courier", 9)
    if code.strip():
        for line in code.splitlines():
            if y < 60:
                p.showPage()
                y = height - 40
                p.setFont("Courier", 9)
            p.drawString(50, y, line)
            y -= 12
    else:
        p.drawString(50, y, "(No code provided)")
        y -= 12
    y -= 18
    p.setFont("Helvetica-Bold", 12)
    p.drawString(40, y, "Extracted Debug Blocks and Feedback:")
    y -= 18
    p.setFont("Helvetica", 10)
    if debug_blocks:
        for block in debug_blocks:
            if y < 60:
                p.showPage()
                y = height - 40
                p.setFont("Helvetica", 10)
            block_lines = simpleSplit(block, "Helvetica", 10, width - 100)
            for line in block_lines:
                p.drawString(50, y, line)
                y -= 12
            # Feedback logic (same as template)
            block_lower = block.lower()
            if '# debug:' in block_lower and ('test' not in block_lower and 'issue' not in block_lower and 'fix' not in block_lower):
                feedback = 'Add a test, issue, and fix description to your DEBUG block.'
            else:
                missing = []
                if 'test' not in block_lower:
                    missing.append('TEST')
                if 'issue' not in block_lower:
                    missing.append('ISSUE')
                if 'fix' not in block_lower:
                    missing.append('FIX')
                if not missing:
                    feedback = 'Great! Your DEBUG block is complete.'
                else:
                    feedback = f"Add a {', '.join(missing)} to your DEBUG block for full marks."
            p.setFont("Helvetica-Oblique", 9)
            p.setFillColorRGB(0.2,0.2,0.7)
            feedback_lines = simpleSplit(f"Feedback: {feedback}", "Helvetica-Oblique", 9, width - 120)
            for line in feedback_lines:
                p.drawString(70, y, line)
                y -= 12
            p.setFillColorRGB(0,0,0)
            y -= 10
    p.save()
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name=pdf_filename, mimetype="application/pdf")

# Practice: Code Comments Extractor (copy/paste version)
@bp.route('/lesson1/download_feedback', methods=['POST'])
@login_required
def download_lesson1_feedback():
    from app.models import CommentFeedback
    from datetime import datetime
    from reportlab.lib.pagesizes import A4
    # Dynamically get lesson_id by template_path
    from app.models import Lesson
    template_path = "modules/module3/m3lesson1.html"
    lesson = Lesson.query.filter_by(template_path=template_path).first()
    if not lesson:
        return "Lesson for comment checker not found.", 404
    lesson_id = lesson.id
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
        return "No extracted comments found for this lesson.", 404

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
    extracted_feedback_for_session = []
    feedback_entries = []
    checked_files_grid = []
    is_teacher = False
    feedback_dict = {}
    if request.method == 'POST':
        # Handle file upload only (no extraction yet)
        if 'file' in request.files and request.files['file'].filename:
            file = request.files['file']
            uploaded_filename = file.filename
            try:
                code = file.read().decode('utf-8')
            except (UnicodeDecodeError, AttributeError) as e:
                return f"Error reading file: {str(e)}", 400
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
            # Return immediately after file upload to show extract button
            # Build checked_files_grid before returning
            checked_files_grid = []
            is_teacher = False
            if current_user.is_authenticated:
                from app.models import CommentCheck as CommentCheckModel, DebugCheck
                is_teacher = hasattr(current_user, 'is_teacher') and current_user.is_teacher()
                comment_files = {c.filename for c in CommentCheckModel.query.filter_by(user_id=current_user.id).all()}
                debug_files = {d.filename for d in DebugCheck.query.filter_by(user_id=current_user.id).all()}
                all_files = sorted(comment_files | debug_files)
                for fname in all_files:
                    checked_files_grid.append({
                        'filename': fname,
                        'comment': '✔️' if fname in comment_files else '',
                        'debug': '✔️' if fname in debug_files else ''
                    })
            return render_template('main/practice_code_comments.html', code=code, comment_lines=[], already_checked=already_checked, uploaded_filename=uploaded_filename, upload_status=upload_status, can_extract=can_extract, username=username, checked_files_grid=checked_files_grid, is_teacher=is_teacher, feedback_dict={})
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
                can_extract = True
                upload_status = f"File '{uploaded_filename}' extracted for user '{username}'."
            # Extract all comments (lines starting with # or inline after code)
            if can_extract and code:
                from app import db
                from app.models import CommentFeedback, Lesson
                template_path = "modules/module3/m3lesson1.html"
                lesson = Lesson.query.filter_by(template_path=template_path).first()
                if not lesson:
                    return "Lesson for comment checker not found.", 404
                lesson_id = lesson.id
                save_filename = uploaded_filename or filename or "unknown"
                extracted_comments_for_session.clear()
                # Compute code hash for deduplication
                code_hash = hashlib.sha256(code.encode('utf-8')).hexdigest()
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
                            extracted_feedback_for_session.append((idx, feedback))
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
                                        feedback=feedback,
                                        code_hash=code_hash
                                    ))
                db.session.commit()
                # Always fetch feedback for this file from DB for display
                feedback_entries = CommentFeedback.query.filter_by(user_id=current_user.id, lesson_id=lesson_id, filename=save_filename).order_by(CommentFeedback.line_num).all()
                # Instead of redirecting, just show results on this page
        # Handle paste/submit as before
        else:
            code = request.form.get('code', '')
            # Extract all comments (lines starting with # or inline after code)
            if code:
                from app import db
                from app.models import CommentFeedback, Lesson
                template_path = "modules/module3/m3lesson1.html"
                lesson = Lesson.query.filter_by(template_path=template_path).first()
                if not lesson:
                    return "Lesson for comment checker not found.", 404
                lesson_id = lesson.id
                save_filename = filename or "unknown"
                # Compute code hash for deduplication
                code_hash = hashlib.sha256(code.encode('utf-8')).hexdigest()
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
                                        feedback=feedback,
                                        code_hash=code_hash
                                    ))
                db.session.commit()
                # Always fetch feedback for this file from DB for display
                feedback_entries = CommentFeedback.query.filter_by(user_id=current_user.id, lesson_id=lesson_id, filename=save_filename).order_by(CommentFeedback.line_num).all()
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
            # If user clicked Extract Comments, show results on this page
            if 'extract_file' in request.form and not already_checked:
                extracted_comments_for_session = []
                for idx, comment in comment_lines:
                    feedback = ""
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
                # Build feedback dict for template
                feedback_dict = {idx: feedback for idx, _, feedback in extracted_comments_for_session}
                return render_template('main/practice_code_comments.html', code=code, comment_lines=comment_lines, already_checked=already_checked, uploaded_filename=uploaded_filename, upload_status=upload_status, can_extract=can_extract, username=username, checked_files_grid=checked_files_grid, is_teacher=is_teacher, feedback_dict=feedback_dict)
    # If already checked, fetch comments and feedback from DB for display
    if already_checked:
        # Don't clear code/comments; fetch from DB
        comment_lines = []
        feedback_entries = []
        if current_user.is_authenticated and (uploaded_filename or filename):
            from app.models import CommentFeedback, Lesson
            template_path = "modules/module3/m3lesson1.html"
            lesson = Lesson.query.filter_by(template_path=template_path).first()
            if lesson:
                lesson_id = lesson.id
                file_to_check = uploaded_filename or filename or "unknown"
                feedback_entries = CommentFeedback.query.filter_by(user_id=current_user.id, lesson_id=lesson_id, filename=file_to_check).order_by(CommentFeedback.line_num).all()
                for entry in feedback_entries:
                    comment_lines.append((entry.line_num, entry.comment))
        can_extract = False
    
    # Populate checked files grid and teacher status if not already set
    if not checked_files_grid:
        if current_user.is_authenticated:
            from app.models import CommentCheck, DebugCheck
            is_teacher = hasattr(current_user, 'is_teacher') and current_user.is_teacher()
            # Show both comment and debug checked files for both teachers and students
            comment_files = {c.filename for c in CommentCheck.query.filter_by(user_id=current_user.id).all()}
            debug_files = {d.filename for d in DebugCheck.query.filter_by(user_id=current_user.id).all()}
            all_files = sorted(comment_files | debug_files)
            for fname in all_files:
                checked_files_grid.append({
                    'filename': fname,
                    'comment': '✔️' if fname in comment_files else '',
                    'debug': '✔️' if fname in debug_files else ''
                })
    # Always fetch feedback for the current file for display
    if current_user.is_authenticated and (uploaded_filename or filename):
        from app.models import CommentFeedback, Lesson
        template_path = "modules/module3/m3lesson1.html"
        lesson = Lesson.query.filter_by(template_path=template_path).first()
        if lesson:
            lesson_id = lesson.id
            file_to_check = uploaded_filename or filename or "unknown"
            feedback_entries = CommentFeedback.query.filter_by(user_id=current_user.id, lesson_id=lesson_id, filename=file_to_check).order_by(CommentFeedback.line_num).all()
    # Build a feedback dict for template: line_num -> feedback
    feedback_dict = {entry.line_num: entry.feedback for entry in feedback_entries} if feedback_entries else {}
    return render_template('main/practice_code_comments.html', code=code, comment_lines=comment_lines, already_checked=already_checked, uploaded_filename=uploaded_filename, upload_status=upload_status, can_extract=can_extract, username=username, checked_files_grid=checked_files_grid, is_teacher=is_teacher, feedback_dict=feedback_dict)

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

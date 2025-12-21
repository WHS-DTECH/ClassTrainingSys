from app import create_app, db
from app.models import Lesson

def update_conventions_layout(lesson_id):
    app = create_app()
    with app.app_context():
        lesson = Lesson.query.get(lesson_id)
        if lesson:
            lesson.content = """
<h2>Section 1: Python Comments - Best Practices</h2>
<p>Follow these conventions to write clear, effective comments in your Python code:</p>
<style>
.comment-conventions-row { display: flex; gap: 2em; margin-bottom: 1em; }
.comment-conventions-col { flex: 1; min-width: 200px; }
.comment-conventions-col ul { padding-left: 1.2em; }
</style>
<div class="comment-conventions-row">
  <div class="comment-conventions-col">
    <h3>Conventions 1–5</h3>
    <ul>
      <li><b>Convention 1:</b> Use complete sentences for comments.<br><i>Write comments as full sentences to improve clarity and professionalism.</i></li>
      <li><b>Convention 2:</b> Keep comments concise and relevant.<br><i>Only include information that helps understand the code; avoid unnecessary details.</i></li>
      <li><b>Convention 3:</b> Update comments when code changes.<br><i>Always revise comments to match the current code to prevent confusion.</i></li>
      <li><b>Convention 4:</b> Avoid obvious comments.<br><i>Don't state what is already clear from the code itself.</i></li>
      <li><b>Convention 5:</b> Use proper grammar and spelling.<br><i>Well-written comments are easier to read and look more professional.</i></li>
    </ul>
  </div>
  <div class="comment-conventions-col">
    <h3>Conventions 6–7</h3>
    <ul>
      <li><b>Convention 6:</b> Explain why, not just what.<br><i>Describe the reasoning or intent behind code decisions, not just what the code does.</i></li>
      <li><b>Convention 7:</b> Use TODO/FIXME tags for future work or known issues.<br><i>Mark places in the code that need attention or improvement.</i></li>
    </ul>
  </div>
</div>
"""
            db.session.commit()
            print(f'Lesson {lesson_id} conventions layout updated.')
        else:
            print(f'Lesson {lesson_id} not found.')

def update_js_conventions_layout(lesson_id):
    app = create_app()
    with app.app_context():
        lesson = Lesson.query.get(lesson_id)
        if lesson:
            lesson.content = """
<h2>Section 2: JavaScript Comments - Best Practices</h2>
<p>Follow these conventions to write clear, effective comments in your JavaScript code:</p>
<style>
.comment-conventions-row { display: flex; gap: 2em; margin-bottom: 1em; }
.comment-conventions-col { flex: 1; min-width: 200px; }
.comment-conventions-col ul { padding-left: 1.2em; }
</style>
<div class="comment-conventions-row">
  <div class="comment-conventions-col">
    <h3>Conventions 1–5</h3>
    <ul>
      <li><b>Convention 1:</b> Use JSDoc or block comments for functions and complex logic.<br><i>Document parameters, return values, and side effects for better maintainability.</i></li>
      <li><b>Convention 2:</b> Use single-line comments (<code>//</code>) for brief notes.<br><i>Keep inline comments short and to the point.</i></li>
      <li><b>Convention 3:</b> Avoid commenting out large blocks of old code.<br><i>Remove unused code from the codebase to keep it clean.</i></li>
      <li><b>Convention 4:</b> Keep comments up to date.<br><i>Update or remove comments that no longer apply after code changes.</i></li>
      <li><b>Convention 5:</b> Use comments to clarify tricky or non-obvious code.<br><i>Help future readers understand complex logic or workarounds.</i></li>
    </ul>
  </div>
  <div class="comment-conventions-col">
    <h3>Conventions 6–7</h3>
    <ul>
      <li><b>Convention 6:</b> Explain why, not just what.<br><i>Describe the reasoning or intent behind code, especially for hacks or workarounds.</i></li>
      <li><b>Convention 7:</b> Use TODO/FIXME/NOTE tags for tasks, bugs, or important notes.<br><i>Mark places in the code that need attention or improvement.</i></li>
    </ul>
  </div>
</div>
"""
            db.session.commit()
            print(f'Lesson {lesson_id} conventions layout updated.')
        else:
            print(f'Lesson {lesson_id} not found.')

def update_html_css_conventions_layout(lesson_id):
    app = create_app()
    with app.app_context():
        lesson = Lesson.query.get(lesson_id)
        if lesson:
            lesson.content = """
<h2>Section 3: HTML and CSS Comments - Best Practices</h2>
<p>Follow these conventions to write clear, effective comments in your HTML and CSS code:</p>
<style>
.comment-conventions-row { display: flex; gap: 2em; margin-bottom: 1em; }
.comment-conventions-col { flex: 1; min-width: 200px; }
.comment-conventions-col ul { padding-left: 1.2em; }
</style>
<div class="comment-conventions-row">
  <div class="comment-conventions-col">
    <h3>Conventions 1–5</h3>
    <ul>
      <li><b>Convention 1:</b> Use <code>&lt;!-- --&gt;</code> for HTML and <code>/* */</code> for CSS comments.<br><i>Use the correct syntax for each language to ensure comments are recognized.</i></li>
      <li><b>Convention 2:</b> Comment sections and complex structures.<br><i>Label major sections, closing tags, or tricky CSS rules for easier navigation.</i></li>
      <li><b>Convention 3:</b> Avoid leaving commented-out code in production.<br><i>Remove unused code to keep files clean and maintainable.</i></li>
      <li><b>Convention 4:</b> Keep comments up to date.<br><i>Update or remove comments that no longer apply after changes.</i></li>
      <li><b>Convention 5:</b> Use comments to clarify hacks or browser workarounds.<br><i>Explain why a workaround is needed for future maintainers.</i></li>
    </ul>
  </div>
  <div class="comment-conventions-col">
    <h3>Conventions 6–7</h3>
    <ul>
      <li><b>Convention 6:</b> Explain why, not just what.<br><i>Describe the reason for a structure, workaround, or style, not just what it does.</i></li>
      <li><b>Convention 7:</b> Use TODO/FIXME/NOTE tags for tasks, bugs, or important notes.<br><i>Mark places in the code that need attention or improvement.</i></li>
    </ul>
  </div>
</div>
"""
            db.session.commit()
            print(f'Lesson {lesson_id} conventions layout updated.')
        else:
            print(f'Lesson {lesson_id} not found.')

if __name__ == "__main__":
    update_conventions_layout(35)
    update_js_conventions_layout(36)
    update_html_css_conventions_layout(37)
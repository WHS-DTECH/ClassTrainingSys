# force_update_lesson27.py
from app import create_app, db
from app.models import Lesson

def update_lesson27():
    app = create_app()
    with app.app_context():
        lesson = Lesson.query.get(27)
        if lesson:
            lesson.content = '''
<h2>Test: Show Explanation Button</h2>
<p>This is a test block for lesson 27.</p>
<button class="btn btn-info btn-sm show-explanation" type="button" data-target="explanation-test" style="margin-left: 0.5em;">Show Explanation</button>
<div class="explanation-box" id="explanation-test" style="display:none; margin-top:0.5em; border:1px solid #17a2b8; background:#e9f7fa; padding:0.5em; border-radius:4px;">
    <strong>Explanation:</strong> This is a test explanation. If you see this, the update worked.
</div>
'''
            db.session.commit()
            print('Lesson 27 updated.')
        else:
            print('Lesson 27 not found.')

if __name__ == "__main__":
    update_lesson27()

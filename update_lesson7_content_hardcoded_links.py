# Script to update lesson 7 content with hardcoded section links for Module 3: Assessment and Checking

from app import create_app, db
from app.models import Lesson

app = create_app()

with app.app_context():
    lesson = Lesson.query.filter_by(id=7).first()
    if lesson:
        lesson.content = '''<h1>Module 3: Assessment Checking</h1>
<p>Module 3 covers advanced programming concepts and practices.</p>
<p><b>Instructor:</b> Vanessa Pringle</p>
<h2>Course Content</h2>
<ol>
  <li><a href="/lessons/sections/13">0. Checking Overview</a></li>
  <li><a href="/lessons/sections/14">1. Lesson 1: Comment Checker</a></li>
  <li><a href="/lessons/sections/15">2. Lesson 2: Debug Checker</a></li>
</ol>'''
        db.session.commit()
        print('Lesson 7 content updated with hardcoded section links.')
    else:
        print('Lesson 7 not found.')

# Script to update lesson 7 content with hardcoded section links for Module 3: Assessment and Checking

from app import create_app, db
from app.models import Lesson

app = create_app()

with app.app_context():
    lesson = Lesson.query.filter_by(id=7).first()
    if lesson:
        lesson.content = '''<h1>Module 3: Assessment and Checking</h1>
<p>This module covers techniques and strategies for checking student work for assessment purposes, including automated and manual review processes.</p>
<p><b>Instructor:</b> Vanessa Pringle (HOLA Technology)</p>
<h2>Course Content</h2>
<ol>
  <li><a href="/lessons/sections/13">Section 1: Python Assessment – Best Practices</a></li>
  <li><a href="/lessons/sections/14">Section 2: JavaScript Assessment – Best Practices</a></li>
  <li><a href="/lessons/sections/15">Section 3: HTML and CSS Assessment – Best Practices</a></li>
</ol>'''
        db.session.commit()
        print('Lesson 7 content updated with hardcoded section links.')
    else:
        print('Lesson 7 not found.')

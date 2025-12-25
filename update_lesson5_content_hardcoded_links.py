# Script to update lesson 5 content with hardcoded section links for Module 1: Commenting

from app import create_app, db
from app.models import Lesson

app = create_app()

with app.app_context():
    lesson = Lesson.query.filter_by(id=5).first()
    if lesson:
        lesson.content = '''<h1>Module 1: Commenting</h1>
<p>Learn best practices for writing effective comments in your code. This module covers general commenting principles and specific conventions for Python and JavaScript.</p>
<p><b>Instructor:</b> Vanessa Pringle (HOLA Technology)</p>
<h2>Course Content</h2>
<ol>
  <li><a href="/lessons/sections/5">Introduction to Code Comments</a></li>
  <li><a href="/lessons/sections/6">Section 1: Python Comments - Best Practices</a></li>
  <li><a href="/lessons/sections/7">Section 2: JavaScript Comments - Best Practices</a></li>
  <li><a href="/lessons/sections/8">Section 3: HTML and CSS Comments - Best Practices</a></li>
</ol>'''
        db.session.commit()
        print('Lesson 5 content updated with hardcoded section links.')
    else:
        print('Lesson 5 not found.')

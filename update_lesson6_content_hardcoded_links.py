# Script to update lesson 6 content with hardcoded section links for Module 2: Debugging

from app import create_app, db
from app.models import Lesson

app = create_app()

with app.app_context():
    lesson = Lesson.query.filter_by(id=6).first()
    if lesson:
        lesson.content = '''<h1>Module 2: Debugging</h1>
<p>Learn what debugging is, why it is a critical skill for programmers, and how to approach finding and fixing errors in your code. This module covers the debugging mindset, common techniques, and the importance of persistence and problem-solving.</p>
<p><b>Instructor:</b> Vanessa Pringle (HOLA Technology)</p>
<h2>Course Content</h2>
<ol>
  <li><a href="/lessons/sections/9">Section 1: Debugging Mindset</a></li>
  <li><a href="/lessons/sections/10">Section 2: Common Debugging Techniques</a></li>
  <li><a href="/lessons/sections/11">Section 3: Persistence and Problem-Solving</a></li>
  <li><a href="/lessons/sections/12">Section 4: Debugging in Practice</a></li>
</ol>'''
        db.session.commit()
        print('Lesson 6 content updated with hardcoded section links.')
    else:
        print('Lesson 6 not found.')

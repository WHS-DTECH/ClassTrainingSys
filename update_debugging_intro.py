# update_debugging_intro.py
"""
Update the debugging lesson's introduction/theory content to remove duplication and keep only the clean version.
"""
from app import create_app, db
from app.models import Lesson

def update_debugging_intro(lesson_id):
    app = create_app()
    with app.app_context():
        lesson = Lesson.query.get(lesson_id)
        if lesson:
            lesson.content = """
<p><strong>What is Code Debugging?</strong><br>
Code debugging is the process of identifying, isolating, and fixing errors or bugs in your code. It involves understanding how your program works, finding where things go wrong, and correcting mistakes to ensure your code runs as intended.</p>
<p><strong>Why does Debugging Matter?</strong><br>
Debugging is a critical skill for programmers because all code—no matter how experienced the developer—will have bugs at some point. Effective debugging helps you solve problems faster, learn from mistakes, and produce reliable, maintainable software. It also builds your problem-solving skills and persistence, which are essential for success in programming.</p>
<p><strong>The Golden Rule of Debugging</strong><br>
Don’t make more than one change at a time.<br>
When debugging, always change only one thing in your code or environment before testing again. If you change multiple things at once, you won’t know which change fixed (or broke) your code. This rule helps you isolate the cause of a bug and avoid introducing new problems.</p>
<ul>
    <li>Always reproduce the bug before trying to fix it.</li>
    <li>Understand the problem fully before making changes.</li>
    <li>Test after each change.</li>
</ul>
<p><strong>Bad Debug Example</strong></p>
<pre>
# Bad: Making multiple changes at once and not checking results
def add(a, b):
        return a - b  # Bug: should be a + b

# Developer changes both the function and unrelated code, then tests.
</pre>
<p><strong>Good Debug Example</strong></p>
<pre>
# Good: Change one thing, test, and document
def add(a, b):
        return a + b  # Fixed: changed '-' to '+'
# Test this change before making any others.
</pre>
<p><strong>When to Debug</strong></p>
<ul>
    <li>When your code produces errors or unexpected results.</li>
    <li>When a feature stops working after a change.</li>
    <li>When you need to understand unfamiliar code behavior.</li>
</ul>
<p><strong>When NOT to Debug</strong></p>
<ul>
    <li>When you haven’t reproduced the bug yet—always reproduce first.</li>
    <li>When you don’t understand the code—read and understand it first.</li>
    <li>When you’re guessing or making random changes—debug methodically.</li>
</ul>
"""
            db.session.commit()
            print(f'Lesson {lesson_id} content updated.')
        else:
            print(f'Lesson {lesson_id} not found.')

if __name__ == "__main__":
    update_debugging_intro(40)

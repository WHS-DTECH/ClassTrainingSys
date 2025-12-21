"""
Add Module 1: Commenting to the database
This module teaches students best practices for writing comments in Python and JavaScript
"""

from app import create_app, db
from app.models import User, Course, Lesson, Assignment, Quiz, QuizQuestion, Enrollment
from datetime import datetime, timedelta

def add_commenting_module():
    app = create_app()
    
    with app.app_context():
        # Get the teacher account
        teacher = User.query.filter_by(username='teacher').first()
        if not teacher:
            print("Error: Teacher account not found. Please run init_db.py first.")
            return
        
        # Create or update Module 1: Commenting
        print("Creating Module 1: Commenting...")
        module1 = Course.query.filter_by(title='Module 1: Commenting', teacher_id=teacher.id).first()
        if not module1:
            module1 = Course(
                title='Module 1: Commenting',
                description='Learn best practices for writing effective comments in your code. This module covers general commenting principles and specific conventions for Python and JavaScript.',
                teacher_id=teacher.id
            )
            db.session.add(module1)
            db.session.commit()
        else:
            # Delete all existing lessons for this module (robust)
            lessons_to_delete = Lesson.query.filter_by(course_id=module1.id).all()
            for lesson in lessons_to_delete:
                db.session.delete(lesson)
            db.session.commit()

        # Lesson 1: Introduction to Code Comments
        lesson1 = Lesson(
            course_id=module1.id,
            title='Introduction to Code Comments',
            content='''
<h2>What Are Code Comments?</h2>
<p>Code comments are human-readable explanations or annotations in your source code. They are ignored by compilers and interpreters, serving only to help developers understand the code.</p>

<h3>Why Comments Matter</h3>
<ul>
    <li><strong>Code Documentation:</strong> Explain what your code does and why</li>
    <li><strong>Future Reference:</strong> Help your future self understand your reasoning</li>
    <li><strong>Team Collaboration:</strong> Help other developers work with your code</li>
    <li><strong>Debugging:</strong> Temporarily disable code without deleting it</li>
    <li><strong>Learning Tool:</strong> Document your learning process</li>
</ul>

<h3>The Golden Rule of Comments</h3>
<p><strong>Comments should explain WHY, not WHAT.</strong></p>
<p>Good code should be self-explanatory about what it does. Comments should explain the reasoning, context, or non-obvious decisions.</p>

<h3>Bad Comment Example:</h3>
<pre>
# Add 1 to counter
counter = counter + 1
</pre>
<p>This comment just repeats what the code obviously does.</p>

<h3>Good Comment Example:</h3>
<pre>
# Increment counter to skip the header row
counter = counter + 1
</pre>
<p>This explains WHY we're incrementing, providing valuable context.</p>

<h3>When to Comment</h3>
<ul>
    <li>Complex algorithms or logic</li>
    <li>Non-obvious solutions or workarounds</li>
    <li>Important business rules or requirements</li>
    <li>Temporary code or TODOs</li>
    <li>Function and class documentation</li>
</ul>

<h3>When NOT to Comment</h3>
<ul>
    <li>Obvious code that speaks for itself</li>
    <li>Instead of fixing bad code (refactor instead)</li>
    <li>Outdated information (update or remove)</li>
    <li>Excessive comments that clutter the code</li>
</ul>

<p><strong>Remember:</strong> Good code with clear variable names and structure needs fewer comments!</p>

<hr style="margin: 3rem 0;">

<h2>🎯 Practice Activities</h2>
<p><strong>Instructions:</strong> Click on the line numbers where you think a comment is needed. You'll get immediate feedback!</p>

<div class="activity-container">
    <h3>Activity 1: Simple Calculation</h3>
    <p>Which lines need comments? (Click the line numbers)</p>
    <div class="code-activity" data-activity="1">
        <div class="code-line" data-line="1" data-needs-comment="false">
            <span class="line-number">1</span>
            <span class="code-content">def calculate_price(quantity, unit_price):</span>
        </div>
        <div class="code-line" data-line="2" data-needs-comment="false">
            <span class="line-number">2</span>
            <span class="code-content">&nbsp;&nbsp;&nbsp;&nbsp;subtotal = quantity * unit_price</span>
        </div>
        <div class="code-line" data-line="3" data-needs-comment="true" data-explanation="This line needs a comment to explain WHY we're applying a 20% discount (business rule). The calculation itself is obvious, but the reason isn't.">
            <span class="line-number">3</span>
            <span class="code-content">&nbsp;&nbsp;&nbsp;&nbsp;discount = subtotal * 0.20</span>
        </div>
        <div class="code-line" data-line="4" data-needs-comment="false">
            <span class="line-number">4</span>
            <span class="code-content">&nbsp;&nbsp;&nbsp;&nbsp;return subtotal - discount</span>
        </div>
    </div>
    <div class="activity-feedback" id="feedback-1"></div>
    <button class="btn btn-secondary btn-sm reset-activity" data-activity="1">Reset Activity</button>
</div>

<div class="activity-container">
    <h3>Activity 2: Data Processing</h3>
    <p>Which lines need comments? (Click the line numbers)</p>
    <div class="code-activity" data-activity="2">
        <div class="code-line" data-line="1" data-needs-comment="false">
            <span class="line-number">1</span>
            <span class="code-content">data = [45, 67, 23, 89, 12, 56]</span>
        </div>
        <div class="code-line" data-line="2" data-needs-comment="false">
            <span class="line-number">2</span>
            <span class="code-content">total = 0</span>
        </div>
        <div class="code-line" data-line="3" data-needs-comment="false">
            <span class="line-number">3</span>
            <span class="code-content">for value in data:</span>
        </div>
        <div class="code-line" data-line="4" data-needs-comment="true" data-explanation="This line needs a comment to explain WHY we're only adding values over 50 (what's the business logic or purpose?). The code shows WHAT we're doing, but not WHY.">
            <span class="line-number">4</span>
            <span class="code-content">&nbsp;&nbsp;&nbsp;&nbsp;if value > 50:</span>
        </div>
        <div class="code-line" data-line="5" data-needs-comment="false">
            <span class="line-number">5</span>
            <span class="code-content">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;total += value</span>
        </div>
        <div class="code-line" data-line="6" data-needs-comment="false">
            <span class="line-number">6</span>
            <span class="code-content">print(total)</span>
        </div>
    </div>
    <div class="activity-feedback" id="feedback-2"></div>
    <button class="btn btn-secondary btn-sm reset-activity" data-activity="2">Reset Activity</button>
</div>

<div class="activity-container">
    <h3>Activity 3: Complex Algorithm</h3>
    <p>Which lines need comments? (Click the line numbers)</p>
    <div class="code-activity" data-activity="3">
        <div class="code-line" data-line="1" data-needs-comment="false">
            <span class="line-number">1</span>
            <span class="code-content">def process_user_input(text):</span>
        </div>
        <div class="code-line" data-line="2" data-needs-comment="false">
            <span class="line-number">2</span>
            <span class="code-content">&nbsp;&nbsp;&nbsp;&nbsp;cleaned = text.strip().lower()</span>
        </div>
        <div class="code-line" data-line="3" data-needs-comment="true" data-explanation="This line needs a comment because using slice notation with step -1 to reverse a string is a Python-specific idiom that may not be immediately clear to all developers. Explaining WHY we're reversing it would also be helpful.">
            <span class="line-number">3</span>
            <span class="code-content">&nbsp;&nbsp;&nbsp;&nbsp;reversed_text = cleaned[::-1]</span>
        </div>
        <div class="code-line" data-line="4" data-needs-comment="true" data-explanation="This line needs a comment to explain WHY we're checking if the text equals its reverse (palindrome check). The logic isn't immediately obvious without context.">
            <span class="line-number">4</span>
            <span class="code-content">&nbsp;&nbsp;&nbsp;&nbsp;if cleaned == reversed_text:</span>
        </div>
        <div class="code-line" data-line="5" data-needs-comment="false">
            <span class="line-number">5</span>
            <span class="code-content">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;return True</span>
        </div>
        <div class="code-line" data-line="6" data-needs-comment="false">
            <span class="line-number">6</span>
            <span class="code-content">&nbsp;&nbsp;&nbsp;&nbsp;return False</span>
        </div>
    </div>
    <div class="activity-feedback" id="feedback-3"></div>
    <button class="btn btn-secondary btn-sm reset-activity" data-activity="3">Reset Activity</button>
</div>

<div class="activity-container">
    <h3>Activity 4: API Call</h3>
    <p>Which lines need comments? (Click the line numbers)</p>
    <div class="code-activity" data-activity="4">
        <div class="code-line" data-line="1" data-needs-comment="false">
            <span class="line-number">1</span>
            <span class="code-content">def fetch_data(user_id):</span>
        </div>
        <div class="code-line" data-line="2" data-needs-comment="true" data-explanation="This line needs a comment to explain WHY we're adding a 2-second delay (rate limiting, avoiding API throttling, preventing server overload, etc.). The sleep function is clear, but the business reason isn't.">
            <span class="line-number">2</span>
            <span class="code-content">&nbsp;&nbsp;&nbsp;&nbsp;time.sleep(2)</span>
        </div>
        <div class="code-line" data-line="3" data-needs-comment="false">
            <span class="line-number">3</span>
            <span class="code-content">&nbsp;&nbsp;&nbsp;&nbsp;response = requests.get(f'/api/users/{user_id}')</span>
        </div>
        <div class="code-line" data-line="4" data-needs-comment="false">
            <span class="line-number">4</span>
            <span class="code-content">&nbsp;&nbsp;&nbsp;&nbsp;return response.json()</span>
        </div>
    </div>
    <div class="activity-feedback" id="feedback-4"></div>
    <button class="btn btn-secondary btn-sm reset-activity" data-activity="4">Reset Activity</button>
</div>

<style>
.activity-container {
    margin: 2rem 0;
    padding: 1.5rem;
    background: #f8f9fa;
    border-radius: 8px;
    border: 1px solid #dee2e6;
}

.code-activity {
    background: white;
    border: 1px solid #ccc;
    border-radius: 4px;
    margin: 1rem 0;
    font-family: 'Courier New', monospace;
    font-size: 14px;
}

.code-line {
    display: flex;
    padding: 4px 0;
    border-bottom: 1px solid #eee;
    cursor: pointer;
    transition: background-color 0.2s;
}

.code-line:hover {
    background-color: #f0f0f0;
}

.code-line.selected {
    background-color: #fff3cd;
}

.code-line.correct {
    background-color: #d4edda !important;
    border-left: 4px solid #28a745;
}

.code-line.incorrect {
    background-color: #f8d7da !important;
    border-left: 4px solid #dc3545;
}

.line-number {
    display: inline-block;
    width: 40px;
    text-align: center;
    background: #e9ecef;
    color: #666;
    user-select: none;
    border-right: 1px solid #ccc;
    font-weight: bold;
}

.code-content {
    padding-left: 10px;
    flex: 1;
}

.activity-feedback {
    margin-top: 1rem;
    padding: 1rem;
    border-radius: 4px;
    display: none;
}

.activity-feedback.show {
    display: block;
}

.activity-feedback.success {
    background-color: #d4edda;
    border: 1px solid #c3e6cb;
    color: #155724;
}

.activity-feedback.partial {
    background-color: #fff3cd;
    border: 1px solid #ffeaa7;
    color: #856404;
}

.activity-feedback.error {
    background-color: #f8d7da;
    border: 1px solid #f5c6cb;
    color: #721c24;
}

.reset-activity {
    margin-top: 1rem;
}

.explanation-box {
    margin-top: 0.5rem;
    padding: 0.75rem;
    background: white;
    border-left: 4px solid #007bff;
    font-size: 0.9rem;
}
</style>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const activities = document.querySelectorAll('.code-activity');
    
    activities.forEach(activity => {
        const activityNum = activity.dataset.activity;
        const lines = activity.querySelectorAll('.code-line');
        const feedback = document.getElementById('feedback-' + activityNum);
        let selectedLines = new Set();
        let checked = false;
        
        lines.forEach(line => {
            line.addEventListener('click', function() {
                if (checked) return; // Don't allow changes after checking
                
                const lineNum = this.dataset.line;
                
                if (selectedLines.has(lineNum)) {
                    selectedLines.delete(lineNum);
                    this.classList.remove('selected');
                } else {
                    selectedLines.add(lineNum);
                    this.classList.add('selected');
                }
                
                checkAnswers();
            });
        });
        
        function checkAnswers() {
            if (selectedLines.size === 0) {
                feedback.classList.remove('show');
                return;
            }
            
            checked = true;
            let correctCount = 0;
            let totalNeeded = 0;
            let feedbackHTML = '<h4>Results:</h4>';
            
            lines.forEach(line => {
                const lineNum = line.dataset.line;
                const needsComment = line.dataset.needsComment === 'true';
                const explanation = line.dataset.explanation || '';
                
                if (needsComment) totalNeeded++;
                
                if (selectedLines.has(lineNum)) {
                    if (needsComment) {
                        line.classList.add('correct');
                        line.classList.remove('incorrect', 'selected');
                        correctCount++;
                        feedbackHTML += '<div class="explanation-box"><strong>✓ Line ' + lineNum + ':</strong> Correct! ' + explanation + '</div>';
                    } else {
                        line.classList.add('incorrect');
                        line.classList.remove('correct', 'selected');
                        feedbackHTML += '<div class="explanation-box"><strong>✗ Line ' + lineNum + ':</strong> This line does NOT need a comment. The code is self-explanatory.</div>';
                    }
                } else if (needsComment) {
                    line.classList.add('incorrect');
                    feedbackHTML += '<div class="explanation-box"><strong>✗ Line ' + lineNum + ':</strong> You missed this one! ' + explanation + '</div>';
                }
            });
            
            feedback.innerHTML = feedbackHTML;
            feedback.classList.add('show');
            
            if (correctCount === totalNeeded && selectedLines.size === totalNeeded) {
                feedback.classList.add('success');
                feedback.classList.remove('partial', 'error');
                feedback.innerHTML = '<h4>🎉 Perfect!</h4>' + feedbackHTML;
            } else if (correctCount > 0) {
                feedback.classList.add('partial');
                feedback.classList.remove('success', 'error');
                feedback.innerHTML = '<h4>Partially Correct</h4><p>You identified ' + correctCount + ' out of ' + totalNeeded + ' lines correctly.</p>' + feedbackHTML;
            } else {
                feedback.classList.add('error');
                feedback.classList.remove('success', 'partial');
                feedback.innerHTML = '<h4>Try Again</h4>' + feedbackHTML;
            }
        }
        
        // Reset button
        const resetBtn = document.querySelector('.reset-activity[data-activity="' + activityNum + '"]');
        if (resetBtn) {
            resetBtn.addEventListener('click', function() {
                selectedLines.clear();
                checked = false;
                lines.forEach(line => {
                    line.classList.remove('selected', 'correct', 'incorrect');
                });
                feedback.classList.remove('show', 'success', 'partial', 'error');
                feedback.innerHTML = '';
            });
        }
    });
});
</script>

<p style="margin-top: 2rem;"><strong>Great job!</strong> Now you understand when comments are truly needed. Remember: comment the WHY, not the WHAT!</p>
            ''',
            order=1
        )
        db.session.add(lesson1)
        
        # Lesson 2: Python Comments - Best Practices
        lesson2 = Lesson(
            course_id=module1.id,
            title='Section 1: Python Comments - Best Practices',
            content='''
<h2>Python Commenting Conventions</h2>
<p>Python has specific conventions outlined in PEP 8, the official Python style guide.</p>

<h3>1. Single-Line Comments</h3>
<p>Use the hash symbol (#) for single-line comments.</p>
<pre>
# This is a single-line comment
x = 5  # You can also place comments at the end of a line
</pre>

<h3>2. Multi-Line Comments</h3>
<p>Python doesn't have dedicated multi-line comment syntax, but you can use multiple # symbols:</p>
<pre>
# This is a longer comment that spans
# multiple lines to explain something
# complex about the code below
</pre>

<h3>3. Docstrings (Documentation Strings)</h3>
<p>Use triple quotes for function, class, and module documentation:</p>
<pre>
def calculate_area(length, width):
    """
    Calculate the area of a rectangle.
    
    Args:
        length (float): The length of the rectangle
        width (float): The width of the rectangle
    
    Returns:
        float: The calculated area
    """
    return length * width
</pre>

<h3>4. PEP 8 Commenting Guidelines</h3>
<ul>
    <li><strong>Inline comments:</strong> Use sparingly, separate by at least 2 spaces from code</li>
    <li><strong>Block comments:</strong> Each line starts with # and a single space</li>
    <li><strong>Maximum length:</strong> Keep comments to 72 characters per line</li>
    <li><strong>Update comments:</strong> When code changes, update the comments!</li>
</ul>

<h3>5. Python Comment Best Practices</h3>

<h4>✅ Good: Explain Complex Logic</h4>
<pre>
# Use binary search since the list is already sorted
# This reduces time complexity from O(n) to O(log n)
index = binary_search(sorted_list, target)
</pre>

<h4>✅ Good: Document Workarounds</h4>
<pre>
# TODO: This is a temporary fix for bug #1234
# Replace with proper validation once API is updated
if data is None:
    data = []
</pre>

<h4>✅ Good: Explain Business Logic</h4>
<pre>
# Apply 10% discount for orders over $100
# as per marketing policy dated 2025-01-15
if order_total > 100:
    discount = order_total * 0.10
</pre>

<h4>❌ Bad: Stating the Obvious</h4>
<pre>
# Set x to 10
x = 10

# Loop through items
for item in items:
    # Print item
    print(item)
</pre>

<h4>❌ Bad: Commenting Instead of Refactoring</h4>
<pre>
# This function is too complex and needs refactoring
def do_everything(a, b, c, d, e):
    # 100 lines of confusing code...
</pre>

<h3>6. Special Python Comments</h3>

<h4>Encoding Declaration (top of file):</h4>
<pre>
# -*- coding: utf-8 -*-
</pre>

<h4>Shebang (for executable scripts):</h4>
<pre>
#!/usr/bin/env python3
</pre>

<h4>Type Hints Comments (older Python):</h4>
<pre>
def greet(name):
    # type: (str) -> str
    return f"Hello, {name}"
</pre>

<h3>7. Python Docstring Formats</h3>

<h4>Google Style:</h4>
<pre>
def function(arg1, arg2):
    """
    Summary line.
    
    Extended description of function.
    
    Args:
        arg1: Description of arg1
        arg2: Description of arg2
    
    Returns:
        Description of return value
    """
</pre>

<h4>NumPy Style:</h4>
<pre>
def function(arg1, arg2):
    """
    Summary line.
    
    Extended description.
    
    Parameters
    ----------
    arg1 : type
        Description
    arg2 : type
        Description
    
    Returns
    -------
    type
        Description
    """
</pre>

<p><strong>Key Takeaway:</strong> Python comments should enhance code readability without cluttering it. Use docstrings for documentation and inline comments for explanations.</p>

<hr style="margin: 3rem 0;">

<h2>✍️ Practice: Write Your Own Comments</h2>
<p>Below are simple Python code snippets. Write appropriate comments following the best practices you just learned. Click "Check Comment" for feedback!</p>

<div class="write-comment-activity">
    <h3>Exercise 1: Explain Business Logic</h3>
    <pre class="code-example">
shipping_cost = 0
if order_total > 75:
    shipping_cost = 0
else:
    shipping_cost = 5.99
    </pre>
    <p>Write a comment to explain the business rule (hint: explain WHY the threshold is 75):</p>
    <textarea class="comment-input" id="py-comment-1" rows="2" placeholder="# Your comment here..."></textarea>
    <button class="btn btn-primary btn-sm check-comment" data-exercise="py-1">Check Comment</button>
    <button class="btn btn-info btn-sm show-explanation" type="button" data-target="explanation-py-1" style="margin-left: 0.5em;">Show Explanation</button>
    <div class="comment-feedback" id="feedback-py-1"></div>
    <div class="explanation-box" id="explanation-py-1" style="display:none; margin-top:0.5em; border:1px solid #17a2b8; background:#e9f7fa; padding:0.5em; border-radius:4px;">
        <strong>Explanation:</strong> The threshold of 75 is a business rule: orders over $75 get free shipping to encourage larger purchases. Your comment should explain this reason, not just what the code does.
    </div>
</div>

<div class="write-comment-activity">
    <h3>Exercise 2: Document a Workaround</h3>
    <pre class="code-example">
time.sleep(0.5)
response = api.get_data()
    </pre>
    <p>Write a comment to explain why there's a delay (hint: explain the reason, not what sleep does):</p>
    <textarea class="comment-input" id="py-comment-2" rows="2" placeholder="# Your comment here..."></textarea>
    <button class="btn btn-primary btn-sm check-comment" data-exercise="py-2">Check Comment</button>
    <button class="btn btn-info btn-sm show-explanation" type="button" data-target="explanation-py-2" style="margin-left: 0.5em;">Show Explanation</button>
    <div class="comment-feedback" id="feedback-py-2"></div>
    <div class="explanation-box" id="explanation-py-2" style="display:none; margin-top:0.5em; border:1px solid #17a2b8; background:#e9f7fa; padding:0.5em; border-radius:4px;">
        <strong>Explanation:</strong> The delay is used to avoid hitting API rate limits or to ensure the server has time to process requests. Your comment should explain the reason for the delay, not just describe the sleep function.
    </div>
</div>

<div class="write-comment-activity">
    <h3>Exercise 3: Avoid Obvious Comments</h3>
    <pre class="code-example">
total_price = quantity * unit_price
    </pre>
    <p>Does this code need a comment? If yes, write one. If no, type "NO COMMENT NEEDED":</p>
    <textarea class="comment-input" id="py-comment-3" rows="2" placeholder="# Your answer..."></textarea>
    <button class="btn btn-primary btn-sm check-comment" data-exercise="py-3">Check Comment</button>
    <button class="btn btn-info btn-sm show-explanation" type="button" data-target="explanation-py-3" style="margin-left: 0.5em;">Show Explanation</button>
    <div class="comment-feedback" id="feedback-py-3"></div>
    <div class="explanation-box" id="explanation-py-3" style="display:none; margin-top:0.5em; border:1px solid #17a2b8; background:#e9f7fa; padding:0.5em; border-radius:4px;">
        <strong>Explanation:</strong> This code is self-explanatory and does not need a comment. Comments should only be added when the code's purpose is not obvious.
    </div>
</div>

<style>
.write-comment-activity {
    margin: 2rem 0;
    padding: 1.5rem;
    background: #f8f9fa;
    border-radius: 8px;
    border: 1px solid #dee2e6;
}

.code-example {
    background: #2d2d2d;
    color: #f8f8f2;
    padding: 1rem;
    border-radius: 4px;
    margin: 1rem 0;
}

.comment-input {
    width: 100%;
    padding: 0.75rem;
    font-family: 'Courier New', monospace;
    border: 2px solid #dee2e6;
    border-radius: 4px;
    font-size: 14px;
    margin: 0.5rem 0;
}

.comment-input:focus {
    outline: none;
    border-color: #007bff;
}

.check-comment {
    margin-top: 0.5rem;
}

.comment-feedback {
    margin-top: 1rem;
    padding: 1rem;
    border-radius: 4px;
    display: none;
}

.comment-feedback.show {
    display: block;
}

.comment-feedback.success {
    background-color: #d4edda;
    border: 1px solid #c3e6cb;
    color: #155724;
}

.comment-feedback.warning {
    background-color: #fff3cd;
    border: 1px solid #ffeaa7;
    color: #856404;
}

.comment-feedback.error {
    background-color: #f8d7da;
    border: 1px solid #f5c6cb;
    color: #721c24;
}
</style>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const exercises = {
        'py-1': {
            check: function(comment) {
                comment = comment.toLowerCase().trim();
                
                // Check if it's just repeating the code
                if (comment.includes('set shipping') || comment.includes('if order') || 
                    (comment.includes('0') && comment.includes('75'))) {
                    return {
                        type: 'error',
                        message: '❌ Your comment describes WHAT the code does. Instead, explain WHY we have free shipping over $75 (e.g., marketing promotion, company policy, competitive advantage).'
                    };
                }
                
                // Check if it explains the WHY
                if (comment.includes('promo') || comment.includes('policy') || 
                    comment.includes('marketing') || comment.includes('encourage') ||
                    comment.includes('customer') || comment.includes('competitive') ||
                    comment.includes('free shipping')) {
                    return {
                        type: 'success',
                        message: '✅ Great! You explained WHY we have this rule, not just what it does. This provides valuable context for other developers.'
                    };
                }
                
                return {
                    type: 'warning',
                    message: '⚠️ Good attempt, but try to explain WHY the business offers free shipping over $75. What\'s the business reason or policy behind this threshold?'
                };
            }
        },
        'py-2': {
            check: function(comment) {
                comment = comment.toLowerCase().trim();
                
                // Check if just describing sleep
                if ((comment.includes('sleep') || comment.includes('wait') || comment.includes('delay')) && 
                    !comment.includes('api') && !comment.includes('rate') && !comment.includes('limit')) {
                    return {
                        type: 'error',
                        message: '❌ Your comment just restates that we\'re sleeping/waiting. Explain WHY we need the delay (e.g., API rate limiting, avoiding throttling, preventing errors).'
                    };
                }
                
                // Check for good explanation
                if (comment.includes('rate') || comment.includes('limit') || 
                    comment.includes('throttl') || comment.includes('avoid') ||
                    comment.includes('prevent') || comment.includes('api')) {
                    return {
                        type: 'success',
                        message: '✅ Perfect! You explained the reason for the delay, which helps others understand this isn\'t arbitrary but necessary for API compliance.'
                    };
                }
                
                return {
                    type: 'warning',
                    message: '⚠️ Try explaining WHY there\'s a delay. Is it for API rate limiting? Preventing server overload? Avoiding errors?'
                };
            }
        },
        'py-3': {
            check: function(comment) {
                comment = comment.toLowerCase().trim();
                
                // Check if they correctly identified no comment needed
                if (comment.includes('no comment') || comment.includes('not needed') ||
                    comment.includes('no need') || comment === 'no' || comment === 'none') {
                    return {
                        type: 'success',
                        message: '✅ Exactly right! This code is self-explanatory. The variable names clearly show we\'re calculating total price. Adding a comment like "# Calculate total price" would just be redundant.'
                    };
                }
                
                // If they wrote a comment
                if (comment.startsWith('#') || comment.length > 5) {
                    if (comment.includes('multiply') || comment.includes('calculate') || 
                        comment.includes('total') || comment.includes('price')) {
                        return {
                            type: 'error',
                            message: '❌ This comment is redundant! The code already clearly shows we\'re calculating total_price by multiplying quantity and unit_price. The variable names tell the story - no comment needed. Remember: don\'t comment the obvious!'
                        };
                    }
                }
                
                return {
                    type: 'warning',
                    message: '⚠️ Think about whether this simple calculation really needs a comment. The variable names are clear and the operation is obvious. Would a comment add value?'
                };
            }
        }
    };
    
    document.querySelectorAll('.check-comment').forEach(button => {
        button.addEventListener('click', function() {
            const exerciseId = this.dataset.exercise;
            const input = document.getElementById(exerciseId.replace('py-', 'py-comment-'));
            const feedback = document.getElementById('feedback-' + exerciseId);
            const comment = input.value.trim();
            
            if (!comment) {
                feedback.className = 'comment-feedback show error';
                feedback.innerHTML = '❌ Please write a comment first!';
                return;
            }
            
            const result = exercises[exerciseId].check(comment);
            feedback.className = 'comment-feedback show ' + result.type;
            feedback.innerHTML = result.message;
        });
    });
});
</script>
            ''',
            order=2
        )
        db.session.add(lesson2)
        
        # Lesson 3: JavaScript Comments - Best Practices
        lesson3 = Lesson(
            course_id=module1.id,
            title='Section 2: JavaScript Comments - Best Practices',
            content='''
<h2>JavaScript Commenting Conventions</h2>
<p>JavaScript supports two types of comments and has conventions popularized by JSDoc and various style guides.</p>

<h3>1. Single-Line Comments</h3>
<p>Use double slashes (//) for single-line comments:</p>
<pre>
// This is a single-line comment
let x = 5;  // You can also place comments at the end of a line
</pre>

<h3>2. Multi-Line Comments</h3>
<p>Use /* */ for comments spanning multiple lines:</p>
<pre>
/* 
 * This is a multi-line comment
 * that spans several lines
 * to explain complex logic
 */
</pre>

<h3>3. JSDoc Comments</h3>
<p>Use JSDoc format for documenting functions, classes, and modules:</p>
<pre>
/**
 * Calculate the area of a rectangle
 * @param {number} length - The length of the rectangle
 * @param {number} width - The width of the rectangle
 * @returns {number} The calculated area
 */
function calculateArea(length, width) {
    return length * width;
}
</pre>

<h3>4. JavaScript Comment Best Practices</h3>

<h4>✅ Good: Explain Intent and Context</h4>
<pre>
// Cache DOM query results to avoid repeated lookups
// Performance improvement for large documents
const mainNav = document.querySelector('.main-nav');
</pre>

<h4>✅ Good: Document API Usage</h4>
<pre>
/**
 * Fetch user data from the API
 * @async
 * @param {string} userId - The unique user identifier
 * @returns {Promise<Object>} User data object
 * @throws {Error} If the API request fails
 */
async function fetchUserData(userId) {
    const response = await fetch(`/api/users/${userId}`);
    if (!response.ok) {
        throw new Error('Failed to fetch user data');
    }
    return response.json();
}
</pre>

<h4>✅ Good: Explain Workarounds and Browser Quirks</h4>
<pre>
// Fix for Safari's date parsing issue
// Safari requires dates in ISO format (YYYY-MM-DD)
const date = new Date(dateString.replace(/\//g, '-'));
</pre>

<h4>✅ Good: Mark TODOs and FIXMEs</h4>
<pre>
// TODO: Add input validation
// FIXME: Handle edge case when array is empty
// HACK: Temporary solution until API v2 is ready
</pre>

<h4>❌ Bad: Commenting Out Dead Code</h4>
<pre>
function processData(data) {
    // let oldMethod = data.map(x => x * 2);
    // let anotherOldWay = data.filter(x => x > 0);
    // return oldMethod.concat(anotherOldWay);
    
    return data.map(x => x * 2).filter(x => x > 0);
}
// Use version control instead of commenting out old code!
</pre>

<h4>❌ Bad: Redundant Comments</h4>
<pre>
// Increment counter
counter++;

// Call function
doSomething();
</pre>

<h3>5. JSDoc Tags Reference</h3>
<pre>
/**
 * @param {type} name - Description
 * @returns {type} Description
 * @throws {Error} Description
 * @example
 * functionName(arg1, arg2);
 * @deprecated Use newFunction() instead
 * @see {@link OtherFunction}
 * @author Your Name
 * @version 1.0.0
 * @since 1.0.0
 * @todo Add feature X
 */
</pre>

<h3>6. Modern JavaScript Comment Patterns</h3>

<h4>ES6 Modules:</h4>
<pre>
/**
 * User authentication utilities
 * @module auth/utils
 */

/**
 * Validate user credentials
 * @function validateCredentials
 */
export function validateCredentials(username, password) {
    // Implementation
}
</pre>

<h4>Class Documentation:</h4>
<pre>
/**
 * Represents a user in the system
 * @class
 */
class User {
    /**
     * Create a user
     * @constructor
     * @param {string} name - The user's name
     * @param {string} email - The user's email
     */
    constructor(name, email) {
        this.name = name;
        this.email = email;
    }
    
    /**
     * Get user's display name
     * @returns {string} The formatted display name
     */
    getDisplayName() {
        return `${this.name} (${this.email})`;
    }
}
</pre>

<h4>Async/Await Documentation:</h4>
<pre>
/**
 * Save user data to database
 * @async
 * @param {Object} userData - User information to save
 * @returns {Promise<boolean>} True if save was successful
 */
async function saveUser(userData) {
    try {
        await database.insert(userData);
        return true;
    } catch (error) {
        console.error('Failed to save user:', error);
        return false;
    }
}
</pre>

<h3>7. Style Guide Recommendations</h3>

<h4>Airbnb Style Guide:</h4>
<ul>
    <li>Use // for single-line comments</li>
    <li>Place comments on a new line above the subject</li>
    <li>Start comments with a space for readability</li>
    <li>Prefix with FIXME or TODO for action items</li>
</ul>

<h4>Google JavaScript Style Guide:</h4>
<ul>
    <li>Use JSDoc for all functions, classes, and methods</li>
    <li>Document all parameters and return values</li>
    <li>Keep comments concise and meaningful</li>
    <li>Update comments when code changes</li>
</ul>

<h3>8. Special Comment Patterns</h3>

<h4>Copyright and License:</h4>
<pre>
/**
 * @license
 * Copyright (c) 2025 Your Company
 * Licensed under the MIT License
 */
</pre>

<h4>Configuration Comments:</h4>
<pre>
/* eslint-disable no-console */
console.log('Debug info');
/* eslint-enable no-console */
</pre>

<h4>Region Comments (for code folding):</h4>
<pre>
// #region Helper Functions
function helper1() { }
function helper2() { }
// #endregion
</pre>

<p><strong>Key Takeaway:</strong> JavaScript comments should document intent, explain complex logic, and provide context. Use JSDoc for professional API documentation.</p>

<hr style="margin: 3rem 0;">

<h2>✍️ Practice: Write Your Own Comments</h2>
<p>Below are simple JavaScript code snippets. Write appropriate comments following JSDoc and best practices. Click "Check Comment" for feedback!</p>

<div class="write-comment-activity">
    <h3>Exercise 1: Explain Browser Workaround</h3>
    <pre class="code-example">
const date = dateString.replace(/-/g, '/');
const parsed = new Date(date);
    </pre>
    <p>Write a comment to explain why we're replacing dashes (hint: browser compatibility issue):</p>
    <textarea class="comment-input" id="js-comment-1" rows="2" placeholder="// Your comment here..."></textarea>
    <button class="btn btn-primary btn-sm check-comment" data-exercise="js-1">Check Comment</button>
    <div class="comment-feedback" id="feedback-js-1"></div>
</div>

<div class="write-comment-activity">
    <h3>Exercise 2: Document Complex Logic</h3>
    <pre class="code-example">
const filtered = data.filter(item => item.score > 50)
                    .sort((a, b) => b.score - a.score)
                    .slice(0, 10);
    </pre>
    <p>Write a comment to explain what this achieves (hint: explain the business purpose, not the operations):</p>
    <textarea class="comment-input" id="js-comment-2" rows="2" placeholder="// Your comment here..."></textarea>
    <button class="btn btn-primary btn-sm check-comment" data-exercise="js-2">Check Comment</button>
    <div class="comment-feedback" id="feedback-js-2"></div>
</div>

<div class="write-comment-activity">
    <h3>Exercise 3: Write JSDoc for a Function</h3>
    <pre class="code-example">
function calculateDiscount(price, percentage) {
    return price * (percentage / 100);
}
    </pre>
    <p>Write a JSDoc comment for this function (include @param and @returns tags):</p>
    <textarea class="comment-input" id="js-comment-3" rows="6" placeholder="/**
 * Your JSDoc here
 */"></textarea>
    <button class="btn btn-primary btn-sm check-comment" data-exercise="js-3">Check Comment</button>
    <div class="comment-feedback" id="feedback-js-3"></div>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const jsExercises = {
        'js-1': {
            check: function(comment) {
                comment = comment.toLowerCase().trim();
                
                // Check if just describing what the code does
                if (comment.includes('replace') || comment.includes('dash') && !comment.includes('safari') && 
                    !comment.includes('browser') && !comment.includes('compatibility') && !comment.includes('ie')) {
                    return {
                        type: 'error',
                        message: '❌ Your comment describes WHAT the code does. Explain WHY we need to replace dashes - which browsers have issues? What problem does this solve?'
                    };
                }
                
                // Check for good explanation
                if (comment.includes('safari') || comment.includes('browser') || 
                    comment.includes('compatibility') || comment.includes('ie') ||
                    comment.includes('firefox') || comment.includes('parse') && comment.includes('issue')) {
                    return {
                        type: 'success',
                        message: '✅ Excellent! You explained the browser compatibility issue. This helps future developers understand why we have this seemingly odd code.'
                    };
                }
                
                return {
                    type: 'warning',
                    message: '⚠️ Try explaining WHY we need to replace dashes. Is it a browser compatibility issue? Which browsers? This context is valuable!'
                };
            }
        },
        'js-2': {
            check: function(comment) {
                comment = comment.toLowerCase().trim();
                
                // Check if just describing the operations
                if ((comment.includes('filter') || comment.includes('sort') || comment.includes('slice')) && 
                    !comment.includes('top') && !comment.includes('best') && !comment.includes('highest') && !comment.includes('leaderboard')) {
                    return {
                        type: 'error',
                        message: '❌ Your comment describes the technical operations. Instead, explain the business purpose: What are we trying to achieve? (e.g., "Get top 10 performers", "Show leaderboard")'
                    };
                }
                
                // Check for business purpose
                if (comment.includes('top') || comment.includes('best') || 
                    comment.includes('highest') || comment.includes('leaderboard') ||
                    comment.includes('rank') || comment.includes('perform')) {
                    return {
                        type: 'success',
                        message: '✅ Perfect! You explained the business purpose rather than the technical operations. This tells readers WHY this code exists.'
                    };
                }
                
                return {
                    type: 'warning',
                    message: '⚠️ Focus on the business purpose: What is this filtered, sorted, sliced data used for? (leaderboard? top performers? best results?)'
                };
            }
        },
        'js-3': {
            check: function(comment) {
                const original = comment.trim();
                comment = comment.toLowerCase();
                
                // Check if it's JSDoc format
                if (!comment.includes('/**') && !comment.includes('*')) {
                    return {
                        type: 'error',
                        message: '❌ This should be a JSDoc comment starting with /** and ending with */. Use proper JSDoc format!'
                    };
                }
                
                // Check for required tags
                const hasParam = comment.includes('@param');
                const hasReturns = comment.includes('@return');
                const hasDescription = comment.split('\\n').length > 2;
                
                if (!hasParam) {
                    return {
                        type: 'error',
                        message: '❌ Missing @param tags! You need to document both parameters: price and percentage.'
                    };
                }
                
                if (!hasReturns) {
                    return {
                        type: 'warning',
                        message: '⚠️ Good start, but you\'re missing the @returns tag to document what the function returns.'
                    };
                }
                
                if (hasParam && hasReturns && hasDescription) {
                    return {
                        type: 'success',
                        message: '✅ Great JSDoc! You included a description, @param tags for the parameters, and @returns. This is exactly what professional documentation looks like!'
                    };
                }
                
                return {
                    type: 'warning',
                    message: '⚠️ You\'re on the right track! Make sure you have: 1) A description, 2) @param for each parameter, and 3) @returns for the return value.'
                };
            }
        }
    };
    
    document.querySelectorAll('.check-comment').forEach(button => {
        button.addEventListener('click', function() {
            const exerciseId = this.dataset.exercise;
            const input = document.getElementById(exerciseId.replace('js-', 'js-comment-'));
            const feedback = document.getElementById('feedback-' + exerciseId);
            const comment = input.value.trim();
            
            if (!comment) {
                feedback.className = 'comment-feedback show error';
                feedback.innerHTML = '❌ Please write a comment first!';
                return;
            }
            
            const result = jsExercises[exerciseId].check(comment);
            feedback.className = 'comment-feedback show ' + result.type;
            feedback.innerHTML = result.message;
        });
    });
});
</script>
            ''',
            order=3
        )
        db.session.add(lesson3)

        # Lesson 4: HTML and CSS Comments - Best Practices
        lesson4 = Lesson(
            course_id=module1.id,
            title='Section 3: HTML and CSS Comments - Best Practices',
            content='''
<h2>HTML and CSS Commenting Conventions</h2>
<p>HTML and CSS have their own ways to add comments, which are important for explaining structure, intent, and temporary code changes in web development.</p>

<h3>1. HTML Comments</h3>
<p>Use <code>&lt;!-- ... --&gt;</code> to add comments in HTML:</p>
<pre>
<!-- This is a comment in HTML -->
<div class="container">
    <!-- Main content starts here -->
    <h1>Welcome!</h1>
</div>
</pre>
<ul>
    <li>HTML comments do <strong>not</strong> appear on the page, but are visible in the source code.</li>
    <li>Use comments to explain sections, mark TODOs, or temporarily disable code.</li>
    <li>Avoid leaving large blocks of commented-out code in production.</li>
</ul>

<h3>2. CSS Comments</h3>
<p>Use <code>/* ... */</code> for comments in CSS:</p>
<pre>
/* This is a CSS comment */
.main-header {
    color: #333; /* Set text color */
    /* background: #eee;  // This line is commented out */
}
</pre>
<ul>
    <li>CSS comments can be placed anywhere outside selectors or inside rule blocks.</li>
    <li>Use comments to explain complex selectors, overrides, or design decisions.</li>
    <li>Remove unnecessary comments before deploying to production for cleaner code.</li>
</ul>

<h3>3. HTML &amp; CSS Comment Best Practices</h3>
<ul>
    <li>Explain <strong>why</strong> a structure or style is used, not just what it does.</li>
    <li>Use comments to help future developers (or yourself) understand the layout and styling choices.</li>
    <li>Keep comments up to date as the code changes.</li>
</ul>

<h4><strong>Good:</strong> Explain Structure and Intent</h4>
<pre>
<!-- Navigation bar for main site sections -->
<nav>
    ...
</nav>
</pre>
<pre>
/* Responsive design for mobile */
&#64;media (max-width: 600px) {
    .sidebar {
        display: none; /* Hide sidebar on small screens */
    }
}
</pre>

<h4><strong>Bad:</strong> Obvious or Outdated Comments</h4>
<pre>
<!-- This is a div -->
<div></div>
</pre>
<pre>
/* Change color */
color: red;
</pre>

<p><strong>Key Takeaway:</strong> Use HTML and CSS comments to clarify structure, intent, and design choices. Avoid cluttering your code with unnecessary or outdated comments.</p>

<p>Below are simple HTML and CSS code snippets. Write appropriate comments following the best practices you just learned. Click "Check Comment" for feedback!</p>
''',
            order=3
        )
        db.session.add(lesson4)
        db.session.add(lesson4)

        # Lesson 4: HTML and CSS Comments - Best Practices
        lesson4 = Lesson(
            course_id=module1.id,
            title='Section 3: HTML and CSS Comments - Best Practices',
            content='''
<h2>HTML and CSS Commenting Conventions</h2>
<p>HTML and CSS have their own ways to add comments, which are important for explaining structure, intent, and temporary code changes in web development.</p>

<h3>1. HTML Comments</h3>
<p>Use <code>&lt;!-- ... --&gt;</code> to add comments in HTML:</p>
<pre>
<!-- This is a comment in HTML -->
<div class="container">
    <!-- Main content starts here -->
    <h1>Welcome!</h1>
</div>
</pre>
<ul>
    <li>HTML comments do <strong>not</strong> appear on the page, but are visible in the source code.</li>
    <li>Use comments to explain sections, mark TODOs, or temporarily disable code.</li>
    <li>Avoid leaving large blocks of commented-out code in production.</li>
</ul>

<h3>2. CSS Comments</h3>
<p>Use <code>/* ... */</code> for comments in CSS:</p>
<pre>
/* This is a CSS comment */
.main-header {
    color: #333; /* Set text color */
    /* background: #eee;  // This line is commented out */
}
</pre>
<ul>
    <li>CSS comments can be placed anywhere outside selectors or inside rule blocks.</li>
    <li>Use comments to explain complex selectors, overrides, or design decisions.</li>
    <li>Remove unnecessary comments before deploying to production for cleaner code.</li>
</ul>

<h3>3. HTML &amp; CSS Comment Best Practices</h3>
<ul>
    <li>Explain <strong>why</strong> a structure or style is used, not just what it does.</li>
    <li>Use comments to help future developers (or yourself) understand the layout and styling choices.</li>
    <li>Keep comments up to date as the code changes.</li>
</ul>

<h4><strong>Good:</strong> Explain Structure and Intent</h4>
<pre>
<!-- Navigation bar for main site sections -->
<nav>
    ...
</nav>
</pre>
<pre>
/* Responsive design for mobile */
&#64;media (max-width: 600px) {
    .sidebar {
        display: none; /* Hide sidebar on small screens */
    }
}
</pre>

<h4><strong>Bad:</strong> Obvious or Outdated Comments</h4>
<pre>
<!-- This is a div -->
<div></div>
</pre>
<pre>
/* Change color */
color: red;
</pre>

<p><strong>Key Takeaway:</strong> Use HTML and CSS comments to clarify structure, intent, and design choices. Avoid cluttering your code with unnecessary or outdated comments.</p>

<p>Below are simple HTML and CSS code snippets. Write appropriate comments following the best practices you just learned. Click "Check Comment" for feedback!</p>
''',
            order=3
        )
        db.session.add(lesson4)


        # Lesson 5: Best Practices Summary
        lesson5 = Lesson(
            course_id=module1.id,
            title='Commenting Best Practices - Summary',
            content='''
<h2>Universal Commenting Best Practices</h2>
<p>These principles apply to both Python and JavaScript (and most programming languages):</p>

<h3>1. The Comment Hierarchy</h3>
<ol>
    <li><strong>Best:</strong> Write self-documenting code that needs no comments</li>
    <li><strong>Good:</strong> Write clear code with minimal, meaningful comments</li>
    <li><strong>Acceptable:</strong> Write comments to explain complex sections</li>
    <li><strong>Bad:</strong> Write excessive comments explaining obvious code</li>
    <li><strong>Worst:</strong> Write misleading or outdated comments</li>
</ol>

<h3>2. Self-Documenting Code</h3>

<h4>Instead of commenting, use descriptive names:</h4>
<pre>
// Bad
let d = 10;  // days until deadline

// Good
let daysUntilDeadline = 10;
</pre>

<h4>Extract complex logic into well-named functions:</h4>
<pre>
// Bad
// Check if user has admin privileges
if (user.role === 'admin' || user.permissions.includes('admin_access')) {
    // ...
}

// Good
if (userHasAdminPrivileges(user)) {
    // ...
}
</pre>

<h3>3. When Comments Are Essential</h3>

<h4>✅ Complex Algorithms:</h4>
<pre>
// Using the Sieve of Eratosthenes algorithm
// More efficient than trial division for finding multiple primes
function findPrimes(limit) {
    // Implementation
}
</pre>

<h4>✅ Business Rules:</h4>
<pre>
# Per company policy effective Q4 2025:
# Free shipping for orders over $50
if order_total >= 50:
    shipping_cost = 0
</pre>

<h4>✅ API Documentation:</h4>
<pre>
/**
 * Process payment through third-party gateway
 * @requires Valid API credentials in environment
 * @ratelimit 100 requests per minute
 */
</pre>

<h4>✅ Warnings and Gotchas:</h4>
<pre>
// WARNING: Do not call this method more than once
// It has side effects that modify global state
function initializeSystem() {
    // ...
}
</pre>

<h3>4. Comment Maintenance</h3>

<h4>Keep Comments Fresh:</h4>
<ul>
    <li>Update comments when you change code</li>
    <li>Delete comments for removed code</li>
    <li>Review comments during code reviews</li>
    <li>Remove commented-out code (use version control instead)</li>
</ul>

<h4>The Danger of Outdated Comments:</h4>
<pre>
// Bad: Outdated comment
// Returns the user's age
function getUserData() {
    return user.name;  // Code changed but comment didn't!
}
</pre>

<h3>5. Comment Style Checklist</h3>

<h4>Python:</h4>
<ul>
    <li>☐ Use # for inline comments</li>
    <li>☐ Use triple quotes for docstrings</li>
    <li>☐ Follow PEP 8 (72 char limit, proper spacing)</li>
    <li>☐ Document all public functions and classes</li>
    <li>☐ Include type hints when helpful</li>
</ul>

<h4>JavaScript:</h4>
<ul>
    <li>☐ Use // for single-line comments</li>
    <li>☐ Use /* */ for multi-line comments</li>
    <li>☐ Use JSDoc for function/class documentation</li>
    <li>☐ Include @param and @returns tags</li>
    <li>☐ Document async functions and promises</li>
</ul>

<h3>6. Special Comment Tags</h3>
<table border="1" cellpadding="10">
    <tr>
        <th>Tag</th>
        <th>Purpose</th>
        <th>Example</th>
    </tr>
    <tr>
        <td>TODO</td>
        <td>Feature to be added</td>
        <td>// TODO: Add error handling</td>
    </tr>
    <tr>
        <td>FIXME</td>
        <td>Known bug to fix</td>
        <td>// FIXME: Handles null incorrectly</td>
    </tr>
    <tr>
        <td>HACK</td>
        <td>Temporary workaround</td>
        <td>// HACK: Quick fix for demo</td>
    </tr>
    <tr>
        <td>NOTE</td>
        <td>Important information</td>
        <td>// NOTE: Must run after initialization</td>
    </tr>
    <tr>
        <td>OPTIMIZE</td>
        <td>Performance improvement needed</td>
        <td>// OPTIMIZE: Use caching here</td>
    </tr>
</table>

<h3>7. Final Tips</h3>

<blockquote>
<p><strong>"Code tells you how, comments tell you why."</strong></p>
<p>- Jeff Atwood, Co-founder of Stack Overflow</p>
</blockquote>

<ul>
    <li><strong>Quality over quantity:</strong> One good comment beats ten useless ones</li>
    <li><strong>Think of your audience:</strong> Write for developers (including yourself in 6 months)</li>
    <li><strong>Be concise:</strong> Get to the point quickly</li>
    <li><strong>Be professional:</strong> Avoid jokes in production code</li>
    <li><strong>Be honest:</strong> Admit TODOs and known issues</li>
</ul>

<h3>Quiz Yourself:</h3>
<p>Before moving on, ask yourself:</p>
<ul>
    <li>Can I explain the difference between good and bad comments?</li>
    <li>Do I know when to use comments vs. refactoring code?</li>
    <li>Can I write proper docstrings/JSDoc?</li>
    <li>Do I understand Python PEP 8 commenting guidelines?</li>
    <li>Do I know JavaScript comment syntax and JSDoc tags?</li>
</ul>

<p><strong>Remember:</strong> Great code needs few comments. Great comments make good code excellent!</p>
            ''',
            order=99
        )
        db.session.add(lesson5)
        db.session.commit()
        # Debug: print all lessons for this module
        lessons = Lesson.query.filter_by(course_id=module1.id).order_by(Lesson.order).all()
        print(f"Lessons in DB for this module: {len(lessons)}")
        for idx, lesson in enumerate(lessons, 1):
            print(f"  {idx}. {lesson.title} (order={lesson.order})")
        
        # Create an assignment
        print("Creating assignment...")
        assignment = Assignment(
            course_id=module1.id,
            title='Comment Refactoring Exercise',
            description=r'''
<h3>Assignment: Improve Code Comments</h3>

<p>Below is a piece of code with poor commenting practices. Your task is to:</p>
<ol>
    <li>Remove unnecessary comments</li>
    <li>Add helpful comments where needed</li>
    <li>Write proper docstrings/JSDoc</li>
    <li>Follow language-specific conventions</li>
</ol>

<h4>Choose ONE language (Python OR JavaScript):</h4>

<h4>Python Version:</h4>
<pre>
# function
def calc(a,b,c):
    # add a and b
    x=a+b
    # multiply by c
    y=x*c
    # return result
    return y

# create list
nums=[1,2,3,4,5]
# loop
for n in nums:
    # print
    print(n*2)
</pre>

<h4>JavaScript Version:</h4>
<pre>
// function
function calc(a,b,c){
    // add a and b
    let x=a+b;
    // multiply by c
    let y=x*c;
    // return result
    return y;
}

// create array
const nums=[1,2,3,4,5];
// loop
for(let n of nums){
    // print
    console.log(n*2);
}
</pre>

<h4>Submission Requirements:</h4>
<ul>
    <li>Choose either Python or JavaScript</li>
    <li>Rewrite the code with improved commenting</li>
    <li>Use proper docstrings (Python) or JSDoc (JavaScript)</li>
    <li>Add meaningful comments only where necessary</li>
    <li>Use descriptive variable names to reduce need for comments</li>
    <li>Explain your reasoning for the changes you made</li>
</ul>
            ''',
            due_date=datetime.utcnow() + timedelta(days=7),
            max_points=100
        )
        db.session.add(assignment)
        db.session.commit()
        
        # Create a quiz
        print("Creating quiz...")
        quiz = Quiz(
            course_id=module1.id,
            title='Commenting Best Practices Quiz',
            description='Test your knowledge of commenting conventions in Python and JavaScript',
            time_limit=20,
            max_attempts=3
        )
        db.session.add(quiz)
        db.session.commit()
        
        # Add quiz questions
        questions = [
            {
                'question_text': 'What is the primary purpose of code comments?',
                'question_type': 'multiple_choice',
                'options': 'To make the code run faster\nTo explain WHY the code exists, not WHAT it does\nTo replace variable names\nTo increase file size',
                'correct_answer': 'To explain WHY the code exists, not WHAT it does',
                'points': 10,
                'order': 1
            },
            {
                'question_text': 'In Python, what symbol is used for single-line comments?',
                'question_type': 'short_answer',
                'correct_answer': '#',
                'points': 10,
                'order': 2
            },
            {
                'question_text': 'In JavaScript, what syntax is used for multi-line comments?',
                'question_type': 'multiple_choice',
                'options': '// comment //\n# comment #\n/* comment */\n<!-- comment -->',
                'correct_answer': '/* comment */',
                'points': 10,
                'order': 3
            },
            {
                'question_text': 'Python docstrings use triple quotes.',
                'question_type': 'true_false',
                'options': 'True\nFalse',
                'correct_answer': 'True',
                'points': 10,
                'order': 4
            },
            {
                'question_text': 'Which of the following is a BAD commenting practice?',
                'question_type': 'multiple_choice',
                'options': 'Explaining complex algorithms\nCommenting obvious code like "x = 5  # set x to 5"\nDocumenting API functions\nExplaining business rules',
                'correct_answer': 'Commenting obvious code like "x = 5  # set x to 5"',
                'points': 10,
                'order': 5
            },
            {
                'question_text': 'What tag is commonly used to mark code that needs to be fixed?',
                'question_type': 'short_answer',
                'correct_answer': 'FIXME',
                'points': 10,
                'order': 6
            },
            {
                'question_text': 'In JSDoc, which tag is used to document function parameters?',
                'question_type': 'multiple_choice',
                'options': '@parameter\n@param\n@arg\n@input',
                'correct_answer': '@param',
                'points': 10,
                'order': 7
            },
            {
                'question_text': 'Self-documenting code with clear variable names is better than excessive comments.',
                'question_type': 'true_false',
                'options': 'True\nFalse',
                'correct_answer': 'True',
                'points': 10,
                'order': 8
            }
        ]
        
        for q_data in questions:
            question = QuizQuestion(
                quiz_id=quiz.id,
                **q_data
            )
            db.session.add(question)
        
        db.session.commit()
        
        # Auto-enroll all students in this module
        print("Auto-enrolling students in Module 1...")
        students = User.query.filter_by(role='student').all()
        for student in students:
            # Check if already enrolled
            existing = Enrollment.query.filter_by(
                student_id=student.id,
                course_id=module1.id
            ).first()
            
            if not existing:
                enrollment = Enrollment(student_id=student.id, course_id=module1.id)
                db.session.add(enrollment)
        
        db.session.commit()
        print(f"Enrolled {len(students)} students in Module 1")
        
        print("\n" + "="*60)
        print("Module 1: Commenting has been created successfully!")
        print("="*60)
        print(f"\nModule ID: {module1.id}")
        print(f"Lessons created: 4")
        print(f"  1. Introduction to Code Comments")
        print(f"  2. Section 1: Python Comments - Best Practices")
        print(f"  3. Section 2: JavaScript Comments - Best Practices")
        print(f"  4. Commenting Best Practices - Summary")
        print(f"\nAssignment: Comment Refactoring Exercise")
        print(f"Quiz: {len(questions)} questions")
        print("\nLog in as a teacher to view the module,")
        print("or enroll as a student to work through the lessons!")
        print("="*60)

if __name__ == '__main__':
    add_commenting_module()

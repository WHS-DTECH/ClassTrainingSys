# update_lessons_with_explanations_fixed.py
from app import create_app, db
from app.models import Lesson

def update_lessons():
    app = create_app()
    with app.app_context():
        # Update lesson 27 (Python)
        lesson27 = Lesson.query.get(27)
        if lesson27:
            lesson27.content = '''
<h2>✍️ Practice: Write Your Own Comments (Python)</h2>
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
'''
        # Update lesson 28 (JavaScript)
        lesson28 = Lesson.query.get(28)
        if lesson28:
            lesson28.content = '''
<h2>✍️ Practice: Write Your Own Comments (JavaScript)</h2>
<div class="write-comment-activity">
    <h3>Exercise 1: Document a Workaround</h3>
    <pre class="code-example">
setTimeout(() => fetchData(), 500);
    </pre>
    <p>Write a comment to explain why there's a delay (hint: explain the reason, not what setTimeout does):</p>
    <textarea class="comment-input" id="js-comment-1" rows="2" placeholder="// Your comment here..."></textarea>
    <button class="btn btn-primary btn-sm check-comment" data-exercise="js-1">Check Comment</button>
    <button class="btn btn-info btn-sm show-explanation" type="button" data-target="explanation-js-1" style="margin-left: 0.5em;">Show Explanation</button>
    <div class="comment-feedback" id="feedback-js-1"></div>
    <div class="explanation-box" id="explanation-js-1" style="display:none; margin-top:0.5em; border:1px solid #17a2b8; background:#e9f7fa; padding:0.5em; border-radius:4px;">
        <strong>Explanation:</strong> The delay is used to avoid hitting API rate limits or to ensure the server has time to process requests. Your comment should explain the reason for the delay, not just describe setTimeout.
    </div>
</div>
'''
        db.session.commit()
        print('Updated lessons 27 and 28 with Show Explanation buttons.')

if __name__ == "__main__":
    update_lessons()

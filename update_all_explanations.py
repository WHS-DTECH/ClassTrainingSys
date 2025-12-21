# update_all_explanations.py
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
    <button class="btn btn-info btn-sm show-explanation" type="button" data-target="explanation-js-2" style="margin-left: 0.5em;">Show Explanation</button>
    <div class="comment-feedback" id="feedback-js-2"></div>
    <div class="explanation-box" id="explanation-js-2" style="display:none; margin-top:0.5em; border:1px solid #17a2b8; background:#e9f7fa; padding:0.5em; border-radius:4px;">
        <strong>Explanation:</strong> This code filters, sorts, and slices the data to get the top 10 items with a score above 50. The business purpose is to display the highest scoring items to the user.
    </div>
</div>
<div class="write-comment-activity">
    <h3>Exercise 3: Write JSDoc for a Function</h3>
    <pre class="code-example">
function calculateDiscount(price, percentage) {
    return price * (percentage / 100);
}
    </pre>
    <p>Write a JSDoc comment for this function (include @param and @returns tags):</p>
    <textarea class="comment-input" id="js-comment-3" rows="6" placeholder="/**\n * Your JSDoc here\n */"></textarea>
    <button class="btn btn-primary btn-sm check-comment" data-exercise="js-3">Check Comment</button>
    <button class="btn btn-info btn-sm show-explanation" type="button" data-target="explanation-js-3" style="margin-left: 0.5em;">Show Explanation</button>
    <div class="comment-feedback" id="feedback-js-3"></div>
    <div class="explanation-box" id="explanation-js-3" style="display:none; margin-top:0.5em; border:1px solid #17a2b8; background:#e9f7fa; padding:0.5em; border-radius:4px;">
        <strong>Explanation:</strong> Example JSDoc:
        <pre>/**
 * Calculates the discount amount.
 * @param {number} price - The original price
 * @param {number} percentage - The discount percentage
 * @returns {number} The discount amount
 */</pre>
    </div>
</div>
'''
        db.session.commit()
        print('Updated all exercises in lessons 27 and 28 with Show Explanation buttons.')

if __name__ == "__main__":
    update_lessons()

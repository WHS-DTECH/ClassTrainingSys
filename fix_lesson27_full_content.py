# fix_lesson27_full_content.py
from app import create_app, db
from app.models import Lesson

def update_lesson27():
    app = create_app()
    with app.app_context():
        lesson = Lesson.query.get(27)
        if lesson:
            lesson.content = '''
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
    <hr>
    <h2>Activity: Match Code to Purpose</h2>
    <p>Drag each code section to its correct purpose.</p>
    <div id="mix-match-container">
        <div class="mix-match-codes" style="float:left; width:48%;">
            <div class="mix-code" draggable="true" id="code1" style="border:1px solid #ccc; padding:0.5em; margin-bottom:0.5em; background:#f8f9fa;">for i in range(10): print(i)</div>
            <div class="mix-code" draggable="true" id="code2" style="border:1px solid #ccc; padding:0.5em; margin-bottom:0.5em; background:#f8f9fa;">if user_input == 'q': break</div>
            <div class="mix-code" draggable="true" id="code3" style="border:1px solid #ccc; padding:0.5em; margin-bottom:0.5em; background:#f8f9fa;">total = sum(prices)</div>
        </div>
        <div class="mix-match-targets" style="float:right; width:48%;">
            <div class="mix-target" id="target1" style="border:1px dashed #17a2b8; min-height:2em; margin-bottom:0.5em; padding:0.5em;">A. Add up all the prices in a list</div>
            <div class="mix-target" id="target2" style="border:1px dashed #17a2b8; min-height:2em; margin-bottom:0.5em; padding:0.5em;">B. Print numbers 0 to 9</div>
            <div class="mix-target" id="target3" style="border:1px dashed #17a2b8; min-height:2em; margin-bottom:0.5em; padding:0.5em;">C. Exit a loop if the user enters 'q'</div>
        </div>
        <div style="clear:both;"></div>
    </div>
    <p><button class="btn btn-primary btn-sm" onclick="checkMixMatch()">Check Answers</button></p>
    <div id="mix-match-feedback"></div>
    <script>
    let dragged;
    document.querySelectorAll('.mix-code').forEach(el => {
        el.addEventListener('dragstart', e => { dragged = el; });
    });
    document.querySelectorAll('.mix-target').forEach(target => {
        target.addEventListener('dragover', e => { e.preventDefault(); });
        target.addEventListener('drop', e => {
            e.preventDefault();
            if (dragged) target.innerHTML = dragged.outerHTML;
        });
    });
    function checkMixMatch() {
        let correct = 0;
        if (document.getElementById('target1').innerText.includes('total = sum(prices)')) correct++;
        if (document.getElementById('target2').innerText.includes('for i in range(10): print(i)')) correct++;
        if (document.getElementById('target3').innerText.includes("if user_input == 'q': break")) correct++;
        let feedback = document.getElementById('mix-match-feedback');
        if (correct === 3) feedback.innerHTML = '<span style="color:green;">All correct! 🎉</span>';
        else feedback.innerHTML = '<span style="color:red;">Some answers are incorrect. Try again!</span>';
    }
    </script>
    '''
            db.session.commit()
            print('Lesson 27 updated with all activities.')
        else:
            print('Lesson 27 not found.')

if __name__ == "__main__":
    update_lesson27()

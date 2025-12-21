# fix_lesson28_full_content.py
from app import create_app, db
from app.models import Lesson

def update_lesson28():
    app = create_app()
    with app.app_context():
        lesson = Lesson.query.get(28)
        if lesson:
            lesson.content = '''
<h2>✍️ Practice: Write Your Own Comments (JavaScript)</h2>
<div class="write-comment-activity">
    <h3>Exercise 1: Explain Business Logic</h3>
    <pre class="code-example">
let shippingCost = 0;
if (orderTotal > 75) {
    shippingCost = 0;
} else {
    shippingCost = 5.99;
}
    </pre>
    <p>Write a comment to explain the business rule (hint: explain WHY the threshold is 75):</p>
    <textarea class="comment-input" id="js-comment-1" rows="2" placeholder="// Your comment here..."></textarea>
    <button class="btn btn-primary btn-sm check-comment" data-exercise="js-1">Check Comment</button>
    <button class="btn btn-info btn-sm show-explanation" type="button" data-target="explanation-js-1" style="margin-left: 0.5em;">Show Explanation</button>
    <div class="comment-feedback" id="feedback-js-1"></div>
    <div class="explanation-box" id="explanation-js-1" style="display:none; margin-top:0.5em; border:1px solid #17a2b8; background:#e9f7fa; padding:0.5em; border-radius:4px;">
        <strong>Explanation:</strong> The threshold of 75 is a business rule: orders over $75 get free shipping to encourage larger purchases. Your comment should explain this reason, not just what the code does.
    </div>
</div>
<div class="write-comment-activity">
    <h3>Exercise 2: Document a Workaround</h3>
    <pre class="code-example">
setTimeout(function() {
    const response = api.getData();
}, 500);
    </pre>
    <p>Write a comment to explain why there's a delay (hint: explain the reason, not what setTimeout does):</p>
    <textarea class="comment-input" id="js-comment-2" rows="2" placeholder="// Your comment here..."></textarea>
    <button class="btn btn-primary btn-sm check-comment" data-exercise="js-2">Check Comment</button>
    <button class="btn btn-info btn-sm show-explanation" type="button" data-target="explanation-js-2" style="margin-left: 0.5em;">Show Explanation</button>
    <div class="comment-feedback" id="feedback-js-2"></div>
    <div class="explanation-box" id="explanation-js-2" style="display:none; margin-top:0.5em; border:1px solid #17a2b8; background:#e9f7fa; padding:0.5em; border-radius:4px;">
        <strong>Explanation:</strong> The delay is used to avoid hitting API rate limits or to ensure the server has time to process requests. Your comment should explain the reason for the delay, not just describe setTimeout.
    </div>
</div>
<div class="write-comment-activity">
    <h3>Exercise 3: Avoid Obvious Comments</h3>
    <pre class="code-example">
let totalPrice = quantity * unitPrice;
    </pre>
    <p>Does this code need a comment? If yes, write one. If no, type "NO COMMENT NEEDED":</p>
    <textarea class="comment-input" id="js-comment-3" rows="2" placeholder="// Your answer..."></textarea>
    <button class="btn btn-primary btn-sm check-comment" data-exercise="js-3">Check Comment</button>
    <button class="btn btn-info btn-sm show-explanation" type="button" data-target="explanation-js-3" style="margin-left: 0.5em;">Show Explanation</button>
    <div class="comment-feedback" id="feedback-js-3"></div>
    <div class="explanation-box" id="explanation-js-3" style="display:none; margin-top:0.5em; border:1px solid #17a2b8; background:#e9f7fa; padding:0.5em; border-radius:4px;">
        <strong>Explanation:</strong> This code is self-explanatory and does not need a comment. Comments should only be added when the code's purpose is not obvious.
    </div>
</div>
<hr>
<h2>Section 5: Assessment Requirements</h2>
<p><strong>92004 - Achieved</strong> - documenting the program with comments.<br>
<strong>Merit</strong> - documenting the program with comments that clarify the purpose of code sections.</p>

<!-- Mix and Match Activity -->
<h3>Activity: Match Code to Purpose</h3>
<p>Drag each code section to its correct purpose.</p>
<div id="mix-match-js-container">
    <div class="mix-match-codes" style="float:left; width:48%;">
        <div class="mix-code" draggable="true" id="js-code1" style="border:1px solid #ccc; padding:0.5em; margin-bottom:0.5em; background:#f8f9fa;">for (let i = 0; i &lt; 10; i++) &#123; console.log(i); &#125;</div>
        <div class="mix-code" draggable="true" id="js-code2" style="border:1px solid #ccc; padding:0.5em; margin-bottom:0.5em; background:#f8f9fa;">if (userInput === 'q') &#123; break; &#125;</div>
        <div class="mix-code" draggable="true" id="js-code3" style="border:1px solid #ccc; padding:0.5em; margin-bottom:0.5em; background:#f8f9fa;">let total = prices.reduce((a, b) =&gt; a + b, 0);</div>
    </div>
    <div class="mix-match-targets" style="float:right; width:48%;">
        <div class="mix-target" id="js-target1" style="border:1px dashed #17a2b8; min-height:2em; margin-bottom:0.5em; padding:0.5em;">A. Add up all the prices in an array</div>
        <div class="mix-target" id="js-target2" style="border:1px dashed #17a2b8; min-height:2em; margin-bottom:0.5em; padding:0.5em;">B. Print numbers 0 to 9</div>
        <div class="mix-target" id="js-target3" style="border:1px dashed #17a2b8; min-height:2em; margin-bottom:0.5em; padding:0.5em;">C. Exit a loop if the user enters 'q'</div>
    </div>
    <div style="clear:both;"></div>
</div>
<p><button class="btn btn-primary btn-sm" onclick="checkMixMatchJS()">Check Answers</button></p>
<div id="mix-match-js-feedback"></div>
<script>
let jsDragged;
document.querySelectorAll('#mix-match-js-container .mix-code').forEach(el => {
    el.addEventListener('dragstart', e => { jsDragged = el; });
});
document.querySelectorAll('#mix-match-js-container .mix-target').forEach(target => {
    target.addEventListener('dragover', e => { e.preventDefault(); });
    target.addEventListener('drop', e => {
        e.preventDefault();
        if (jsDragged) target.innerHTML = jsDragged.outerHTML;
    });
});
function checkMixMatchJS() {
    let correct = 0;
    if (document.getElementById('js-target1').innerText.includes('let total = prices.reduce')) correct++;
    if (document.getElementById('js-target2').innerText.includes('for (let i = 0; i < 10; i++)')) correct++;
    if (document.getElementById('js-target3').innerText.includes("if (userInput === 'q')")) correct++;
    let feedback = document.getElementById('mix-match-js-feedback');
    if (correct === 3) feedback.innerHTML = '<span style="color:green;">All correct! 🎉</span>';
    else feedback.innerHTML = '<span style="color:red;">Some answers are incorrect. Try again!</span>';
}
</script>
'''
            db.session.commit()
            print('Lesson 28 updated with all activities.')
        else:
            print('Lesson 28 not found.')

if __name__ == "__main__":
    update_lesson28()

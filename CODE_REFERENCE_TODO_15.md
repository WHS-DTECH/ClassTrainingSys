# Code Implementation Reference
## TODO #15 - Assignment Grading Interface with NZQA Standards

Quick reference for all code components implemented.

---

## 1. Database Models (app/models.py)

### AssignmentRubric Model
```python
class AssignmentRubric(db.Model):
    __tablename__ = 'assignment_rubric'
    
    id = db.Column(db.Integer, primary_key=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignment.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    total_points = db.Column(db.Integer, default=100)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    assignment = db.relationship('Assignment', backref='rubric')
    criteria = db.relationship('RubricCriterion', backref='rubric', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<AssignmentRubric {self.title} Assignment:{self.assignment_id}>'
```

### RubricCriterion Model
```python
class RubricCriterion(db.Model):
    __tablename__ = 'rubric_criterion'
    
    id = db.Column(db.Integer, primary_key=True)
    rubric_id = db.Column(db.Integer, db.ForeignKey('assignment_rubric.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    points = db.Column(db.Integer, nullable=False)
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<RubricCriterion {self.name} {self.points}pts>'
```

### GradeDetail Model
```python
class GradeDetail(db.Model):
    __tablename__ = 'grade_detail'
    
    id = db.Column(db.Integer, primary_key=True)
    submission_id = db.Column(db.Integer, db.ForeignKey('assignment_submission.id'), nullable=False)
    criterion_id = db.Column(db.Integer, db.ForeignKey('rubric_criterion.id'), nullable=False)
    points_awarded = db.Column(db.Integer)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    submission = db.relationship('AssignmentSubmission', lazy=True)
    criterion = db.relationship('RubricCriterion', lazy=True)
    
    def __repr__(self):
        return f'<GradeDetail Submission:{self.submission_id} Criterion:{self.criterion_id} Points:{self.points_awarded}>'
```

---

## 2. API Routes (app/routes/assignments.py)

### Grading Dashboard Route
```python
@bp.route('/<int:assignment_id>/grading', methods=['GET', 'POST'])
@login_required
def grading_dashboard(assignment_id):
    """Display all submissions for grading"""
    assignment = Assignment.query.get_or_404(assignment_id)
    
    # Permission check
    if not (current_user.is_teacher or current_user.id == assignment.teacher_id):
        abort(403)
    
    submissions = AssignmentSubmission.query.filter_by(
        assignment_id=assignment_id
    ).all()
    
    # Calculate stats
    total = len(submissions)
    graded = sum(1 for s in submissions if s.total_points is not None)
    pending = total - graded
    avg_score = sum(s.total_points for s in submissions if s.total_points) / graded if graded > 0 else 0
    
    return render_template('assignments/grading_dashboard.html',
                         assignment=assignment,
                         submissions=submissions,
                         stats={'total': total, 'graded': graded, 'pending': pending, 'average': avg_score})
```

### Grade Submission Route
```python
@bp.route('/<int:assignment_id>/submission/<int:submission_id>/grade', methods=['GET', 'POST'])
@login_required
def grade_submission_advanced(assignment_id, submission_id):
    """Grade individual submission with rubric"""
    assignment = Assignment.query.get_or_404(assignment_id)
    submission = AssignmentSubmission.query.get_or_404(submission_id)
    
    # Permission check
    if not (current_user.is_teacher or current_user.id == assignment.teacher_id):
        abort(403)
    
    rubric = AssignmentRubric.query.filter_by(assignment_id=assignment_id).first()
    
    if request.method == 'POST':
        total_points = 0
        
        # Process each criterion
        for criterion in rubric.criteria if rubric else []:
            points = request.form.get(f'criterion_{criterion.id}')
            notes = request.form.get(f'notes_{criterion.id}')
            
            if points:
                points = int(points)
                total_points += points
                
                # Save GradeDetail
                grade_detail = GradeDetail(
                    submission_id=submission_id,
                    criterion_id=criterion.id,
                    points_awarded=points,
                    notes=notes
                )
                db.session.add(grade_detail)
        
        # Update submission
        submission.total_points = total_points
        submission.feedback = request.form.get('overall_feedback')
        submission.graded = True
        
        db.session.commit()
        
        return redirect(url_for('assignments.grading_dashboard', assignment_id=assignment_id))
    
    return render_template('assignments/grade_submission.html',
                         assignment=assignment,
                         submission=submission,
                         rubric=rubric)
```

### Manage Rubric Route
```python
@bp.route('/<int:assignment_id>/rubric', methods=['GET', 'POST'])
@login_required
def manage_rubric(assignment_id):
    """Create or edit assignment rubric"""
    assignment = Assignment.query.get_or_404(assignment_id)
    
    # Permission check
    if not (current_user.is_teacher or current_user.id == assignment.teacher_id):
        abort(403)
    
    rubric = AssignmentRubric.query.filter_by(assignment_id=assignment_id).first()
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        total_points = int(request.form.get('total_points', 100))
        
        if not rubric:
            rubric = AssignmentRubric(
                assignment_id=assignment_id,
                title=title,
                description=description,
                total_points=total_points
            )
            db.session.add(rubric)
        else:
            rubric.title = title
            rubric.description = description
            rubric.total_points = total_points
        
        db.session.flush()
        
        # Process criteria
        for i in range(10):  # Support up to 10 criteria
            name = request.form.get(f'criterion_{i}_name')
            if name:
                criterion = RubricCriterion(
                    rubric_id=rubric.id,
                    name=name,
                    description=request.form.get(f'criterion_{i}_desc'),
                    points=int(request.form.get(f'criterion_{i}_points', 0)),
                    order=i
                )
                db.session.add(criterion)
        
        db.session.commit()
        
        return redirect(url_for('assignments.manage_rubric', assignment_id=assignment_id))
    
    return render_template('assignments/manage_rubric.html',
                         assignment=assignment,
                         rubric=rubric)
```

---

## 3. JavaScript Utilities (app/static/js/nzqa_rubrics.js)

### Create Rubric from Preset
```javascript
function createRubricFromPreset(presetKey) {
    const preset = NZQA_RUBRICS[presetKey];
    if (!preset) {
        console.error('Rubric preset not found:', presetKey);
        return null;
    }

    return {
        title: preset.title,
        description: preset.description,
        total_points: preset.total_points,
        criteria: preset.criteria.map((criterion, index) => ({
            name: criterion.name,
            description: criterion.description,
            points: criterion.points,
            order: index,
            levels: criterion.levels
        }))
    };
}
```

### Get Available Rubrics
```javascript
function getAvailableRubrics() {
    return Object.keys(NZQA_RUBRICS).map(key => ({
        key: key,
        title: NZQA_RUBRICS[key].title,
        description: NZQA_RUBRICS[key].description,
        total_points: NZQA_RUBRICS[key].total_points,
        criteria_count: NZQA_RUBRICS[key].criteria.length
    }));
}
```

### Get Performance Level Description
```javascript
function getPointLevelDescription(criterion, points) {
    if (!criterion.levels || !criterion.levels[points]) {
        return null;
    }
    return criterion.levels[points];
}
```

---

## 4. Sample NZQA Preset Structure

```javascript
const NZQA_RUBRICS = {
    programming_fundamentals: {
        title: "Programming Fundamentals (Year 9-10) - NZQA Standards",
        description: "Assessment aligned with NZQA Technology Curriculum Phase 4...",
        total_points: 100,
        criteria: [
            {
                name: "Design Thinking & Planning (NZQA)",
                description: "Student demonstrates ability to identify design requirements...",
                points: 20,
                levels: {
                    0: "No evidence of planning or design thinking",
                    5: "Minimal planning; problem requirements unclear or missing",
                    10: "Basic problem analysis; simple design plan with gaps",
                    15: "Clear problem identification; logical design with mostly complete documentation",
                    20: "Comprehensive analysis of requirements; detailed design documentation..."
                }
            },
            // ... 5 more criteria
        ]
    },
    // ... 3 more presets (web_development, data_structures_algorithms, capstone_project)
};
```

---

## 5. Template Structure Examples

### Grading Dashboard Key Sections
```html
<!-- Stats Cards -->
<div class="row g-3">
    <div class="col-md-3">
        <div class="card stat-card">
            <div class="card-body">
                <h6>Total Submissions</h6>
                <h3>{{ submissions | length }}</h3>
            </div>
        </div>
    </div>
    <!-- Similar cards for Graded, Pending, Average Score -->
</div>

<!-- Submission Table -->
<table class="table table-hover">
    <thead>
        <tr>
            <th>Student</th>
            <th>Submitted</th>
            <th>Status</th>
            <th>Score</th>
            <th>Actions</th>
        </tr>
    </thead>
    <tbody>
        {% for submission in submissions %}
        <tr>
            <td>{{ submission.student.name }}</td>
            <td>{{ submission.submitted_at.strftime('%Y-%m-%d %H:%M') }}</td>
            <td>
                <span class="badge {% if submission.graded %}bg-success{% else %}bg-warning{% endif %}">
                    {{ 'Graded' if submission.graded else 'Pending' }}
                </span>
            </td>
            <td>{{ submission.total_points or 'N/A' }}/{{ rubric.total_points if rubric }}</td>
            <td>
                <a href="{{ url_for(...) }}" class="btn btn-sm btn-primary">Grade</a>
            </td>
        </tr>
        {% endfor %}
    </tbody>
</table>
```

### Grade Submission Key Sections
```html
<!-- Rubric Criteria Display -->
{% for criterion in rubric.criteria %}
<div class="criterion-card mb-4">
    <h6>{{ criterion.name }}</h6>
    <p class="criterion-description">{{ criterion.description }}</p>
    
    <!-- Point Slider -->
    <div class="point-slider">
        <input type="range" 
               name="criterion_{{ criterion.id }}" 
               min="0" 
               max="{{ criterion.points }}"
               value="0"
               class="criterion-slider"
               data-criterion="{{ criterion.id }}">
        <span class="current-points">0</span> / {{ criterion.points }} points
    </div>
    
    <!-- Performance Level Display -->
    <div class="performance-level">
        <small id="level_{{ criterion.id }}">No evidence</small>
    </div>
    
    <!-- Notes/Feedback -->
    <textarea name="notes_{{ criterion.id }}" 
              class="form-control mt-2" 
              placeholder="Feedback for this criterion..."></textarea>
</div>
{% endfor %}

<!-- Overall Feedback -->
<div class="overall-feedback mt-4">
    <label>Overall Feedback</label>
    <textarea name="overall_feedback" class="form-control" rows="5"></textarea>
</div>

<!-- Total Points Display -->
<div class="total-points mt-3">
    <h5>Total Points: <span id="total-points">0</span> / {{ rubric.total_points }}</h5>
</div>
```

---

## 6. Key JavaScript Event Handlers

### Preset Selection Handler
```javascript
document.querySelectorAll('.preset-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        const presetKey = this.dataset.preset;
        const rubric = createRubricFromPreset(presetKey);
        
        if (rubric) {
            document.getElementById('title').value = rubric.title;
            document.getElementById('description').value = rubric.description;
            document.getElementById('total_points').value = rubric.total_points;
            
            // Load criteria into form
            loadNZQAPreset(presetKey);
        }
    });
});
```

### Point Slider Handler
```javascript
document.querySelectorAll('.criterion-slider').forEach(slider => {
    slider.addEventListener('input', function() {
        const criterion = NZQA_RUBRICS.programming_fundamentals.criteria
            .find(c => c.name === this.dataset.criterion);
        
        const points = parseInt(this.value);
        document.getElementById(`level_${this.dataset.criterion}`).textContent = 
            criterion.levels[points] || 'No evidence';
        
        // Update total
        updateTotalPoints();
    });
});
```

### Total Points Calculation
```javascript
function updateTotalPoints() {
    let total = 0;
    document.querySelectorAll('.criterion-slider').forEach(slider => {
        total += parseInt(slider.value);
    });
    document.getElementById('total-points').textContent = total;
}
```

---

## 7. HTML Input Structures

### Rubric Criteria Form
```html
<div class="criteria-form">
    <h6>Rubric Criteria</h6>
    <div id="criteria-container">
        <div class="criterion-input-group" data-criterion-index="0">
            <input type="text" name="criterion_0_name" placeholder="Criterion name" class="form-control mb-2">
            <textarea name="criterion_0_desc" placeholder="Description" class="form-control mb-2"></textarea>
            <input type="number" name="criterion_0_points" placeholder="Points" class="form-control mb-2" value="20">
            <button type="button" class="btn btn-sm btn-danger remove-criterion">Remove</button>
        </div>
    </div>
    <button type="button" class="btn btn-primary mt-2" onclick="addCriterion()">
        Add Criterion
    </button>
</div>
```

### Grading Form Inputs
```html
<form method="POST">
    <!-- Hidden: Criterion Point Values -->
    {% for criterion in rubric.criteria %}
    <input type="hidden" name="criterion_{{ criterion.id }}" id="points_{{ criterion.id }}" value="0">
    <input type="hidden" name="notes_{{ criterion.id }}" id="notes_{{ criterion.id }}" value="">
    {% endfor %}
    
    <!-- Hidden: Overall Feedback -->
    <input type="hidden" name="overall_feedback" id="overall_feedback" value="">
    
    <!-- Visible: Sliders and Feedback (see templates) -->
    
    <!-- Submit -->
    <button type="submit" class="btn btn-success">
        <i class="fas fa-check"></i> Submit Grades
    </button>
</form>
```

---

## 8. CSS Key Styles

### Preset Buttons
```css
.preset-btn {
    border-color: #17a2b8;
    color: #17a2b8;
    transition: all 0.3s ease;
}

.preset-btn:hover {
    background-color: #17a2b8;
    color: white;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(23, 162, 184, 0.3);
}
```

### Criterion Cards
```css
.criterion-card {
    border-left: 4px solid #007bff;
    padding: 1.5rem;
    background: #f8f9fa;
    border-radius: 4px;
}

.criterion-slider {
    width: 100%;
    height: 8px;
    cursor: pointer;
}
```

### Stats Cards
```css
.stat-card {
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.stat-card:hover {
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}
```

---

## 9. Database Query Examples

### Load Rubric with Criteria
```python
rubric = AssignmentRubric.query.filter_by(
    assignment_id=assignment_id
).options(joinedload(AssignmentRubric.criteria)).first()
```

### Load Submission with Grades
```python
submission = AssignmentSubmission.query.filter_by(
    id=submission_id
).options(joinedload(AssignmentSubmission.grades)).first()
```

### Get Grade Details for Submission
```python
grades = GradeDetail.query.filter_by(
    submission_id=submission_id
).options(joinedload(GradeDetail.criterion)).all()
```

---

## 10. Form Validation

### Server-Side Validation
```python
if not title or len(title) < 3:
    flash('Rubric title must be at least 3 characters', 'error')
    return redirect(...)

if total_points <= 0:
    flash('Total points must be greater than 0', 'error')
    return redirect(...)

total_criterion_points = sum(int(request.form.get(f'criterion_{i}_points', 0)) 
                              for i in range(10) 
                              if request.form.get(f'criterion_{i}_name'))

if total_criterion_points != total_points:
    flash(f'Criteria points ({total_criterion_points}) must equal total ({total_points})', 'warning')
```

### Client-Side Validation
```javascript
function validateRubric() {
    const criteria = document.querySelectorAll('.criterion-input-group');
    if (criteria.length === 0) {
        alert('Please add at least one criterion');
        return false;
    }
    
    // Validate points match
    updateTotalPoints();
    return true;
}
```

---

## Configuration & Setup

### No Additional Dependencies Required
- Uses existing Flask, SQLAlchemy, WTForms
- JavaScript is vanilla (no jQuery required)
- CSS uses existing Bootstrap framework
- HTML templates extend existing base.html

### Database Migration (if using Alembic)
```bash
# Generate migration
flask db migrate -m "Add rubric models for grading"

# Apply migration
flask db upgrade
```

---

This reference guide covers all major code components from TODO #15 implementation.
For complete files, see actual implementation in:
- `app/models.py`
- `app/routes/assignments.py`
- `app/static/js/nzqa_rubrics.js`
- `app/templates/assignments/*.html`

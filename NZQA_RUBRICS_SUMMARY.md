# NZQA Technology Curriculum Rubrics Implementation
**Class Training System - Phase 4 (Year 9-10) Assessment Standards**

---

## Overview

The Class Training System now includes comprehensive rubric presets aligned with the official **NZQA Technology Curriculum Phase 4** (Years 9-10) achievement standards. These rubrics provide standards-based assessment tools for programming and digital technology instruction.

**Official Curriculum Reference:** https://newzealandcurriculum.tahurangi.education.govt.nz/new-zealand-curriculum-online/new-zealand-curriculum/learning-areas/technology-curriculum/

---

## Four NZQA-Aligned Rubric Presets

### 1. Programming Fundamentals (100 Points)
**Target Audience:** Year 9-10 students  
**Assessment Domains:** Design, Logic, Code Quality, Testing, Ethics, Documentation

#### Criteria Breakdown:
| Criterion | Points | Focus Area |
|-----------|--------|-----------|
| Design Thinking & Planning | 20 | Requirements analysis, algorithmic representation, design documentation |
| Computational Thinking & Logic | 25 | Correctness, control flow, sequences, decisions, loops, data types |
| Code Implementation & Best Practices | 20 | Naming conventions, comments, formatting, functions, DRY principles |
| Testing, Debugging & Validation | 15 | Test cases, error identification, edge case handling, requirements validation |
| Digital Citizenship & Ethics | 10 | Attribution, accessibility, inclusivity, ethical implications |
| Documentation & Communication | 10 | Code comments, written explanations, concept articulation |

**Total Points:** 100  
**Performance Levels:** 6 levels per criterion (0, 5, 8-10, 12-15, 20, 25)

#### Key Achievement Standards:
- ✅ Program produces correct output for all test cases
- ✅ Clear evidence of problem decomposition and planning
- ✅ Code demonstrates professional quality and maintainability
- ✅ Systematic testing approach with documented edge cases
- ✅ Proper attribution and accessibility considerations
- ✅ Comprehensive documentation of learning

---

### 2. Web Development & Digital Design (100 Points)
**Target Audience:** Year 9-10 students  
**Assessment Domains:** UX Design, HTML/CSS, JavaScript, Accessibility, Code Organization, Innovation

#### Criteria Breakdown:
| Criterion | Points | Focus Area |
|-----------|--------|-----------|
| User-Centered Design Thinking | 15 | User analysis, accessibility features, responsive design, usability validation |
| HTML/CSS Technical Implementation | 20 | Semantic HTML, CSS layouts (flexbox/grid), responsive design, device compatibility |
| JavaScript Functionality & Interactivity | 20 | DOM manipulation, event handling, form validation, smooth interactions |
| Digital Citizenship & Accessibility | 15 | WCAG guidelines, data privacy, ethical content use, inclusive design |
| Code Organization & Maintainability | 15 | Structure, naming conventions, comments, follow standards |
| Problem-Solving & Innovation | 15 | Creative solutions, beyond requirements, thoughtful enhancements |

**Total Points:** 100  
**Performance Levels:** 6 levels per criterion

#### Key Achievement Standards:
- ✅ Website is fully responsive across all devices
- ✅ Semantic HTML with proper structure and accessibility features
- ✅ JavaScript provides smooth, functional interactions
- ✅ WCAG AA accessibility compliance
- ✅ Professional, user-focused design
- ✅ Evidence of creative problem-solving

---

### 3. Data Structures & Algorithms (100 Points)
**Target Audience:** Year 10 students  
**Assessment Domains:** Efficiency, Data Selection, Code Quality, Testing, Analysis, Ethics

#### Criteria Breakdown:
| Criterion | Points | Focus Area |
|-----------|--------|-----------|
| Algorithm Correctness & Efficiency | 25 | Correct results, time complexity, optimization, efficiency tradeoffs |
| Data Structure Selection & Usage | 20 | Appropriate selection (arrays, lists, dicts, objects, sets), justified choices |
| Code Quality & Implementation | 15 | Clean code, meaningful names, documentation, professional standards |
| Testing, Validation & Edge Cases | 15 | Multiple test cases, all edge cases, proper error handling, validation |
| Computational Thinking & Analysis | 15 | Deep understanding, performance analysis, design justification, improvements |
| Digital Citizenship & Academic Integrity | 10 | Attribution, security considerations, ethical analysis |

**Total Points:** 100  
**Performance Levels:** 6 levels per criterion

#### Key Achievement Standards:
- ✅ Algorithm produces correct results with reasonable efficiency
- ✅ Data structures appropriately selected and justified
- ✅ Comprehensive testing with edge case coverage
- ✅ Deep understanding of computational principles
- ✅ Proper attribution of external code/resources
- ✅ Security and ethical implications addressed

---

### 4. Capstone/Integrated Project (100 Points)
**Target Audience:** Year 10 students  
**Assessment Domains:** Planning, Technical Mastery, Design, Problem-Solving, Documentation, Ethics

#### Criteria Breakdown:
| Criterion | Points | Focus Area |
|-----------|--------|-----------|
| Project Planning & Management | 15 | Clear scope, timeline, milestones, adaptability to changes |
| Technical Implementation & Integration | 25 | Technology mastery, multiple tech integration, sophisticated thinking |
| Design Thinking & User Experience | 15 | User-centered design, intuitive UX, professional appearance, testing |
| Problem-Solving & Innovation | 15 | Sophisticated problem-solving, complex challenge handling, innovations |
| Documentation & Communication | 15 | Design rationale, user guides, code comments, technical docs |
| Digital Citizenship, Ethics & Responsibility | 15 | Privacy, security, accessibility, sustainability, social responsibility |

**Total Points:** 100  
**Performance Levels:** 6 levels per criterion

#### Key Achievement Standards:
- ✅ Professional project management with clear planning and milestones
- ✅ Sophisticated technical implementation with multiple technologies
- ✅ User-tested, intuitive design with professional appearance
- ✅ Comprehensive documentation and clear communication
- ✅ Innovative solutions to complex problems
- ✅ Exemplary ethical standards and social responsibility

---

## Implementation Architecture

### Database Models
Located in `app/models.py`:

```python
class AssignmentRubric(db.Model):
    """Stores rubric definitions for assignments"""
    id = db.Column(db.Integer, primary_key=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignment.id'))
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    total_points = db.Column(db.Integer, default=100)
    criteria = db.relationship('RubricCriterion', cascade='all, delete-orphan')

class RubricCriterion(db.Model):
    """Individual grading criteria within a rubric"""
    id = db.Column(db.Integer, primary_key=True)
    rubric_id = db.Column(db.Integer, db.ForeignKey('assignment_rubric.id'))
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    points = db.Column(db.Integer)
    order = db.Column(db.Integer)

class GradeDetail(db.Model):
    """Tracks points awarded per criterion for each submission"""
    id = db.Column(db.Integer, primary_key=True)
    submission_id = db.Column(db.Integer, db.ForeignKey('assignment_submission.id'))
    criterion_id = db.Column(db.Integer, db.ForeignKey('rubric_criterion.id'))
    points_awarded = db.Column(db.Integer)
    notes = db.Column(db.Text)
```

### Frontend Components
Located in `app/static/js/nzqa_rubrics.js`:

```javascript
// Access rubric presets
const NZQA_RUBRICS = {
    programming_fundamentals: { /* 20 points criteria */ },
    web_development: { /* 100 points total */ },
    data_structures_algorithms: { /* 100 points total */ },
    capstone_project: { /* 100 points total */ }
}

// Helper functions
createRubricFromPreset(presetKey)      // Load preset rubric
getAvailableRubrics()                  // List all presets
getPointLevelDescription(criterion, points)  // Get level description
```

### Routes & Endpoints
Located in `app/routes/assignments.py`:

- **GET/POST `/grading_dashboard`** - View all submissions with statistics
- **GET/POST `/submission/{id}/grade`** - Grade individual submission with rubric
- **GET/POST `/manage_rubric`** - Create/edit rubrics with preset templates

---

## Performance Levels Scale

Each criterion includes detailed performance level descriptors at multiple points:

### Example: Programming Fundamentals - Design Thinking (20 points)
- **0 Points:** No evidence of planning or design thinking
- **5 Points:** Minimal planning; problem requirements unclear or missing
- **10 Points:** Basic problem analysis; simple design plan with gaps
- **15 Points:** Clear problem identification; logical design with mostly complete documentation
- **20 Points:** Comprehensive analysis of requirements; detailed design documentation; clear algorithmic representation

This multi-level approach provides clear expectations and distinguishes between partial, proficient, and advanced performance.

---

## How to Use

### For Teachers

1. **Creating an Assignment with Grading Rubric:**
   - Create assignment
   - Click "Add Rubric"
   - Choose from 4 NZQA presets OR create custom rubric
   - Presets automatically populate criteria with standards-aligned descriptions

2. **Grading Student Work:**
   - View submission in grading dashboard
   - Use interactive sliders to award points per criterion
   - Real-time total calculation shows overall points
   - Add criterion-specific feedback notes
   - Comments reference NZQA standards

3. **Customizing Rubrics:**
   - Edit rubric templates to match specific course needs
   - Adjust point allocations while maintaining standard descriptors
   - Save custom variations for reuse

### For Students

1. **Understanding Expectations:**
   - View assignment rubric before submitting
   - Read criterion descriptions and performance levels
   - Know exactly what NZQA standards they're being assessed against

2. **Receiving Feedback:**
   - See points awarded per criterion with level descriptions
   - Understand strengths and areas for improvement
   - Reference to specific NZQA standards explains why

---

## Alignment with NZQA Standards

### Design Thinking & Problem Decomposition
- **NZQA Domain:** Computational Thinking and Design Processes
- **Assessed by:** Rubric evidence of planning, pseudocode, flowcharts
- **Standards:** Ability to break problems into manageable parts

### Computational Thinking & Programming Logic
- **NZQA Domain:** Programming and Algorithms
- **Assessed by:** Program correctness, control structures, data types
- **Standards:** Understanding of sequences, conditionals, loops

### Code Quality & Best Practices
- **NZQA Domain:** Programming Practices
- **Assessed by:** Naming, comments, formatting, functions
- **Standards:** Professional, maintainable code standards

### Digital Citizenship & Ethics
- **NZQA Domain:** Digital Citizenship and Ethics
- **Assessed by:** Attribution, accessibility, inclusivity
- **Standards:** Ethical use of technology, inclusive design

### Documentation & Communication
- **NZQA Domain:** Communication of Learning
- **Assessed by:** Code comments, written explanations
- **Standards:** Clear articulation of learning and understanding

---

## Point Distribution Summary

### Programming Fundamentals
- Technical Criteria (Design + Logic + Code + Testing): 80 points
- Soft Skills (Ethics + Documentation): 20 points
- Emphasis: Core programming competencies

### Web Development
- Technical Criteria (HTML/CSS + JavaScript): 40 points
- Design & User Experience: 15 points
- Soft Skills (Accessibility + Organization + Innovation): 45 points
- Emphasis: User-centered development

### Data Structures & Algorithms
- Technical Criteria (Algorithm + Data Structures + Testing): 60 points
- Analysis & Reflection: 15 points
- Soft Skills (Code Quality + Ethics): 25 points
- Emphasis: Computational efficiency and depth

### Capstone Project
- All domains equally weighted: 15-25 points each
- Emphasis: Comprehensive integration of all competencies

---

## Features

✅ **Official Standards Alignment** - Based on NZQA Technology Curriculum Phase 4  
✅ **Four Complete Rubric Templates** - Ready to use out of the box  
✅ **Performance Level Descriptors** - Clear expectations at each point level  
✅ **Flexible Customization** - Modify presets to match course specific needs  
✅ **Digital Citizenship Focus** - Ethics and accessibility built into every rubric  
✅ **Student-Visible Standards** - Students understand NZQA expectations  
✅ **Database Persistence** - Rubrics and grades tracked in database  
✅ **Real-time Calculations** - Automatic point totals during grading  

---

## File Locations

- **Rubric Presets:** `app/static/js/nzqa_rubrics.js` (383 lines)
- **Database Models:** `app/models.py` (AssignmentRubric, RubricCriterion, GradeDetail)
- **Routes:** `app/routes/assignments.py` (grading_dashboard, grade_submission_advanced, manage_rubric)
- **Templates:**
  - `app/templates/assignments/grading_dashboard.html` (195 lines)
  - `app/templates/assignments/grade_submission.html` (300+ lines)
  - `app/templates/assignments/manage_rubric.html` (456 lines)

---

## Next Steps

1. **Backend Integration Testing** - Verify rubric data persists and loads correctly
2. **Grading Workflow Validation** - Test complete submission → grade → feedback flow
3. **Preset Application** - Verify rubric presets load and apply correctly
4. **Student View** - Ensure students can see rubric criteria before submitting
5. **Report Generation** - Create reports showing rubric performance analytics

---

## References

- NZQA Technology Curriculum: https://newzealandcurriculum.tahurangi.education.govt.nz/
- Phase 4 (Year 9-10) Specific: Achievement standards for programming and digital technology
- Assessment Framework: Multi-level rubric with detailed performance descriptors
- Best Practices: Standards-based assessment with clear learning targets

---

**Last Updated:** December 2025  
**Status:** TODO #15 Completed - Ready for Testing and Deployment

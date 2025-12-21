# Script to update template_path for all module lessons
from app import create_app, db
from app.models import Lesson

# Mapping of lesson titles to template paths (adjust as needed)
lesson_template_map = {
    # Module 1: Commenting
    'Introduction to Code Comments': 'modules/module1/m1lesson_intro.html',
    'Section 1: Python Comments - Best Practices': 'modules/module1/m1lesson1.html',
    'Section 2: JavaScript Comments - Best Practices': 'modules/module1/m1lesson2.html',
    'Section 3: HTML and CSS Comments - Best Practices': 'modules/module1/m1lesson3.html',
    'Commenting Best Practices - Summary': 'modules/module1/m1lesson_summary.html',
    # Module 1 Contents
    'Module 1: Commenting': 'modules/module1/m1_contents.html',

    # Module 2: Debugging
    'Introduction to Code Debugging': 'modules/module2/m2lesson_intro.html',
    'Section 1: Python Debugging - Best Practices': 'modules/module2/m2lesson1.html',
    'Section 2: JavaScript Debugging - Best Practices': 'modules/module2/m2lesson2.html',
    'Section 3: HTML and CSS Debugging - Best Practices': 'modules/module2/m2lesson3.html',
    '99. Debugging Best Practices - Summary': 'modules/module2/m2lesson_summary.html',
    'Module 2: Debugging': 'modules/module2/m2_contents.html',

    # Module 3: Checking for Assessment Purposes
    'Module 3: Checking for Assessment Purposes': 'modules/module3/m3_contents.html',
    'Lesson 1: Introduction to Assessment Checking': 'modules/module3/m3lesson0.html',
    'Lesson 2: Automated Checking Systems': 'modules/module3/m3lesson1.html',
    'Lesson 3: Manual Review Strategies': 'modules/module3/m3lesson2.html',
    'Lesson 4: Feedback and Reporting': 'modules/module3/m3lesson3.html',
}

def update_template_paths():
    app = create_app()
    with app.app_context():
        updated = 0
        for lesson in Lesson.query.all():
            if lesson.title in lesson_template_map:
                lesson.template_path = lesson_template_map[lesson.title]
                updated += 1
        db.session.commit()
        print(f"Updated template_path for {updated} lessons.")

if __name__ == "__main__":
    update_template_paths()

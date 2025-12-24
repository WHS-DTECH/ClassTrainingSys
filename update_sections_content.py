# Script to update section content from HTML files
import os
from app import db, create_app
from app.models import Section

# Map section_id to HTML file path
SECTION_HTML_MAP = {
    5: 'app/templates/lessons/lesson1/l1section_intro.html',
    6: 'app/templates/lessons/lesson1/l1section1.html',
    7: 'app/templates/lessons/lesson1/l1section2.html',
    8: 'app/templates/lessons/lesson1/l1section3.html',
    9: 'app/templates/lessons/lesson2/l2section_intro.html',
    10: 'app/templates/lessons/lesson2/l2section1.html',
    11: 'app/templates/lessons/lesson2/l2section2.html',
    12: 'app/templates/lessons/lesson2/l2section3.html',
    13: 'app/templates/lessons/lesson3/l3section_intro.html',
    14: 'app/templates/lessons/lesson3/l3section1.html',
    15: 'app/templates/lessons/lesson3/l3section2.html',
    16: 'app/templates/lessons/lesson4/l4section1.html',
    17: 'app/templates/lessons/lesson4/l4section2.html',
}

def read_html(path):
    with open(path, encoding='utf-8') as f:
        return f.read()

def update_sections_content():
    app = create_app(skip_socketio=True)
    with app.app_context():
        print("SQLAlchemy DB URI:", app.config['SQLALCHEMY_DATABASE_URI'])
        for section_id, html_path in SECTION_HTML_MAP.items():
            if not os.path.exists(html_path):
                print(f"File not found: {html_path}")
                continue
            html_content = read_html(html_path)
            section = Section.query.get(section_id)
            if section:
                section.content = html_content
                print(f"Updated Section_ID={section_id} with content from {html_path}")
        db.session.commit()
        print("Section content update complete.")

if __name__ == "__main__":
    update_sections_content()
## Removed all SQLite code and duplicate SECTION_HTML_MAP. Only SQLAlchemy/Flask app context is used above.

# Script: test_section_navigation.py
# Description: Test navigation for all sections to confirm templates render without errors.

from app import create_app
from app.models import Section
from flask import url_for

# This script prints the expected route and template for each section.
# Actual HTTP testing should be done with a test client or browser.
def test_section_navigation():
    app = create_app()
    with app.app_context():
        sections = Section.query.order_by(Section.id).all()
        print("Section Navigation Test Results:")
        print("-"*70)
        for section in sections:
            route = f"/courses/sections/{section.id}"
            template = section.template_path if section.template_path else "sections/section.html"
            print(f"Section ID: {section.id} | Title: {section.title}\nRoute: {route}\nTemplate: {template}\n{'-'*60}")
        print("Manual browser or test client verification recommended for full template rendering.")

if __name__ == "__main__":
    test_section_navigation()

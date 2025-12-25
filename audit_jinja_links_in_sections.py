# Script: audit_jinja_links_in_sections.py
# Description: Find sections with raw Jinja code in their content field (e.g., {{ url_for(...) }})

from app import create_app
from app.models import Section
import re

def audit_jinja_links_in_sections():
    app = create_app()
    with app.app_context():
        pattern = re.compile(r"\{\{\s*url_for\(")
        sections = Section.query.all()
        found = False
        for section in sections:
            if section.content and pattern.search(section.content):
                print(f"Section ID: {section.id} | Title: {section.title}\nRaw Jinja link found in content:\n{section.content}\n{'-'*60}")
                found = True
        if not found:
            print("No sections with raw Jinja links found.")

if __name__ == "__main__":
    audit_jinja_links_in_sections()

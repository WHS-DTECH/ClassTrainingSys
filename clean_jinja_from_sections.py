"""
Script to clean up raw Jinja template code from section content fields in the database.
Removes {% extends ... %}, {% block ... %}, and {{ ... }} from section content.
"""

import re
from app import create_app
from app.models import db, Section

# Patterns to remove
JINJA_BLOCK_PATTERN = re.compile(r"{%-?\s*(extends|block|endblock)[^%]*%}|{\{[^}]*\}}", re.MULTILINE)


def clean_jinja_from_content(content):
    # Remove Jinja block tags and expressions
    cleaned = JINJA_BLOCK_PATTERN.sub("", content)
    # Remove any leftover empty lines or excessive whitespace
    cleaned = re.sub(r"\n{2,}", "\n", cleaned)
    return cleaned.strip()


def main():
    app = create_app()
    with app.app_context():
        sections = Section.query.all()
        affected = []
        for section in sections:
            original = section.content or ""
            cleaned = clean_jinja_from_content(original)
            if original != cleaned:
                section.content = cleaned
                affected.append(section.id)
        if affected:
            db.session.commit()
            print(f"Cleaned Jinja code from sections: {affected}")
        else:
            print("No sections required cleaning.")

if __name__ == "__main__":
    main()

# clean_duplicate_practice_blocks.py

from app import create_app, db
from app.models import Lesson
import re

def remove_duplicate_practice_blocks(content):
    import re
    # Find all blocks
    pattern = re.compile(
        r'(Practice: Where Would You Debug\?.*?)(?=Practice: Where Would You Debug\?|$)',
        re.DOTALL
    )
    matches = pattern.findall(content)
    if matches and len(matches) > 1:
        # Prefer the block with interactive elements
        interactive = None
        for block in matches:
            if '<input' in block or '<button' in block or 'Show Solution' in block:
                interactive = block
                break
        # Fallback to first if none are interactive
        if not interactive:
            interactive = matches[0]
        # Remove all and keep only the interactive one
        # Remove all blocks
        cleaned = pattern.sub('', content)
        # Insert the interactive block at the first occurrence
        cleaned = interactive + cleaned
        return cleaned
    return content

app = create_app()  # Use the factory to create the app

with app.app_context():
    lessons = Lesson.query.all()
    for lesson in lessons:
        original = lesson.content
        cleaned = remove_duplicate_practice_blocks(original)
        if cleaned != original:
            print(f"Cleaning lesson {lesson.id} - duplicates found.")
            lesson.content = cleaned
    db.session.commit()
    print("Duplicate practice blocks cleaned.")
# Audit and Fix Lesson Content Links

## Audit Results
- Lessons with broken links due to raw Jinja code (e.g., `{{ url_for('courses.view_lesson', lesson_id=lesson.id, section=1) }}`) must be identified in the database.
- These links do not render correctly and result in page not found errors.

## Fix Plan
- Update lesson content to use actual URLs, not raw Jinja code.
- Refactor templates to generate links dynamically if needed.
- Test all lesson and section links to confirm they work as expected.

## Next Steps
1. Run a script to search lesson content for raw Jinja code and list affected lessons.
2. For each affected lesson, update the content to use a valid URL or template logic.
3. Confirm that all links work after changes.

---
Created by GitHub Copilot on 2025-12-25.
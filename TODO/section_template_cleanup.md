# TODO: Section Template Cleanup

## Problem
- The Flask route for viewing a section (`view_section` in app/routes/courses.py) attempts to render a template based on the section's `template_path` field.
- If `template_path` is not set, it defaults to 'sections/section.html'.
- There is currently no 'sections/section.html' file in the codebase, which may cause template errors.

## Action Items
- [ ] Audit all Section records in the database for their `template_path` value.
- [ ] Create a default template at app/templates/sections/section.html for fallback rendering.
- [ ] Ensure every section either has a valid custom template or uses the default.
- [ ] Refactor or remove unused/legacy section templates.
- [ ] Test section navigation to confirm no template errors occur.

## Notes
- This cleanup will prevent runtime errors and provide a consistent section view for all lessons.
- Assign to: [REVIEWER NAME]
- Priority: Medium

---
Created by GitHub Copilot on 2025-12-25.
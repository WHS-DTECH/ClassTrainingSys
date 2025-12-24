# TODO - Migration

1. Change the database structure to a Neon database hooked to a Render web service.
2. Restructure the database organization:
   - Move all lessons to a sections table. Clean up foreign key issues by replacing any reference to lessons with sections and hook sections to courses. Delete all data in the lessons table in preparation for the next step.
   - Duplicate the courses table to lessons table. Clean up foreign key issues by making sure the link is now between lesson to section tables. Delete all data in the courses table in preparation for the next step.
   - Populate the courses table: all lessons are to be linked to one course named 'Programming Documentation'. Make sure the enrolment process works for all users.

---

A copy of this TODO list should be updated here whenever changes are made to the migration plan.

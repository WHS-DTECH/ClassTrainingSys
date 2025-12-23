"""Phase 1.2: Rename lessons table to sections

Revision ID: rename_lessons_to_sections
Revises: add_lessons2_table
Create Date: 2025-12-23 05:00:00.000000

This migration renames the 'lessons' table to 'sections' to represent
the 3rd level in the hierarchy: Course > Lesson2 > Section

All foreign keys and constraints are updated accordingly.
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'rename_lessons_to_sections'
down_revision = 'add_lessons2_table'
branch_labels = None
depends_on = None


def upgrade():
    """Rename lessons table to sections"""
    
    # PostgreSQL specific: Rename the table
    op.execute('ALTER TABLE lessons RENAME TO sections')
    
    # Rename the primary key constraint
    op.execute('ALTER TABLE sections RENAME CONSTRAINT lessons_pkey TO sections_pkey')
    
    # Rename foreign key constraint: lessons_course_id_fkey -> sections_course_id_fkey
    op.execute('ALTER TABLE sections RENAME CONSTRAINT lessons_course_id_fkey TO sections_course_id_fkey')
    
    # Note: Indexes are automatically renamed by PostgreSQL
    # but we should verify: lesson_progress and lesson_feedback tables
    # still have correct foreign keys - those will be handled in Phase 1.4


def downgrade():
    """Rename sections table back to lessons"""
    
    # PostgreSQL specific: Rename the table back
    op.execute('ALTER TABLE sections RENAME TO lessons')
    
    # Rename the primary key constraint back
    op.execute('ALTER TABLE lessons RENAME CONSTRAINT sections_pkey TO lessons_pkey')
    
    # Rename foreign key constraint back
    op.execute('ALTER TABLE lessons RENAME CONSTRAINT sections_course_id_fkey TO lessons_course_id_fkey')

"""Phase 1.1: Create lessons2 table (2nd level in 3-level hierarchy)

Revision ID: add_lessons2_table
Revises: 
Create Date: 2025-12-23 04:00:00.000000

This migration creates a new 'lessons2' table to represent the 2nd level
in the Course > Lesson > Section hierarchy.

The 'lessons2' table will be used to group existing 'lessons' (which will
become 'sections') under lessons.
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_lessons2_table'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    """Create the lessons2 table"""
    
    # Create new 'lessons2' table (2nd level)
    op.create_table(
        'lessons2',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('course_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('order', sa.Integer(), server_default='0'),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create index for faster lookups
    op.create_index(
        'ix_lessons2_course_id',
        'lessons2',
        ['course_id'],
        unique=False
    )


def downgrade():
    """Drop the lessons2 table"""
    op.drop_index('ix_lessons2_course_id', table_name='lessons2')
    op.drop_table('lessons2')

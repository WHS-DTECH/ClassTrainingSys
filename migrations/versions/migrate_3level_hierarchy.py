"""Migrate to 3-level hierarchy: Course > Lesson > Section

Revision ID: 3level_hierarchy
Revises: 
Create Date: 2025-12-23 04:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3level_hierarchy'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    """Upgrade database to 3-level hierarchy"""
    
    # Step 1: Create new 'lessons' table (2nd level - parent of sections)
    op.create_table(
        'lessons',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('course_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('order', sa.Integer(), default=0),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Step 2: Rename current 'lessons' table to 'sections'
    op.rename_table('lessons', 'sections')
    
    # Step 3: Update sections table structure
    # Drop the old course_id foreign key
    op.drop_constraint('lessons_course_id_fkey', 'sections', type_='foreignkey')
    
    # Add lesson_id column to sections
    op.add_column('sections', sa.Column('lesson_id', sa.Integer(), nullable=True))
    
    # Step 4: Migrate data - create lesson records from sections
    # This is done via raw SQL to preserve data
    op.execute("""
        INSERT INTO lessons (course_id, title, description, created_at, updated_at)
        SELECT DISTINCT course_id, 'Default Lesson for ' || course_id, '', NOW(), NOW()
        FROM sections
    """)
    
    # Step 5: Update sections to reference new lessons
    op.execute("""
        UPDATE sections s
        SET lesson_id = (
            SELECT l.id FROM lessons l 
            WHERE l.course_id = s.course_id 
            LIMIT 1
        )
    """)
    
    # Step 6: Make lesson_id NOT NULL in sections
    op.alter_column('sections', 'lesson_id', nullable=False)
    
    # Step 7: Add foreign key for lesson_id
    op.create_foreign_key(
        'sections_lesson_id_fkey', 'sections', 'lessons',
        ['lesson_id'], ['id']
    )
    
    # Step 8: Rename lesson_progress to section_progress
    op.rename_table('lesson_progress', 'section_progress')
    
    # Step 9: Update section_progress foreign key
    op.drop_constraint('lesson_progress_lesson_id_fkey', 'section_progress', type_='foreignkey')
    
    # Add section_id column
    with op.batch_alter_table('section_progress') as batch_op:
        batch_op.add_column(sa.Column('section_id', sa.Integer(), nullable=True))
        # Migrate data from lesson_id to section_id
        # Since old lesson_id now refers to sections, rename it
        batch_op.execute('ALTER TABLE section_progress RENAME COLUMN lesson_id TO section_id')
        # Make section_id NOT NULL
        batch_op.alter_column('section_id', nullable=False)
        batch_op.create_foreign_key(
            'section_progress_section_id_fkey', 'section_progress', 'sections',
            ['section_id'], ['id']
        )
    
    # Step 10: Rename lesson_feedback to section_feedback
    op.rename_table('lesson_feedback', 'section_feedback')
    
    # Step 11: Update section_feedback foreign key
    op.drop_constraint('lesson_feedback_lesson_id_fkey', 'section_feedback', type_='foreignkey')
    
    with op.batch_alter_table('section_feedback') as batch_op:
        batch_op.add_column(sa.Column('section_id', sa.Integer(), nullable=True))
        batch_op.execute('ALTER TABLE section_feedback RENAME COLUMN lesson_id TO section_id')
        batch_op.alter_column('section_id', nullable=False)
        batch_op.create_foreign_key(
            'section_feedback_section_id_fkey', 'section_feedback', 'sections',
            ['section_id'], ['id']
        )
    
    # Step 12: Update comment_feedback to reference sections
    op.drop_constraint('comment_feedback_lesson_id_fkey', 'comment_feedback', type_='foreignkey')
    
    with op.batch_alter_table('comment_feedback') as batch_op:
        batch_op.add_column(sa.Column('section_id', sa.Integer(), nullable=True))
        batch_op.execute('ALTER TABLE comment_feedback RENAME COLUMN lesson_id TO section_id')
        batch_op.alter_column('section_id', nullable=False)
        batch_op.create_foreign_key(
            'comment_feedback_section_id_fkey', 'comment_feedback', 'sections',
            ['section_id'], ['id']
        )
    
    # Step 13: Update assignments table - add lesson_id
    op.add_column('assignments', sa.Column('lesson_id', sa.Integer(), nullable=True))
    op.create_foreign_key(
        'assignments_lesson_id_fkey', 'assignments', 'lessons',
        ['lesson_id'], ['id']
    )
    
    # Step 14: Update quizzes table - add lesson_id
    op.add_column('quizzes', sa.Column('lesson_id', sa.Integer(), nullable=True))
    op.create_foreign_key(
        'quizzes_lesson_id_fkey', 'quizzes', 'lessons',
        ['lesson_id'], ['id']
    )


def downgrade():
    """Downgrade - revert to 2-level hierarchy"""
    
    # Reverse all operations
    op.drop_constraint('quizzes_lesson_id_fkey', 'quizzes', type_='foreignkey')
    op.drop_column('quizzes', 'lesson_id')
    
    op.drop_constraint('assignments_lesson_id_fkey', 'assignments', type_='foreignkey')
    op.drop_column('assignments', 'lesson_id')
    
    # Revert comment_feedback
    op.drop_constraint('comment_feedback_section_id_fkey', 'comment_feedback', type_='foreignkey')
    with op.batch_alter_table('comment_feedback') as batch_op:
        batch_op.execute('ALTER TABLE comment_feedback RENAME COLUMN section_id TO lesson_id')
        batch_op.create_foreign_key(
            'comment_feedback_lesson_id_fkey', 'comment_feedback', 'lessons',
            ['lesson_id'], ['id']
        )
    
    # Revert section_feedback to lesson_feedback
    op.drop_constraint('section_feedback_section_id_fkey', 'section_feedback', type_='foreignkey')
    with op.batch_alter_table('section_feedback') as batch_op:
        batch_op.execute('ALTER TABLE section_feedback RENAME COLUMN section_id TO lesson_id')
        batch_op.create_foreign_key(
            'lesson_feedback_lesson_id_fkey', 'section_feedback', 'lessons',
            ['lesson_id'], ['id']
        )
    op.rename_table('section_feedback', 'lesson_feedback')
    
    # Revert section_progress to lesson_progress
    op.drop_constraint('section_progress_section_id_fkey', 'section_progress', type_='foreignkey')
    with op.batch_alter_table('section_progress') as batch_op:
        batch_op.execute('ALTER TABLE section_progress RENAME COLUMN section_id TO lesson_id')
        batch_op.create_foreign_key(
            'lesson_progress_lesson_id_fkey', 'section_progress', 'lessons',
            ['lesson_id'], ['id']
        )
    op.rename_table('section_progress', 'lesson_progress')
    
    # Revert sections to lessons
    op.drop_constraint('sections_lesson_id_fkey', 'sections', type_='foreignkey')
    op.drop_column('sections', 'lesson_id')
    op.rename_table('sections', 'lessons')
    op.create_foreign_key(
        'lessons_course_id_fkey', 'lessons', 'courses',
        ['course_id'], ['id']
    )
    
    # Drop new lessons table
    op.drop_table('lessons')

"""
Migration: Create assignments and submissions tables
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'ca_submissions_assignments'
down_revision = 'create_enrollments_table'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'assignments',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('course_id', sa.Integer, sa.ForeignKey('courses.id'), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('due_date', sa.DateTime, nullable=True),
        sa.Column('max_points', sa.Integer, nullable=True, default=100),
        sa.Column('created_at', sa.DateTime, nullable=True)
    )
    op.create_table(
        'submissions',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('assignment_id', sa.Integer, sa.ForeignKey('assignments.id'), nullable=False),
        sa.Column('student_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
        sa.Column('content', sa.Text, nullable=True),
        sa.Column('file_path', sa.String(length=500), nullable=True),
        sa.Column('submitted_at', sa.DateTime, nullable=True),
        sa.Column('graded', sa.Boolean, nullable=True, default=False),
        sa.Column('score', sa.Integer, nullable=True),
        sa.Column('feedback', sa.Text, nullable=True),
        sa.Column('graded_at', sa.DateTime, nullable=True)
    )

def downgrade():
    op.drop_table('submissions')
    op.drop_table('assignments')

def downgrade():
    op.drop_table('submissions')
    op.drop_table('assignments')

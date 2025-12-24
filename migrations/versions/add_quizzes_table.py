"""
Add quizzes table
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = 'add_quizzes_table'
down_revision = '9f8563ad22a6'  # Update to your latest migration
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'quizzes',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('course_id', sa.Integer, sa.ForeignKey('courses.id'), nullable=False),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('description', sa.Text),
        sa.Column('time_limit', sa.Integer),
        sa.Column('max_attempts', sa.Integer, default=1),
        sa.Column('created_at', sa.DateTime, server_default=sa.text('CURRENT_TIMESTAMP')),
    )

def downgrade():
    op.drop_table('quizzes')

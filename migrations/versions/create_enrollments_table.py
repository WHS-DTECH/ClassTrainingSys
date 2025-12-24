"""
Migration: Create enrollments table
Revision ID: create_enrollments_table
Revises: make_password_hash_nullable
Create Date: 2025-12-24
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'create_enrollments_table'
down_revision = 'make_password_hash_nullable'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'enrollments',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('student_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
        sa.Column('course_id', sa.Integer, sa.ForeignKey('courses.id'), nullable=False),
        sa.Column('enrolled_at', sa.DateTime, nullable=True),
        sa.Column('status', sa.String(length=20), nullable=True)
    )

def downgrade():
    op.drop_table('enrollments')


"""
Add comment_checks table

Revision ID: add_comment_check_table
Revises: c511bffa91ca
Create Date: 2025-12-18 17:00:00.000000
"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers, used by Alembic.
revision = 'add_comment_check_table'
down_revision = 'c511bffa91ca'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'comment_checks',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
        sa.Column('filename', sa.String(255), nullable=False),
        sa.Column('checked_at', sa.DateTime, default=datetime.utcnow)
    )

def downgrade():
    op.drop_table('comment_checks')

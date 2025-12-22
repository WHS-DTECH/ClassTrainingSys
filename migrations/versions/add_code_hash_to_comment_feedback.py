"""
Revision ID: add_code_hash_to_comment_feedback
Revises: add_comment_check_table
Create Date: 2025-12-22
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_code_hash_to_comment_feedback'
down_revision = 'add_comment_check_table'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('comment_feedback', sa.Column('code_hash', sa.String(length=64), nullable=False, server_default=''))

def downgrade():
    op.drop_column('comment_feedback', 'code_hash')

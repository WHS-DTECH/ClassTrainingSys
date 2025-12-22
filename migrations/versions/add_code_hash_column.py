"""Add code_hash column to comment_feedback

Revision ID: add_code_hash_column
Revises: c511bffa91ca
Create Date: 2025-12-23 08:46:19.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_code_hash_column'
down_revision = 'c511bffa91ca'
branch_labels = None
depends_on = None


def upgrade():
    # Add code_hash column to comment_feedback table
    try:
        op.add_column('comment_feedback', sa.Column('code_hash', sa.String(64), nullable=True))
        # Set default value for existing rows
        op.execute("UPDATE comment_feedback SET code_hash = 'unknown' WHERE code_hash IS NULL")
        # Make it non-nullable
        op.alter_column('comment_feedback', 'code_hash', existing_type=sa.String(64), nullable=False)
    except Exception as e:
        print(f"Migration warning: {e}")


def downgrade():
    op.drop_column('comment_feedback', 'code_hash')


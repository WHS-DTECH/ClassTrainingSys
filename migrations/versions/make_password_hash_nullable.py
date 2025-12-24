
"""
Migration: Make password_hash nullable in users table
Revision ID: make_password_hash_nullable
Revises: e9c0c2e251cb
Create Date: 2025-12-24
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'make_password_hash_nullable'
down_revision = '6152ba9fa1f8'
branch_labels = None
depends_on = None

def upgrade():
    op.alter_column('users', 'password_hash',
        existing_type=sa.String(length=200),
        nullable=True)

def downgrade():
    op.alter_column('users', 'password_hash',
        existing_type=sa.String(length=200),
        nullable=False)

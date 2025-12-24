# Alembic identifiers
revision = 'add_description_to_lessons'
down_revision = 'e9c0c2e251cb'  # Use the actual previous migration's revision string
branch_labels = None
depends_on = None
"""
Add description column to lessons table
"""
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('lessons', sa.Column('description', sa.Text(), nullable=True))

def downgrade():
    op.drop_column('lessons', 'description')

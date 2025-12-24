"""merge heads

Revision ID: 9f8563ad22a6
Revises: add_description_to_lessons, ca_submissions_assignments
Create Date: 2025-12-25 00:01:15.999613

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9f8563ad22a6'
down_revision = ('add_description_to_lessons', 'ca_submissions_assignments')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass

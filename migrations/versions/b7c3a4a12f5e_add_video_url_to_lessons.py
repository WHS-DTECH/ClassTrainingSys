"""add video_url to lessons

Revision ID: b7c3a4a12f5e
Revises: 5764defa444a
Create Date: 2026-05-20 01:15:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b7c3a4a12f5e'
down_revision = '5764defa444a'
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    lesson_columns = {column['name'] for column in inspector.get_columns('lessons')}

    if 'video_url' not in lesson_columns:
        with op.batch_alter_table('lessons', schema=None) as batch_op:
            batch_op.add_column(sa.Column('video_url', sa.String(length=500), nullable=True))


def downgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    lesson_columns = {column['name'] for column in inspector.get_columns('lessons')}

    if 'video_url' in lesson_columns:
        with op.batch_alter_table('lessons', schema=None) as batch_op:
            batch_op.drop_column('video_url')

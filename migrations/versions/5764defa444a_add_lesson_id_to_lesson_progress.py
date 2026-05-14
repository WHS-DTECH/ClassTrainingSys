"""add lesson_id to lesson_progress

Revision ID: 5764defa444a
Revises: 98d9d256417d
Create Date: 2026-05-14 13:31:45.926335

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5764defa444a'
down_revision = '98d9d256417d'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('lesson_progress', schema=None) as batch_op:
        batch_op.add_column(sa.Column('lesson_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(
            'fk_lesson_progress_lesson_id_lessons',
            'lessons',
            ['lesson_id'],
            ['id']
        )


def downgrade():
    with op.batch_alter_table('lesson_progress', schema=None) as batch_op:
        batch_op.drop_constraint('fk_lesson_progress_lesson_id_lessons', type_='foreignkey')
        batch_op.drop_column('lesson_id')

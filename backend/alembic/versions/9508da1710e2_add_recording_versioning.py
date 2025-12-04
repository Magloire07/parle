"""add_recording_versioning

Revision ID: 9508da1710e2
Revises: 001
Create Date: 2025-12-04 22:41:45.425763

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9508da1710e2'
down_revision: Union[str, None] = '001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add parent_id and version columns to recordings table
    op.add_column('recordings', sa.Column('parent_id', sa.String(), nullable=True))
    op.add_column('recordings', sa.Column('version', sa.Integer(), nullable=False, server_default='1'))
    op.create_foreign_key('fk_recordings_parent_id', 'recordings', 'recordings', ['parent_id'], ['id'], ondelete='CASCADE')


def downgrade() -> None:
    # Remove the columns
    op.drop_constraint('fk_recordings_parent_id', 'recordings', type_='foreignkey')
    op.drop_column('recordings', 'version')
    op.drop_column('recordings', 'parent_id')

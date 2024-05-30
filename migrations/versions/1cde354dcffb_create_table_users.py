"""create_table_users

Revision ID: 1cde354dcffb
Revises: 77e8fcdd098f
Create Date: 2024-03-15 14:27:02.058090

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1cde354dcffb'
down_revision: Union[str, None] = '77e8fcdd098f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass

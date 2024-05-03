"""add field check worlplace_id

Revision ID: a193df8365ba
Revises: b1fc2cbcb335
Create Date: 2024-05-03 14:37:55.932071

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a193df8365ba'
down_revision: Union[str, None] = 'b1fc2cbcb335'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('checks', sa.Column('workplace_id', sa.Uuid(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('checks', 'workplace_id')
    # ### end Alembic commands ###

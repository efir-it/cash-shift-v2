"""[upd] client_id -> owner_id, add store_id

Revision ID: 78433ebd0902
Revises: 
Create Date: 2023-10-23 12:23:19.045719

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '78433ebd0902'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cash_shifts',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('organization_id', sa.Uuid(), nullable=False),
    sa.Column('store_id', sa.Uuid(), nullable=False),
    sa.Column('owner_id', sa.Uuid(), nullable=False),
    sa.Column('workplace_id', sa.Uuid(), nullable=False),
    sa.Column('worker_id', sa.Uuid(), nullable=False),
    sa.Column('cash_registr_id', sa.Uuid(), nullable=False),
    sa.Column('closed', sa.Boolean(), nullable=False),
    sa.Column('hide', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('events',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('status', sa.String(), nullable=False),
    sa.Column('queue', sa.String(), nullable=False),
    sa.Column('message', sa.String(), nullable=False),
    sa.Column('send_time', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('checks',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('owner_id', sa.Uuid(), nullable=False),
    sa.Column('organization_id', sa.Uuid(), nullable=False),
    sa.Column('store_id', sa.Uuid(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('number', sa.String(), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.Column('number_fiscal_document', sa.String(), nullable=False),
    sa.Column('reason_id', sa.Uuid(), nullable=True),
    sa.Column('cash_shift_id', sa.Uuid(), nullable=False),
    sa.Column('type_operation', sa.Integer(), nullable=False),
    sa.Column('type_payment', sa.Integer(), nullable=False),
    sa.Column('check_status', sa.Integer(), nullable=False),
    sa.Column('type_taxation', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['cash_shift_id'], ['cash_shifts.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('positions_check',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('product_id', sa.Uuid(), nullable=False),
    sa.Column('count', sa.Integer(), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('position', sa.Integer(), nullable=False),
    sa.Column('owner_id', sa.Uuid(), nullable=False),
    sa.Column('check_id', sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(['check_id'], ['checks.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('positions_check')
    op.drop_table('checks')
    op.drop_table('events')
    op.drop_table('cash_shifts')
    # ### end Alembic commands ###

"""empty message

Revision ID: 94544a372ce5
Revises: d0c3533f6a75
Create Date: 2023-11-02 16:27:38.426672

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '94544a372ce5'
down_revision: Union[str, None] = 'd0c3533f6a75'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('cities', 'name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.create_index(op.f('ix_cities_name'), 'cities', ['name'], unique=False)
    op.alter_column('states', 'name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.create_index(op.f('ix_states_name'), 'states', ['name'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_states_name'), table_name='states')
    op.alter_column('states', 'name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_index(op.f('ix_cities_name'), table_name='cities')
    op.alter_column('cities', 'name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###
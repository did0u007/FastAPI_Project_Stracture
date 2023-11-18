"""empty message

Revision ID: 327e654e2226
Revises: 
Create Date: 2023-11-03 10:44:34.576906

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '327e654e2226'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('images',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('url', sa.Unicode(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('states',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Unicode(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_states_name'), 'states', ['name'], unique=True)
    op.create_table('cities',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Unicode(), nullable=False),
    sa.Column('states_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['states_id'], ['states.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_cities_name'), 'cities', ['name'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Unicode(), nullable=True),
    sa.Column('username', sa.Unicode(), nullable=True),
    sa.Column('email', sa.Unicode(), nullable=True),
    sa.Column('password', sa.Unicode(), nullable=True),
    sa.Column('profile_img', sa.Integer(), nullable=True),
    sa.Column('remember_token', sa.Unicode(), nullable=True),
    sa.Column('user_type', sa.Enum('USER', 'ADMIN', 'SELLEER', name='usertype'), nullable=True),
    sa.Column('cities_id', sa.Integer(), nullable=True),
    sa.Column('states_id', sa.Integer(), nullable=True),
    sa.Column('address', sa.Unicode(), nullable=True),
    sa.Column('phone', sa.Unicode(), nullable=True),
    sa.Column('deleted_at', sa.Time(), nullable=True),
    sa.Column('created_at', sa.Time(), nullable=True),
    sa.Column('updated_at', sa.Time(), nullable=True),
    sa.ForeignKeyConstraint(['cities_id'], ['cities.id'], ),
    sa.ForeignKeyConstraint(['profile_img'], ['images.id'], ),
    sa.ForeignKeyConstraint(['states_id'], ['states.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_index(op.f('ix_cities_name'), table_name='cities')
    op.drop_table('cities')
    op.drop_index(op.f('ix_states_name'), table_name='states')
    op.drop_table('states')
    op.drop_table('images')
    # ### end Alembic commands ###

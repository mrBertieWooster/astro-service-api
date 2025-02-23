"""Add zodiacs and compatibilities tables

Revision ID: 62297580701b
Revises: f968c15a28d3
Create Date: 2025-02-08 23:20:43.040021

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '62297580701b'
down_revision: Union[str, None] = 'f968c15a28d3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('zodiacs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('element', sa.Enum('FIRE', 'WATER', 'EARTH', 'AIR', name='zodiacelement'), nullable=False),
    sa.Column('ruling_planet', sa.String(), nullable=False),
    sa.Column('quality', sa.Enum('CARDINAL', 'FIXED', 'MUTABLE', name='zodiacquality'), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_zodiacs_id'), 'zodiacs', ['id'], unique=False)
    op.create_table('compatibilities',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sign1_id', sa.Integer(), nullable=False),
    sa.Column('sign2_id', sa.Integer(), nullable=False),
    sa.Column('compatibility_percentage', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['sign1_id'], ['zodiacs.id'], ),
    sa.ForeignKeyConstraint(['sign2_id'], ['zodiacs.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_compatibilities_id'), 'compatibilities', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_compatibilities_id'), table_name='compatibilities')
    op.drop_table('compatibilities')
    op.drop_index(op.f('ix_zodiacs_id'), table_name='zodiacs')
    op.drop_table('zodiacs')
    # ### end Alembic commands ###

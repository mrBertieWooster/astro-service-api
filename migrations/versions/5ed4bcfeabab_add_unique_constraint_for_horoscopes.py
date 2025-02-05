"""Add unique constraint for horoscopes

Revision ID: 5ed4bcfeabab
Revises: cdf277b057da
Create Date: 2025-02-05 10:08:40.936098

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5ed4bcfeabab'
down_revision: Union[str, None] = 'cdf277b057da'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(
        'uq_horoscope_sign_type_date',  
        'horoscopes',                  
        ['sign', 'type', 'date']       
    )


def downgrade() -> None:
    op.drop_constraint('uq_horoscope_sign_type_date', 'horoscopes', type_='unique')

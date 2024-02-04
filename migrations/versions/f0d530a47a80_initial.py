"""initial

Revision ID: f0d530a47a80
Revises: 791fec0ba0da
Create Date: 2024-02-04 16:37:33.887894

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f0d530a47a80'
down_revision: Union[str, None] = '791fec0ba0da'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
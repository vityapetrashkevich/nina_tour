"""meta

Revision ID: ece7317e6f52
Revises: 61bf3cb96dcb
Create Date: 2026-03-11 19:09:30.954439

"""
from typing import Sequence, Union
import sqlmodel
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ece7317e6f52'
down_revision: Union[str, Sequence[str], None] = '61bf3cb96dcb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

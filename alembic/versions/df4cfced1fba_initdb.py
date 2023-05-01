"""InitDb

Revision ID: df4cfced1fba
Revises:
Create Date: 2023-05-01 17:05:25.131043

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "df4cfced1fba"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('point_of_interests',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('location', sa.String(), nullable=False, unique=True)
    )



def downgrade() -> None:
    op.drop_table('point_of_interests')

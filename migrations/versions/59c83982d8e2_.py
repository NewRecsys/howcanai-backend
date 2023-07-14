"""empty message

Revision ID: 59c83982d8e2
Revises: a3cf940691b1
Create Date: 2023-07-14 10:45:05.933406

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '59c83982d8e2'
down_revision = 'a3cf940691b1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('qna', 'user_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('qna', sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###

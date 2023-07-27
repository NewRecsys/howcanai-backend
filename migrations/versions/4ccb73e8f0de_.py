"""empty message

Revision ID: 4ccb73e8f0de
Revises: 
Create Date: 2023-07-27 02:51:02.856659

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4ccb73e8f0de'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'chatroom', ['id'])
    op.add_column('qna', sa.Column('nexts', sa.ARRAY(sa.Text()), nullable=True))
    op.create_unique_constraint(None, 'qna', ['id'])
    op.create_unique_constraint(None, 'user', ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='unique')
    op.drop_constraint(None, 'qna', type_='unique')
    op.drop_column('qna', 'nexts')
    op.drop_constraint(None, 'chatroom', type_='unique')
    # ### end Alembic commands ###
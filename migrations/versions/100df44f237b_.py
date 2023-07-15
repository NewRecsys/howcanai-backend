"""empty message

Revision ID: 100df44f237b
Revises: 17c53b499a7e
Create Date: 2023-07-15 10:09:08.568522

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '100df44f237b'
down_revision = '17c53b499a7e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('chatroom', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'chatroom', 'user', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'chatroom', type_='foreignkey')
    op.drop_column('chatroom', 'user_id')
    # ### end Alembic commands ###

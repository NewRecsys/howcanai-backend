"""empty message

Revision ID: 41d008b7b427
Revises: 439d7f66acff
Create Date: 2023-07-18 22:10:33.132203

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '41d008b7b427'
down_revision = '439d7f66acff'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('email', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('chatroom',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('create_date', sa.DateTime(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('qna',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('question', sa.String(), nullable=False),
    sa.Column('answer', sa.String(), nullable=False),
    sa.Column('references', sa.ARRAY(sa.Text()), nullable=False),
    sa.Column('create_date', sa.DateTime(), nullable=False),
    sa.Column('chatroom_id', sa.UUID(), nullable=True),
    sa.Column('user_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['chatroom_id'], ['chatroom.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('qna')
    op.drop_table('chatroom')
    op.drop_table('user')
    # ### end Alembic commands ###
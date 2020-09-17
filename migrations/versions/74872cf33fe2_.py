"""empty message

Revision ID: 74872cf33fe2
Revises: 987838667228
Create Date: 2020-09-16 16:55:26.002422

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '74872cf33fe2'
down_revision = '987838667228'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('social_auth',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('social_id', sa.String(length=230), nullable=False),
    sa.Column('provider_id', sa.Integer(), nullable=False),
    sa.Column('provider_name', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('social_id')
    )
    op.create_table('traditional_auth',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('email', sa.String(length=256), nullable=False),
    sa.Column('password', sa.String(length=256), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.String(length=230), nullable=False),
    sa.Column('name', sa.String(length=240), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_table('traditional_auth')
    op.drop_table('social_auth')
    # ### end Alembic commands ###
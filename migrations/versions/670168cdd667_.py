"""empty message

Revision ID: 670168cdd667
Revises: 
Create Date: 2016-12-01 15:19:07.777654

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '670168cdd667'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('roles', sa.Column('password_hash', sa.String(length=128), nullable=True))
    op.add_column('users', sa.Column('email', sa.String(length=64), nullable=True))
    op.add_column('users', sa.Column('password_hash', sa.String(length=128), nullable=True))
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_column('users', 'password_hash')
    op.drop_column('users', 'email')
    op.drop_column('roles', 'password_hash')
    ### end Alembic commands ###
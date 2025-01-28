"""empty message

Revision ID: 5faf250cd3e4
Revises: 
Create Date: 2025-01-28 15:23:31.539561

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5faf250cd3e4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('profile_picture', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('profile_picture')

    # ### end Alembic commands ###

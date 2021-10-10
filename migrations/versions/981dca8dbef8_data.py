"""data

Revision ID: 981dca8dbef8
Revises: 
Create Date: 2021-10-10 16:32:29.896299

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '981dca8dbef8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('datas',
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('temp', sa.Float(), nullable=True),
    sa.Column('humidity', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('timestamp')
    )
    with op.batch_alter_table('datas', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_datas_timestamp'), ['timestamp'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('datas', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_datas_timestamp'))

    op.drop_table('datas')
    # ### end Alembic commands ###

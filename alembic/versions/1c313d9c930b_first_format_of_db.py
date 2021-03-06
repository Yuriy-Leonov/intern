"""first format of DB

Revision ID: 1c313d9c930b
Revises: None
Create Date: 2013-09-12 15:52:52.444494

"""

# revision identifiers, used by Alembic.
revision = '1c313d9c930b'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('vm',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('status', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('addresses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ip', sa.String(length=128), nullable=True),
    sa.Column('mac', sa.String(length=128), nullable=True),
    sa.Column('allocate', sa.Integer(), nullable=True),
    sa.Column('vm_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['vm_id'], ['vm.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('addresses')
    op.drop_table('vm')
    ### end Alembic commands ###

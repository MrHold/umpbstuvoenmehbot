"""init

Revision ID: xxxx_init
Revises: 
Create Date: 2024-01-01 12:00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'xxxx_init'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('telegram_id', sa.BigInteger(), nullable=False, unique=True),
        sa.Column('is_admin', sa.Boolean(), default=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('username', sa.String(255))
    )

    op.create_table('extracurricular_events',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('message', sa.Text(), nullable=False)
    )

    op.create_table('meros',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('date', sa.DateTime(), nullable=False),
        sa.Column('location', sa.String(255)),
        sa.Column('description', sa.Text()),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('category', sa.String(255), nullable=False)
    )

    op.create_table('feedback',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('telegram_id', sa.BigInteger(), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('username', sa.String(255)),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('type', sa.String(255), nullable=False),
        sa.Column('contact', sa.String(255))
    )

def downgrade():
    op.drop_table('meros')
    op.drop_table('extracurricular_events')
    op.drop_table('users')
    op.drop_table('feedback')

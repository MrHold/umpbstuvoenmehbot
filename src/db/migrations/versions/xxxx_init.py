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
        sa.Column('is_subscribed_for_events', sa.Boolean(), default=True),
        sa.Column('is_admin', sa.Boolean(), default=False)
    )

    op.create_table('organizations',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('contacts', sa.Text()),
        sa.Column('direction', sa.String(255))
    )

    op.create_table('extracurricular_events',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('date', sa.DateTime(), nullable=False),
        sa.Column('location', sa.String(255)),
        sa.Column('description', sa.Text()),
        sa.Column('is_active', sa.Boolean(), default=True)
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

def downgrade():
    op.drop_table('meros')
    op.drop_table('extracurricular_events')
    op.drop_table('organizations')
    op.drop_table('users')

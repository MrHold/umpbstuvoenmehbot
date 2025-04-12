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

    # op.create_table('groups',
    #     sa.Column('id', sa.Integer(), primary_key=True),
    #     sa.Column('external_id', sa.String(), nullable=False, unique=True),
    #     sa.Column('name', sa.String(255), nullable=False),
    #     sa.Column('schedules', sa.relationship('Schedule', back_populates='group'))
    # )

    op.create_table('schedules',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('group_id', sa.Integer(), nullable=False),
        sa.Column('parity', sa.String(15), nullable=False),
        sa.Column('day_of_week', sa.String(15), nullable=False),
        sa.Column('start_time', sa.Time(), nullable=False),
        sa.Column('room', sa.String(20), nullable=False),
        sa.Column('subject', sa.String(255), nullable=False),
        sa.Column('teacher', sa.String(100), nullable=False),
    )
    op.create_table('groups',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('group_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(15), nullable=False),
    )

def downgrade():
    op.drop_table('meros')
    op.drop_table('extracurricular_events')
    op.drop_table('users')
    op.drop_table('feedback')
    op.drop_table('schedules')
    op.drop_table('groups')

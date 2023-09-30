"""Add a column

Revision ID: e955d24513bb
Revises: 985dd6888b94
Create Date: 2023-09-29 14:09:50.534651

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e955d24513bb'
down_revision = '985dd6888b94'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_constraint('user_history_user_id_fkey', 'user_history', type_='foreignkey')
    op.create_foreign_key(None, 'user_history', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    op.add_column('users', sa.Column('first_name', sa.String(length=255), nullable=False))
    op.add_column('users', sa.Column('second_name', sa.String(length=255), nullable=False))
    op.add_column('users', sa.Column('is_active', sa.Boolean(), nullable=False))


def downgrade() -> None:
    op.drop_column('users', 'is_active')
    op.drop_column('users', 'second_name')
    op.drop_column('users', 'first_name')
    op.drop_constraint(None, 'user_history', type_='foreignkey')
    op.create_foreign_key('user_history_user_id_fkey', 'user_history', 'users', ['user_id'], ['id'])

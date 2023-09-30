"""init

Revision ID: f52601837612
Revises: 
Create Date: 2023-09-30 16:40:10.806136

"""
import uuid

from alembic import op
import sqlalchemy as sa

from models.entities import Role, RoleName

# revision identifiers, used by Alembic.
revision = 'f52601837612'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('roles',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('name', sa.Enum('ADMIN', 'REGISTERED', 'TEST', name='rolename'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('users',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('social_account',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('user_id', sa.Uuid(), nullable=False),
    sa.Column('social_id', sa.String(), nullable=False),
    sa.Column('social_name', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('social_id', 'social_name', name='social_pk')
    )
    op.create_table('user_history',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('user_id', sa.Uuid(), nullable=False),
    sa.Column('last_login_datetime', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('device', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users_roles',
    sa.Column('users_id', sa.Uuid(), nullable=False),
    sa.Column('roles_id', sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(['roles_id'], ['roles.id'], ),
    sa.ForeignKeyConstraint(['users_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('users_id', 'roles_id')
    )
    op.bulk_insert(
        Role.__table__,
        [
            {"id": uuid.uuid4(), "name": RoleName.ADMIN},
            {"id": uuid.uuid4(), "name": RoleName.REGISTERED},
        ],
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users_roles')
    op.drop_table('user_history')
    op.drop_table('social_account')
    op.drop_table('users')
    op.drop_table('roles')
    # ### end Alembic commands ###
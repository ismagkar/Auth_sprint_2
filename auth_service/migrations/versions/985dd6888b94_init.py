"""init

Revision ID: 985dd6888b94
Revises:
Create Date: 2023-08-06 23:26:00.315295

"""
import uuid

import sqlalchemy as sa
from alembic import op

from src.models.entities import Role, RoleName

revision = "985dd6888b94"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "roles",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.Enum("ADMIN", "REGISTERED", name="rolename"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "users",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password", sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_table(
        "user_history",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column(
            "last_login_datetime",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("device", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "users_roles",
        sa.Column("users_id", sa.Uuid(), nullable=False),
        sa.Column("roles_id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(
            ["roles_id"],
            ["roles.id"],
        ),
        sa.ForeignKeyConstraint(
            ["users_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("users_id", "roles_id"),
    )
    op.bulk_insert(
        Role.__table__,
        [
            {"id": uuid.uuid4(), "name": RoleName.ADMIN},
            {"id": uuid.uuid4(), "name": RoleName.REGISTERED},
        ],
    )


def downgrade() -> None:
    op.drop_table("users_roles")
    op.drop_table("user_history")
    op.drop_table("users")
    op.drop_table("roles")

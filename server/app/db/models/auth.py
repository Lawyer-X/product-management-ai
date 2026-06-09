from sqlalchemy import Column, Table
from sqlalchemy.dialects.postgresql import UUID

from app.db.base import Base

# Stub for Supabase's `auth.users` table. Supabase owns and manages this table
# (rows are created when users sign in via the GitHub OAuth integration), so we
# never create or migrate it. We declare just enough of it here for foreign keys
# like `workspaces.user_id` to resolve during autogenerate. env.py's
# `include_object` hook keeps Alembic from emitting CREATE/DROP for it.
auth_users = Table(
    "users",
    Base.metadata,
    Column("id", UUID, primary_key=True),
    schema="auth",
)

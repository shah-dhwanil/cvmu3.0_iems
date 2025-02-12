from uuid import UUID
from typing import Optional

from asyncpg import UniqueViolationError
from iems.base.postgres import PGConnection
from argon2 import PasswordHasher
from uuid_utils import uuid7

from iems.users.exceptions import UsernameAlreadyExistsException
from iems.users.schemas import (
    CreateUserRequest,
    GetUserResponse,
    UpdateUserRoleRequest,
    UpdateUserPasswordRequest,
    RoleEnum,
)


class UserRepository:
    @staticmethod
    async def create_user(create_user: CreateUserRequest) -> UUID:
        ph = PasswordHasher()
        create_user.password = ph.hash(create_user.password)
        user_id = uuid7()
        async with PGConnection.get_connection() as conn:
            try:
                await conn.execute(
                    """
                    INSERT INTO users (id, username, password, role, active)
                    VALUES ($1, $2, $3, $4, $5);
                    """,
                    str(user_id),
                    create_user.username,
                    create_user.password.encode("UTF-8"),
                    create_user.role,
                    create_user.active,
                )
            except UniqueViolationError:
                raise UsernameAlreadyExistsException()
            return user_id

    # Rest of the methods remain unchanged
    @staticmethod
    async def get_user(user_id: UUID) -> Optional[GetUserResponse]:
        async with PGConnection.get_connection() as conn:
            row = await conn.fetchrow(
                """
                SELECT id, username, role, active
                FROM users
                WHERE id = $1;
                """,
                user_id,
            )
            if row:
                return GetUserResponse(
                    id=str(row["id"]),
                    username=row["username"],
                    role=RoleEnum(row["role"]),
                    active=row["active"],
                )
            return None

    @staticmethod
    async def update_user_role(
        user_id: UUID, update_role: UpdateUserRoleRequest
    ) -> bool:
        async with PGConnection.get_connection() as conn:
            result = await conn.execute(
                """
                UPDATE users
                SET role = $1
                WHERE id = $2;
                """,
                update_role.role,
                user_id,
            )
            return result == "UPDATE 1"

    @staticmethod
    async def update_user_password(
        user_id: UUID, update_password: UpdateUserPasswordRequest
    ) -> bool:
        ph = PasswordHasher()
        update_password.password = ph.hash(update_password.password)
        async with PGConnection.get_connection() as conn:
            result = await conn.execute(
                """
                UPDATE users
                SET password = $1
                WHERE id = $2;
                """,
                update_password.password,  # Note: Password should be hashed before storage
                user_id,
            )
            return result == "UPDATE 1"

    @staticmethod
    async def delete_user(user_id: UUID) -> bool:
        async with PGConnection.get_connection() as conn:
            result = await conn.execute(
                """
                UPDATE users
                SET active = false
                WHERE id = $1;
                """,
                user_id,
            )
            return result == "UPDATE 1"

    @staticmethod
    async def get_user_by_username(username: str) -> Optional[GetUserResponse]:
        async with PGConnection.get_connection() as conn:
            row = await conn.fetchrow(
                """
                SELECT id, username, role, active
                FROM users
                WHERE username = $1;
                """,
                username,
            )
            if row:
                return GetUserResponse(
                    id=row["id"],
                    username=row["username"],
                    role=RoleEnum(row["role"]),
                    active=row["active"],
                )
            return None

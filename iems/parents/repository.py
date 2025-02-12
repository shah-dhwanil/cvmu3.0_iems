from uuid import UUID
from typing import Optional
from asyncpg import ForeignKeyViolationError, UniqueViolationError
from iems.base.postgres import PGConnection
from iems.parents.exceptions import ParentAlreadyExistsError

from iems.parents.schemas import (
    CreateParentRequest,
    GetParentResponse,
    UpdateParentRequest,
)
from iems.users.exceptions import UserNotFoundException


class ParentRepository:
    @staticmethod
    async def create_parent(create_parent: CreateParentRequest) -> UUID:
        async with PGConnection.get_connection() as conn:
            try:
                await conn.execute(
                    """
                    INSERT INTO parents (
                        id, student_id, father_name, mother_name,
                        contact_no, email_id
                    )
                    VALUES ($1, $2, $3, $4, $5, $6);
                    """,
                    create_parent.id,
                    create_parent.student_id,
                    create_parent.father_name,
                    create_parent.mother_name,
                    create_parent.contact_no,
                    create_parent.email_id,
                )
                return create_parent.id
            except UniqueViolationError:
                raise ParentAlreadyExistsError()
            except ForeignKeyViolationError:
                raise UserNotFoundException()

    @staticmethod
    async def get_parent(parent_id: UUID) -> Optional[GetParentResponse]:
        async with PGConnection.get_connection() as conn:
            row = await conn.fetchrow(
                """
                SELECT id, student_id, father_name, mother_name,
                       contact_no, email_id, active
                FROM parents
                WHERE id = $1;
                """,
                parent_id,
            )
            if row:
                return GetParentResponse(
                    id=str(row["id"]),
                    student_id=str(row["student_id"]),
                    father_name=row["father_name"],
                    mother_name=row["mother_name"],
                    contact_no=row["contact_no"],
                    email_id=row["email_id"],
                    active=row["active"],
                )
            return None

    @staticmethod
    async def get_parent_by_student(student_id: UUID) -> Optional[GetParentResponse]:
        async with PGConnection.get_connection() as conn:
            row = await conn.fetchrow(
                """
                SELECT id, student_id, father_name, mother_name,
                       contact_no, email_id, active
                FROM parents
                WHERE student_id = $1;
                """,
                student_id,
            )
            if row:
                return GetParentResponse(
                    id=str(row["id"]),
                    student_id=str(row["student_id"]),
                    father_name=row["father_name"],
                    mother_name=row["mother_name"],
                    contact_no=row["contact_no"],
                    email_id=row["email_id"],
                    active=row["active"],
                )
            return None

    @staticmethod
    async def update_parent(
        parent_id: UUID, update_parent: UpdateParentRequest
    ) -> bool:
        async with PGConnection.get_connection() as conn:
            try:
                result = await conn.execute(
                    """
                    UPDATE parents 
                    SET father_name = $1,
                        mother_name = $2,
                        contact_no = $3,
                        email_id = $4
                    WHERE id = $5;
                    """,
                    update_parent.father_name,
                    update_parent.mother_name,
                    update_parent.contact_no,
                    update_parent.email_id,
                    parent_id,
                )
                return result == "UPDATE 1"
            except UniqueViolationError:
                raise ParentAlreadyExistsError()

    @staticmethod
    async def delete_parent(parent_id: UUID) -> bool:
        async with PGConnection.get_connection() as conn:
            result = await conn.execute(
                """
                UPDATE parents
                SET active = false
                WHERE id = $1;
                """,
                parent_id,
            )
            return result == "UPDATE 1"

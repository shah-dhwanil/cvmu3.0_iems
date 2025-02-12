from uuid import UUID
from typing import Optional, List
from iems.base.postgres import PGConnection
from uuid_utils import uuid7

from iems.subjects.schemas import (
    CreateSubjectRequest,
    GetSubjectResponse,
    UpdateSubjectRequest,
)


class SubjectRepository:
    @staticmethod
    async def create_subject(create_subject: CreateSubjectRequest) -> UUID:
        subject_id = uuid7()
        async with PGConnection.get_connection() as conn:
            await conn.execute(
                """
                INSERT INTO subjects (id, code, name, credits)
                VALUES ($1, $2, $3, $4);
                """,
                str(subject_id),
                create_subject.code,
                create_subject.name,
                create_subject.credits,
            )
            return str(subject_id)

    @staticmethod
    async def get_subject(subject_id: UUID) -> Optional[GetSubjectResponse]:
        async with PGConnection.get_connection() as conn:
            row = await conn.fetchrow(
                """
                SELECT id, code, name, credits
                FROM subjects
                WHERE id = $1;
                """,
                subject_id,
            )
            if row:
                return GetSubjectResponse(
                    id=str(row["id"]),
                    code=row["code"],
                    name=row["name"],
                    credits=row["credits"],
                )
            return None

    @staticmethod
    async def get_all_subjects() -> List[GetSubjectResponse]:
        async with PGConnection.get_connection() as conn:
            rows = await conn.fetch(
                """
                SELECT id, code, name, credits
                FROM subjects;
                """
            )
            return [
                GetSubjectResponse(
                    id=str(row["id"]),
                    code=row["code"],
                    name=row["name"],
                    credits=row["credits"],
                )
                for row in rows
            ]

    @staticmethod
    async def update_subject(
        subject_id: UUID, update_subject: UpdateSubjectRequest
    ) -> bool:
        async with PGConnection.get_connection() as conn:
            result = await conn.execute(
                """
                UPDATE subjects
                SET code = $1, name = $2, credits = $3
                WHERE id = $4;
                """,
                update_subject.code,
                update_subject.name,
                update_subject.credits,
                subject_id,
            )
            return result == "UPDATE 1"

    @staticmethod
    async def delete_subject(subject_id: UUID) -> bool:
        async with PGConnection.get_connection() as conn:
            result = await conn.execute(
                """
                UPDATE subjects
                SET active = false
                WHERE id = $1;
                """,
                subject_id,
            )
            return result == "UPDATE 1"

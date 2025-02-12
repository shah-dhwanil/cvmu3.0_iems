from uuid import UUID
from typing import Optional
from asyncpg import ForeignKeyViolationError
from iems.base.postgres import PGConnection
from uuid_utils import uuid7

from iems.batch.exceptions import BatchNotFoundError
from iems.semister.schemas import (
    CreateSemisterRequest,
    GetSemisterResponse,
    UpdateSemisterRequest,
)


class SemisterRepository:
    @staticmethod
    async def create_semister(create_semister: CreateSemisterRequest) -> UUID:
        semister_id = uuid7()
        async with PGConnection.get_connection() as conn:
            try:
                await conn.execute(
                    """
                    INSERT INTO semister (id, batch_id, sem_no, ongoing)
                    VALUES ($1, $2, $3, $4);
                    """,
                    str(semister_id),
                    create_semister.batch_id,
                    create_semister.sem_no,
                    create_semister.ongoing,
                )
                return str(semister_id)
            except ForeignKeyViolationError:
                raise BatchNotFoundError()

    @staticmethod
    async def get_semister(semister_id: UUID) -> Optional[GetSemisterResponse]:
        async with PGConnection.get_connection() as conn:
            row = await conn.fetchrow(
                """
                SELECT id, batch_id, sem_no, ongoing, active
                FROM semister
                WHERE id = $1;
                """,
                semister_id,
            )
            if row:
                return GetSemisterResponse(
                    id=str(row["id"]),
                    batch_id=str(row["batch_id"]),
                    sem_no=row["sem_no"],
                    ongoing=row["ongoing"],
                )
            return None
    
    

    @staticmethod
    async def get_semister_by_branch(branch_id: UUID) -> list[GetSemisterResponse]:
        async with PGConnection.get_connection() as conn:
            rows = await conn.fetch(
                """
                SELECT id, batch_id, sem_no, ongoing, active
                FROM semister
                WHERE batch_id = $1;
                """,
                branch_id,
            )
            return[GetSemisterResponse(
                    id=str(row["id"]),
                    batch_id=str(row["batch_id"]),
                    sem_no=row["sem_no"],
                    ongoing=row["ongoing"],
                ) for row in rows]

    @staticmethod
    async def update_semister(
        semister_id: UUID, update_semister: UpdateSemisterRequest
    ) -> bool:
        async with PGConnection.get_connection() as conn:
            result = await conn.execute(
                """
                UPDATE semister
                SET batch_id = $1,
                    sem_no = $2,
                    ongoing = $3
                WHERE id = $4;
                """,
                update_semister.batch_id,
                update_semister.sem_no,
                update_semister.ongoing,
                semister_id,
            )
            return result == "UPDATE 1"

    @staticmethod
    async def delete_semister(semister_id: UUID) -> bool:
        async with PGConnection.get_connection() as conn:
            result = await conn.execute(
                """
                UPDATE semister
                SET active = false
                WHERE id = $1;
                """,
                semister_id,
            )
            return result == "UPDATE 1"

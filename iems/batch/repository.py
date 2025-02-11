from uuid import UUID
from typing import Optional
from asyncpg import ForeignKeyViolationError
from iems.base.postgres import PGConnection
from uuid_utils import uuid7

from iems.batch.schemas import (
    CreateBatchRequest,
    GetBatchResponse,
    UpdateBatchRequest,
)
from iems.staffs.exceptions import StaffNotFoundError


class BatchRepository:
    @staticmethod
    async def create_batch(create_batch: CreateBatchRequest) -> UUID:
        batch_id = uuid7()
        async with PGConnection.get_connection() as conn:
            try:
                await conn.execute(
                    """
                    INSERT INTO batch (id, branch, year, hod_id, counciller_id)
                    VALUES ($1, $2, $3, $4, $5);
                    """,
                    str(batch_id),
                    create_batch.branch,
                    create_batch.year,
                    create_batch.hod_id,
                    create_batch.counciller_id,
                )
                return batch_id
            except ForeignKeyViolationError:
                raise StaffNotFoundError()

    @staticmethod
    async def create_batch_all(year: int, branch: str) -> UUID:
        batch_id = uuid7()
        async with PGConnection.get_connection() as conn:
            try:
                await conn.execute(
                    """
                    INSERT INTO batch (id, branch, year, hod_id, counciller_id)
                    VALUES ($1, $2, $3, (SELECT hod_id FROM batch WHERE branch = $2 AND year = $3 - 1),
                    (SELECT counciller_id FROM batch WHERE branch = $2 AND year = $3 - 1));
                    ,
                    """,
                    batch_id,
                    branch,
                    year,
                )
                return batch_id
            except ForeignKeyViolationError:
                raise StaffNotFoundError()

    @staticmethod
    async def get_batch(batch_id: UUID) -> Optional[GetBatchResponse]:
        async with PGConnection.get_connection() as conn:
            row = await conn.fetchrow(
                """
                SELECT id, branch, year, hod_id, counciller_id, active, created_at
                FROM batch
                WHERE id = $1;
                """,
                batch_id,
            )
            if row:
                return GetBatchResponse(
                    id=row["id"],
                    branch=row["branch"],
                    year=row["year"],
                    hod_id=row["hod_id"],
                    counciller_id=row["counciller_id"],
                    active=row["active"],
                    created_at=row["created_at"],
                )
            return None

    @staticmethod
    async def update_batch(batch_id: UUID, update_batch: UpdateBatchRequest) -> bool:
        async with PGConnection.get_connection() as conn:
            result = await conn.execute(
                """
                UPDATE batch
                SET branch = $1,
                    year = $2,
                    hod_id = $3,
                    counciller_id = $4,
                WHERE id = $5;
                """,
                update_batch.branch,
                update_batch.year,
                update_batch.hod_id,
                update_batch.counciller_id,
                batch_id,
            )
            return result == "UPDATE 1"

    @staticmethod
    async def delete_batch(batch_id: UUID) -> bool:
        async with PGConnection.get_connection() as conn:
            result = await conn.execute(
                """
                UPDATE batch
                SET active = false
                WHERE id = $1;
                """,
                batch_id,
            )
            return result == "UPDATE 1"

    @staticmethod
    async def get_batch_by_branch_and_year(
        branch: str, year: int
    ) -> Optional[GetBatchResponse]:
        async with PGConnection.get_connection() as conn:
            row = await conn.fetchrow(
                """
                SELECT id, branch, year, hod_id, counciller_id, active, created_at
                FROM batch
                WHERE branch = $1 AND year = $2;
                """,
                branch,
                year,
            )
            if row:
                return GetBatchResponse(
                    id=row["id"],
                    branch=row["branch"],
                    year=row["year"],
                    hod_id=row["hod_id"],
                    counciller_id=row["counciller_id"],
                    active=row["active"],
                    created_at=row["created_at"],
                )
            return None

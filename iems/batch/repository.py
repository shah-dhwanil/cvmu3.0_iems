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
                key = f"{create_batch.branch.split(",")[1]}_{create_batch.year}"
                res = await conn.execute(f"CREATE SEQUENCE {key};")
                print(res)
                return str(batch_id)
            except ForeignKeyViolationError:
                raise StaffNotFoundError()

    @staticmethod
    async def create_batch_all(year: int, branch: str) -> UUID:
        batch_id = uuid7()
        async with PGConnection.get_connection() as conn:
            try:
                hod_id = await conn.fetchval(
                    """
                    SELECT hod_id FROM batch WHERE branch = $1 AND year = $2 - 1;
                    """,
                    branch,
                    year,
                )
                counciller_id = await conn.fetchval(
                    """
                    SELECT counciller_id FROM batch WHERE branch = $1 AND year = $2 - 1;
                    """,
                    branch,
                    year,
                )
                if hod_id is None or counciller_id is None:
                    return
                await conn.execute(
                    """
                    INSERT INTO batch (id, branch, year, hod_id, counciller_id)
                    VALUES ($1, $2, $3,$4,$5);
                    """,
                    str(batch_id),
                    branch,
                    year,
                    str(hod_id),
                    str(counciller_id),
                )
                return str(batch_id)
            except ForeignKeyViolationError:
                raise StaffNotFoundError()

    @staticmethod
    async def get_batch(batch_id: UUID) -> Optional[GetBatchResponse]:
        async with PGConnection.get_connection() as conn:
            row = await conn.fetchrow(
                """
                SELECT id, branch, year, hod_id, counciller_id
                FROM batch
                WHERE id = $1;
                """,
                batch_id,
            )
            if row:
                return GetBatchResponse(
                    id=str(row["id"]),
                    branch=row["branch"],
                    year=row["year"],
                    hod_id=str(row["hod_id"]),
                    counciller_id=str(row["counciller_id"]),
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
                SELECT id, branch, year, hod_id, counciller_id
                FROM batch
                WHERE branch = $1 AND year = $2;
                """,
                branch,
                year,
            )
            if row:
                return GetBatchResponse(
                    id=str(row["id"]),
                    branch=row["branch"],
                    year=row["year"],
                    hod_id=str(row["hod_id"]),
                    counciller_id=str(row["counciller_id"])
                )
            return None
    @staticmethod
    async def get_batch_year(
        year: int
    ) -> Optional[GetBatchResponse]:
        async with PGConnection.get_connection() as conn:
            rows = await conn.fetch(
                """
                SELECT id, branch, year, hod_id, counciller_id
                FROM batch
                WHERE year = $1;
                """,
                year,
            )
            return [GetBatchResponse(
                    id=str(row["id"]),
                    branch=row["branch"],
                    year=row["year"],
                    hod_id=str(row["hod_id"]),
                    counciller_id=str(row["counciller_id"]),
                ) for row in rows]
            
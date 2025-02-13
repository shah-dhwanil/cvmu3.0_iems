from uuid import UUID
from typing import Optional
from iems.base.postgres import PGConnection
from uuid_utils import uuid7

from iems.notices.schemas import (
    CreateNoticeRequest,
    CreateNoticeResponse,
    GetNoticeResponse,
    GetNoticesResponse,
    UpdateNoticeRequest
)


class NoticeRepository:
    @staticmethod
    async def create_notice(create_notice: CreateNoticeRequest) -> CreateNoticeResponse:
        notice_id = uuid7()
        async with PGConnection.get_connection() as conn:
            await conn.execute(
                """
                INSERT INTO notices (id, created_by, title, description, target_audience,batch_id, docs_id)
                VALUES ($1, $2, $3, $4, $5, $6,$7);
                """,
                str(notice_id),
                create_notice.created_by,
                create_notice.title,
                create_notice.description,
                create_notice.target_audience,
                create_notice.batch_id,
                create_notice.docs_id,
            )
            return CreateNoticeResponse(id=str(notice_id))

    @staticmethod
    async def get_notice(notice_id: UUID) -> Optional[GetNoticeResponse]:
        async with PGConnection.get_connection() as conn:
            row = await conn.fetchrow(
                """
                SELECT id, created_by, title, description, target_audience, docs_id, batch_id, created_at
                FROM notices
                WHERE id = $1;
                """,
                notice_id,
            )
            if row:
                return GetNoticeResponse(
                    id=str(row["id"]),
                    created_by=str(row["created_by"]),
                    title=row["title"],
                    description=row["description"],
                    target_audience=row["target_audience"],
                    batch_id=str(row["batch_id"]) if row["batch_id"] != None else None,
                    docs_id=str(row["docs_id"]) if row["docs_id"] != None else None,
                )
            return None

    @staticmethod
    async def get_notices() -> GetNoticesResponse:
        async with PGConnection.get_connection() as conn:
            rows = await conn.fetch(
                """
                SELECT id, created_by, title, description, target_audience, docs_id,batch_id, created_at
                FROM notices
                ORDER BY created_at DESC;
                """
            )
            notices = [
                GetNoticeResponse(
                    id=str(row["id"]),
                    created_by=str(row["created_by"]),
                    title=row["title"],
                    description=row["description"],
                    target_audience=row["target_audience"],
                    batch_id=str(row["batch_id"])if row["batch_id"] != None else None,
                    docs_id=str(row["docs_id"])if row["docs_id"] != None else None
                )
                for row in rows
            ]
            return GetNoticesResponse(notices=notices)

    @staticmethod
    async def get_notices_by_target_audience_and_batch_id(target_audience: str, batch_id: Optional[UUID]) -> GetNoticesResponse:
        async with PGConnection.get_connection() as conn:
            rows = await conn.fetch(
                """
                SELECT id, created_by, title, description, target_audience, docs_id, batch_id, created_at
                FROM notices
                WHERE target_audience = $1 AND batch_id = $2
                ORDER BY created_at DESC;
                """,
                target_audience,
                batch_id,
            )
            notices = [
                GetNoticeResponse(
                    id=str(row["id"]),
                    created_by=str(row["created_by"]),
                    title=row["title"],
                    description=row["description"],
                    target_audience=row["target_audience"],
                    batch_id=str(row["batch_id"]) if row["batch_id"] != None else None,
                    docs_id=str(row["docs_id"]) if row["docs_id"] != None else None
                )
                for row in rows
            ]
            return notices

    @staticmethod
    async def update_notice(
        notice_id: UUID, update_notice: UpdateNoticeRequest
    ) -> bool:
        async with PGConnection.get_connection() as conn:
            result = await conn.execute(
                """
                UPDATE notices
                SET title = $1, description = $2, target_audience = $3, docs_id = $4,batch_id=$5
                WHERE id = $6;
                """,
                update_notice.title,
                update_notice.description,
                update_notice.target_audience,
                update_notice.docs_id,
                update_notice.batch_id,
                notice_id,
            )
            return result == "UPDATE 1"

    @staticmethod
    async def delete_notice(notice_id: UUID) -> bool:
        async with PGConnection.get_connection() as conn:
            result = await conn.execute(
                """
                DELETE FROM notices
                WHERE id = $1;
                """,
                notice_id,
            )
            return result == "DELETE 1"
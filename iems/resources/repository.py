from uuid import UUID
from typing import Optional
from datetime import datetime, timezone
from iems.base.postgres import PGConnection

from iems.resources.schemas import (
    CreateResourceRequest,
    GetResourceBySubject,
    GetResourceResponse,
    UpdateResourceRequest,
    ResourceTypeEnum,
)


class ResourceRepository:
    @staticmethod
    async def create_resource(create_resource: CreateResourceRequest) -> UUID:
        async with PGConnection.get_connection() as conn:
            resource_id = await conn.fetchval(
                """
                INSERT INTO resources (subject_id, title, shared_at, shared_by, type, docs_id)
                VALUES ($1, $2, $3, $4, $5, $6)
                RETURNING id;
                """,
                create_resource.subject_id,
                create_resource.title,
                datetime.now(timezone.utc),
                create_resource.shared_by,
                create_resource.type,
                create_resource.docs_id,
            )
            return str(resource_id)

    @staticmethod
    async def get_resource(resource_id: UUID) -> Optional[GetResourceResponse]:
        async with PGConnection.get_connection() as conn:
            row = await conn.fetchrow(
                """
                SELECT id, subject_id, title, shared_at, shared_by, type, docs_id
                FROM resources
                WHERE id = $1;
                """,
                resource_id,
            )
            if row:
                return GetResourceResponse(
                    id=str(row["id"]),
                    subject_id=str(row["subject_id"]),
                    title=row["title"],
                    shared_at=row["shared_at"],
                    shared_by=str(row["shared_by"]),
                    type=ResourceTypeEnum(row["type"]),
                    docs_id=row["docs_id"],
                )
            return None

    @staticmethod
    async def update_resource(
        resource_id: UUID, update_resource: UpdateResourceRequest
    ) -> bool:
        async with PGConnection.get_connection() as conn:
            result = await conn.execute(
                """
                UPDATE resources
                SET title = $1, type = $2
                WHERE id = $3;
                """,
                update_resource.title,
                update_resource.type,
                resource_id,
            )
            return result == "UPDATE 1"

    @staticmethod
    async def delete_resource(resource_id: UUID) -> bool:
        async with PGConnection.get_connection() as conn:
            result = await conn.execute(
                """
                DELETE FROM resources
                WHERE id = $1;
                """,
                resource_id,
            )
            return result == "DELETE 1"

    @staticmethod
    async def get_resources_by_subject(subject_id: UUID) -> list[GetResourceResponse]:
        async with PGConnection.get_connection() as conn:
            rows = await conn.fetch(
                """
                SELECT id, subject_id, title, shared_at, shared_by, type, docs_id
                FROM resources
                WHERE subject_id = $1;
                """,
                subject_id,
            )
            return [
                GetResourceResponse(
                    id=str(row["id"]),
                    subject_id=str(row["subject_id"]),
                    title=row["title"],
                    shared_at=row["shared_at"],
                    shared_by=str(row["shared_by"]),
                    type=ResourceTypeEnum(row["type"]),
                    docs_id=row["docs_id"],
                )
                for row in rows
            ]
    @staticmethod
    async def get_resources_by_teacher(teacher_id: UUID) -> list[GetResourceResponse]:
        async with PGConnection.get_connection() as conn:
            rows = await conn.fetch(
                """
                SELECT resources.id, subject_id,name, title, shared_at, shared_by, type, docs_id
                FROM resources
                INNER JOIN subjects ON subjects.id = resources.subject_id
                WHERE shared_by = $1;
                """,
                teacher_id,
            )
            return [
                GetResourceBySubject.Resource(
                    id=str(row["id"]),
                    subject_id=str(row["subject_id"]),
                    title=row["title"],
                    subject_name=row["name"],
                    shared_at=row["shared_at"],
                    shared_by=str(row["shared_by"]),
                    type=ResourceTypeEnum(row["type"]),
                    docs_id=row["docs_id"],
                )
                for row in rows
            ]
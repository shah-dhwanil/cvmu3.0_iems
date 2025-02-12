from uuid import UUID
from typing import Optional
from iems.base.postgres import PGConnection
from uuid_utils import uuid7

from iems.achievements.schemas import (
    CreateAchievementRequest,
    GetAchievementResponse,
    UpdateAchievementRequest,
    GetAchievementByStudentResponse,
)


class AchievementRepository:
    @staticmethod
    async def create_achievement(create_achievement: CreateAchievementRequest) -> UUID:
        achievement_id = uuid7()
        async with PGConnection.get_connection() as conn:
            await conn.execute(
                """
                INSERT INTO achievements (id, student_id, name, type, pos, docs_id)
                VALUES ($1, $2, $3, $4, $5, $6);
                """,
                str(achievement_id),
                create_achievement.student_id,
                create_achievement.name,
                create_achievement.type,
                create_achievement.pos,
                create_achievement.docs_id,
            )
            return str(achievement_id)

    @staticmethod
    async def get_achievement(achievement_id: UUID) -> Optional[GetAchievementResponse]:
        async with PGConnection.get_connection() as conn:
            row = await conn.fetchrow(
                """
                SELECT id, student_id, name, type, pos, docs_id
                FROM achievements
                WHERE id = $1;
                """,
                achievement_id,
            )
            if row:
                return GetAchievementResponse(
                    id=str(row["id"]),
                    student_id=str(row["student_id"]),
                    name=row["name"],
                    type=row["type"],
                    pos=row["pos"],
                    docs_id=row["docs_id"],
                )
            return None

    @staticmethod
    async def get_achievements_by_student(
        student_id: UUID,
    ) -> GetAchievementByStudentResponse:
        async with PGConnection.get_connection() as conn:
            rows = await conn.fetch(
                """
                SELECT id, student_id, name, type, pos, docs_id
                FROM achievements
                WHERE student_id = $1
                ORDER BY created_at DESC;
                """,
                student_id,
            )
            achievements = [
                GetAchievementResponse(
                    id=str(row["id"]),
                    student_id=str(row["student_id"]),
                    name=row["name"],
                    type=row["type"],
                    pos=row["pos"],
                    docs_id=row["docs_id"],
                )
                for row in rows
            ]
            return GetAchievementByStudentResponse(achievements=achievements)

    @staticmethod
    async def update_achievement(
        achievement_id: UUID, update_achievement: UpdateAchievementRequest
    ) -> bool:
        async with PGConnection.get_connection() as conn:
            result = await conn.execute(
                """
                UPDATE achievements
                SET name = $1, type = $2, pos = $3, docs_id = $4
                WHERE id = $5;
                """,
                update_achievement.name,
                update_achievement.type,
                update_achievement.pos,
                update_achievement.docs_id,
                achievement_id,
            )
            return result == "UPDATE 1"

    @staticmethod
    async def delete_achievement(achievement_id: UUID) -> bool:
        async with PGConnection.get_connection() as conn:
            result = await conn.execute(
                """
                DELETE FROM achievements
                WHERE id = $1;
                """,
                achievement_id,
            )
            return result == "DELETE 1"

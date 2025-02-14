from uuid import UUID
from typing import Optional
from iems.base.postgres import PGConnection
from uuid_utils import uuid7

from iems.external_exams.schemas import (
    CreateExternalExamRequest,
    CreateExternalExamResponse,
    GetExternalExamResponse,
    GetExternalExamsByStudentResponse,
    UpdateExternalExamRequest,
    ExternalExamNotFoundResponse,
    EmptyResponse,
)


class ExternalExamRepository:
    @staticmethod
    async def create_external_exam(create_external_exam: CreateExternalExamRequest) -> CreateExternalExamResponse:
        exam_id = uuid7()
        async with PGConnection.get_connection() as conn:
            await conn.execute(
                """
                INSERT INTO external_exams (id, student_id, name, score, seat_no, yoa,marksheet_uuid, rank)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8);
                """,
                str(exam_id),
                create_external_exam.student_id,
                create_external_exam.name,
                create_external_exam.score,
                create_external_exam.seat_no,
                create_external_exam.yoa,
                create_external_exam.marksheet_uuid,
                create_external_exam.rank,
            )
            return CreateExternalExamResponse(id=str(exam_id))

    @staticmethod
    async def get_external_exam(exam_id: UUID) -> Optional[GetExternalExamResponse]:
        async with PGConnection.get_connection() as conn:
            row = await conn.fetchrow(
                """
                SELECT id, student_id, name, score, seat_no, yoa, rank,marksheet_uuid, created_at
                FROM external_exams
                WHERE id = $1;
                """,
                exam_id,
            )
            if row:
                return GetExternalExamResponse(
                    id=str(row["id"]),
                    student_id=str(row["student_id"]),
                    name=row["name"],
                    score=row["score"],
                    seat_no=row["seat_no"],
                    yoa=row["yoa"],
                    marksheet_uuid=row["marksheet_uuid"],
                    rank=row["rank"],
                )
            return None

    @staticmethod
    async def get_external_exams_by_student(student_id: UUID) -> GetExternalExamsByStudentResponse:
        async with PGConnection.get_connection() as conn:
            rows = await conn.fetch(
                """
                SELECT id, student_id, name, score, seat_no, yoa, rank,marksheet_uuid, created_at
                FROM external_exams
                WHERE student_id = $1
                ORDER BY created_at DESC;
                """,
                student_id,
            )
            external_exams = [
                GetExternalExamResponse(
                    id=str(row["id"]),
                    student_id=str(row["student_id"]),
                    name=row["name"],
                    score=row["score"],
                    seat_no=row["seat_no"],
                    yoa=row["yoa"],
                    marksheet_uuid=row["marksheet_uuid"],
                    rank=row["rank"],
                )
                for row in rows
            ]
            return GetExternalExamsByStudentResponse(external_exams=external_exams)

    @staticmethod
    async def update_external_exam(exam_id: UUID, update_external_exam: UpdateExternalExamRequest) -> bool:
        async with PGConnection.get_connection() as conn:
            result = await conn.execute(
                """
                UPDATE external_exams
                SET name = COALESCE($1, name), score = COALESCE($2, score), seat_no = COALESCE($3, seat_no), 
                    yoa = COALESCE($4, yoa), rank = COALESCE($5, rank)
                WHERE id = $6;
                """,
                update_external_exam.name,
                update_external_exam.score,
                update_external_exam.seat_no,
                update_external_exam.yoa,
                update_external_exam.rank,
                exam_id,
            )
            return result == "UPDATE 1"

    @staticmethod
    async def delete_external_exam(exam_id: UUID) -> bool:
        async with PGConnection.get_connection() as conn:
            result = await conn.execute(
                """
                DELETE FROM external_exams
                WHERE id = $1;
                """,
                exam_id,
            )
            return result == "DELETE 1"
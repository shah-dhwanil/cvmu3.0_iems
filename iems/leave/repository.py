from uuid import UUID
from typing import Optional, List
from iems.base.postgres import PGConnection

from iems.courses.repository import CourseRepository
from iems.leave.schemas import (
    CreateLeaveRequest,
    GetLeaveResponse,
    UpdateLeaveRequest,
    LeaveStatusEnum,
)


class LeaveRepository:
    @staticmethod
    async def create_leave(create_leave: CreateLeaveRequest) -> UUID:
        async with PGConnection.get_connection() as conn:
            row = await conn.fetchrow(
                """
                INSERT INTO leaves (student_id, from_date, to_date, reason, document_id)
                VALUES ($1, $2, $3, $4, $5)
                RETURNING id;
                """,
                create_leave.student_id,
                create_leave.from_date,
                create_leave.to_date,
                create_leave.reason,
                create_leave.document_id,
            )
            return row["id"]

    @staticmethod
    async def get_leave(leave_id: UUID) -> Optional[GetLeaveResponse]:
        async with PGConnection.get_connection() as conn:
            row = await conn.fetchrow(
                """
                SELECT id, student_id, from_date, to_date, reason, status, document_id, created_at
                FROM leaves
                WHERE id = $1;
                """,
                leave_id,
            )
            if row:
                return GetLeaveResponse(
                    id=row["id"],
                    student_id=row["student_id"],
                    from_date=row["from_date"],
                    to_date=row["to_date"],
                    reason=row["reason"],
                    status=LeaveStatusEnum(row["status"]),
                    document_id=row["document_id"],
                )
            return None

    @staticmethod
    async def get_leaves_by_student(student_id: UUID) -> List[GetLeaveResponse]:
        async with PGConnection.get_connection() as conn:
            rows = await conn.fetch(
                """
                SELECT id, student_id, from_date, to_date, reason, status, document_id, created_at
                FROM leaves
                WHERE student_id = $1
                ORDER BY created_at DESC;
                """,
                student_id,
            )
            return [
                GetLeaveResponse(
                    id=row["id"],
                    student_id=row["student_id"],
                    from_date=row["from_date"],
                    to_date=row["to_date"],
                    reason=row["reason"],
                    status=LeaveStatusEnum(row["status"]),
                    document_id=row["document_id"],
                )
                for row in rows
            ]

    @staticmethod
    async def get_pending_leaves_by_hod(hod_id: UUID) -> List[GetLeaveResponse]:
        async with PGConnection.get_connection() as conn:
            rows = await conn.fetch(
                """
                SELECT id, student_id, from_date, to_date, reason, status, document_id, created_at
                FROM leaves
                INNER JOIN students ON leaves.student_id = students.id
                INNER JOIN batch ON students.batch_id = batch.id
                WHERE batch.hod_id = $1 AND status = 'accepted_counciller'
                ORDER BY created_at DESC;
                """,
                hod_id,
            )
            return [
                GetLeaveResponse(
                    id=row["id"],
                    student_id=row["student_id"],
                    from_date=row["from_date"],
                    to_date=row["to_date"],
                    reason=row["reason"],
                    status=LeaveStatusEnum(row["status"]),
                    document_id=row["document_id"],
                )
                for row in rows
            ]

    @staticmethod
    async def get_pending_leaves_by_counciller(
        counciller_id: UUID,
    ) -> List[GetLeaveResponse]:
        async with PGConnection.get_connection() as conn:
            rows = await conn.fetch(
                """
                SELECT id, student_id, from_date, to_date, reason, status, document_id, created_at
                FROM leaves
                INNER JOIN students ON leaves.student_id = students.id
                INNER JOIN batch ON students.batch_id = batch.id
                WHERE batch.counciller_id = $1 AND status = 'submitted'
                ORDER BY created_at DESC;
                """,
                counciller_id,
            )
            return [
                GetLeaveResponse(
                    id=row["id"],
                    student_id=row["student_id"],
                    from_date=row["from_date"],
                    to_date=row["to_date"],
                    reason=row["reason"],
                    status=LeaveStatusEnum(row["status"]),
                    document_id=row["document_id"],
                )
                for row in rows
            ]

    @staticmethod
    async def update_leave(leave_id: UUID, update_leave: UpdateLeaveRequest) -> bool:
        async with PGConnection.get_connection() as conn:
            result = await conn.execute(
                """
                UPDATE leaves
                SET from_date = $1, to_date = $2, reason = $3, document_id = $4
                WHERE id = $5;
                """,
                update_leave.from_date,
                update_leave.to_date,
                update_leave.reason,
                update_leave.document_id,
                leave_id,
            )
            return result == "UPDATE 1"

    @staticmethod
    async def update_leave_status(leave_id: UUID, status: LeaveStatusEnum) -> bool:
        async with PGConnection.get_connection() as conn:
            result = await conn.execute(
                """
                UPDATE leaves
                SET status = $1
                WHERE id = $2;
                """,
                status,
                leave_id,
            )
            return result == "UPDATE 1"

    @staticmethod
    async def delete_leave(leave_id: UUID) -> bool:
        async with PGConnection.get_connection() as conn:
            result = await conn.execute(
                """
                DELETE FROM leaves
                WHERE id = $1;
                """,
                leave_id,
            )
            return result == "DELETE 1"

    @staticmethod
    async def approve_leave(leave_id: UUID):
        async with PGConnection.get_connection() as conn:
            leave = await LeaveRepository.get_leave(leave_id)
            courses = await CourseRepository.get_course_by_student_id(leave.student_id)
            course_ids = [course.id for course in courses]
            await conn.execute(
                """
                UPDATE attendance
                SET dont_care = true
                WHERE student_id = $1 
                AND course_id IN $2
                AND class_time BETWEEN $3 AND $4;
                """,
                leave.student_id,
                course_ids,
                leave.from_date,
                leave.to_date,
            )

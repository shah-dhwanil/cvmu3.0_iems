from uuid import UUID
from typing import List
from datetime import datetime

from uuid_utils import uuid7
from iems.base.postgres import PGConnection

from iems.attendence.schemas import (
    MarkAttendence,
    GetAttendenceByCourseIdAndClassTimeResponse,
    GetAttendenceByStudentId,
    UpdateAttendence,
)


class AttendenceRepository:
    @staticmethod
    async def mark_attendence(mark_attendence: MarkAttendence) -> List[UUID]:
        async with PGConnection.get_connection() as conn:
            # Create records for present students
            present_ids = []
            for student_id in mark_attendence.present_student_ids:
                uid = uuid7()
                row = await conn.fetchrow(
                    """
                    INSERT INTO attendence (id,course_id, student_id, class_time, present)
                    VALUES ($1, $2, $3,$4, true)
                    RETURNING id;
                    """,
                    uid,
                    mark_attendence.course_id,
                    student_id,
                    mark_attendence.class_time,
                )
                present_ids.append(row["id"])

            # Create records for absent students
            absent_ids = []
            for student_id in mark_attendence.absent_student_ids:
                uid = uuid7()
                row = await conn.fetchrow(
                    """
                    INSERT INTO attendence (id,course_id, student_id, class_time, present)
                    VALUES ($1, $2, $3,$4, false)
                    RETURNING id;
                    """,
                    uid,
                    mark_attendence.course_id,
                    student_id,
                    mark_attendence.class_time,
                )
                absent_ids.append(row["id"])

            return present_ids + absent_ids

    @staticmethod
    async def get_attendence_by_course_and_time(
        course_id: UUID, class_time: datetime
    ) -> GetAttendenceByCourseIdAndClassTimeResponse:
        async with PGConnection.get_connection() as conn:
            rows = await conn.fetch(
                """
                SELECT id, student_id, present, dont_care
                FROM attendence
                WHERE course_id = $1 AND class_time = $2;
                """,
                course_id,
                class_time,
            )
            records = [
                GetAttendenceByCourseIdAndClassTimeResponse.AttendenceRecord(
                    id=row["id"],
                    student_id=row["student_id"],
                    present=row["present"],
                    dont_care=row["dont_care"],
                )
                for row in rows
            ]
            return GetAttendenceByCourseIdAndClassTimeResponse(
                attendence_records=records
            )

    @staticmethod
    async def get_attendence_by_student(student_id: UUID) -> GetAttendenceByStudentId:
        async with PGConnection.get_connection() as conn:
            rows = await conn.fetch(
                """
                SELECT 
                    course_id,
                    COUNT(CASE WHEN present = true THEN 1 END) as present_no,
                    COUNT(CASE WHEN dont_care = true THEN 1 END) as dont_care_no,
                    COUNT(*) as total_no
                FROM attendence
                INNER JOIN courses ON attendence.course_id = courses.id
                INNER JOIN students ON attendence.student_id = students.id
                WHERE student_id = $1 AND courses.semester_id = students.curr_sem
                GROUP BY course_id;
                """,
                student_id,
            )
            records = [
                GetAttendenceByStudentId.AttendenceRecord(
                    course_id=row["course_id"],
                    present_no=row["present_no"],
                    dont_care_no=row["dont_care_no"],
                    total_no=row["total_no"],
                )
                for row in rows
            ]
            return GetAttendenceByStudentId(attendence_records=records)

    @staticmethod
    async def update_attendence(update: UpdateAttendence) -> bool:
        async with PGConnection.get_connection() as conn:
            result = await conn.execute(
                """
                UPDATE attendence
                SET present = $1
                WHERE id = $2;
                """,
                update.present,
                update.id,
            )
            return result == "UPDATE 1"

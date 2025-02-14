from uuid import UUID
from typing import Optional
from iems.base.postgres import PGConnection
from uuid_utils import uuid7

from iems.courses.schemas import (
    CreateCourseRequest,
    GetCourseResponse,
    GetCouseByStudentId,
    UpdateCourseRequest,
    GetCourseTaughtBy,
)


class CourseRepository:
    @staticmethod
    async def create_course(create_course: CreateCourseRequest) -> UUID:
        course_id = uuid7()
        async with PGConnection.get_connection() as conn:
            await conn.execute(
                """
                INSERT INTO courses (id, sem_id, subject_id, taught_by)
                VALUES ($1, $2, $3, $4);
                """,
                str(course_id),
                create_course.sem_id,
                create_course.subject_id,
                create_course.taught_by,
            )
            return str(course_id)

    @staticmethod
    async def get_course(course_id: UUID) -> Optional[GetCourseResponse]:
        async with PGConnection.get_connection() as conn:
            row = await conn.fetchrow(
                """
                SELECT id, sem_id, subject_id, taught_by, active, created_at
                FROM courses
                WHERE id = $1;
                """,
                course_id,
            )
            if row:
                return GetCourseResponse(
                    id=str(row["id"]),
                    sem_id=str(row["sem_id"]),
                    subject_id=str(row["subject_id"]),
                    taught_by=str(row["taught_by"]),
                )
            return None

    @staticmethod
    async def get_course_by_student_id(student_id: UUID) -> list[GetCouseByStudentId.Course]:
        async with PGConnection.get_connection() as conn:
            row = await conn.fetch(
                """
                SELECT courses.id,subjects.name,courses.taught_by FROM courses
                INNER JOIN semister ON courses.sem_id = semister.id
                INNER JOIN batch ON semister.batch_id = batch.id
                INNER JOIN students ON students.batch_id =batch.id
                INNER JOIN subjects ON courses.subject_id = subjects.id
                WHERE courses.sem_id = students.current_sem AND students.id = $1;
                """,
                student_id,
            )
            return [
                GetCouseByStudentId.Course(id=str(r["id"]), name=r["name"], by=str(r["taught_by"]))
                for r in row
            ]

    @staticmethod
    async def get_course_by_teacher_id(teacher_id: UUID) -> list[GetCourseTaughtBy]:
        async with PGConnection.get_connection() as conn:
            row = await conn.fetch(
                """
                SELECT courses.id,courses.sem_id,subjects.name,batch.branch,batch.year FROM courses
                INNER JOIN semister ON courses.sem_id = semister.id
                INNER JOIN batch ON semister.batch_id = batch.id
                INNER JOIN subjects ON courses.subject_id = subjects.id
                WHERE courses.sem_id IN (SELECT sem_id FROM students GROUP BY sem_id)
                AND courses.taught_by = $1;
                """,
                teacher_id,
            )
            return [
                GetCourseTaughtBy(
                    id=str(r["id"]),sem_id=str(r["sem_id"]), name=r["name"], branch=r["branch"], year=r["year"]
                )
                for r in row
            ]

    @staticmethod
    async def update_course(
        course_id: UUID, update_course: UpdateCourseRequest
    ) -> bool:
        async with PGConnection.get_connection() as conn:
            result = await conn.execute(
                """
                UPDATE courses
                SET sem_id = $1, subject_id = $2, taught_by = $3
                WHERE id = $4;
                """,
                update_course.sem_id,
                update_course.subject_id,
                update_course.taught_by,
                course_id,
            )
            return result == "UPDATE 1"

    @staticmethod
    async def delete_course(course_id: UUID) -> bool:
        async with PGConnection.get_connection() as conn:
            result = await conn.execute(
                """
                UPDATE courses
                SET active = false
                WHERE id = $1;
                """,
                course_id,
            )
            return result == "UPDATE 1"

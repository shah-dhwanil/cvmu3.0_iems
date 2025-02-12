from uuid import UUID
from typing import Optional
from asyncpg import ForeignKeyViolationError, UniqueViolationError
from iems.base.postgres import PGConnection
from iems.students.exceptions import StudentAlreadyExistsError

from iems.students.schemas import (
    CreateStudentRequest,
    GetStudentResponse,
    UpdateStudentCurrentSemRequest,
    UpdateStudentRequest,
    GetAllStudentsResponse,
)
from iems.users.exceptions import UserNotFoundException


class StudentRepository:
    @staticmethod
    async def create_student(create_student: CreateStudentRequest) -> UUID:
        async with PGConnection.get_connection() as conn:
            try:
                await conn.execute(
                    """
                    INSERT INTO students (
                        id, first_name, last_name, enrollment_id,
                        gender, contact_no, email_id,batch_id,current_sem
                    )
                    VALUES ($1, $2, $3, $4, $5, $6, $7,$8,$9);
                    """,
                    create_student.id,
                    create_student.first_name,
                    create_student.last_name,
                    create_student.enrollment_id,
                    create_student.gender,
                    create_student.contact_no,
                    create_student.email_id,
                    create_student.batch_id,
                    create_student.current_sem,
                )
                return create_student.id
            except UniqueViolationError:
                raise StudentAlreadyExistsError()
            except ForeignKeyViolationError:
                raise UserNotFoundException()

    @staticmethod
    async def get_student(student_id: UUID) -> Optional[GetStudentResponse]:
        async with PGConnection.get_connection() as conn:
            row = await conn.fetchrow(
                """
                SELECT id, first_name, last_name, enrollment_id,
                       gender, contact_no, email_id, active
                FROM students
                WHERE id = $1;
                """,
                student_id,
            )
            if row:
                return GetStudentResponse(
                    id=str(row["id"]),
                    first_name=row["first_name"],
                    last_name=row["last_name"],
                    enrollment_id=row["enrollment_id"],
                    gender=row["gender"],
                    contact_no=row["contact_no"],
                    email_id=row["email_id"],
                    active=row["active"],
                )
            return None

    @staticmethod
    async def get_all_students() -> GetAllStudentsResponse:
        async with PGConnection.get_connection() as conn:
            rows = await conn.fetch(
                """
                SELECT id, enrollment_id, first_name, last_name
                FROM students
                WHERE active = true;
                """
            )
            students = [
                GetAllStudentsResponse.Student(
                    id=str(row["id"]),
                    enrollment_id=row["enrollment_id"],
                    name=f"{row['first_name']} {row['last_name']}",
                )
                for row in rows
            ]
            return GetAllStudentsResponse(students=students)

    @staticmethod
    async def update_student(
        student_id: UUID, update_student: UpdateStudentRequest
    ) -> bool:
        async with PGConnection.get_connection() as conn:
            try:
                result = await conn.execute(
                    """
                    UPDATE students
                    SET first_name = $1,
                        last_name = $2,
                        enrollment_id = $3,
                        gender = $4,
                        contact_no = $5,
                        email_id = $6
                    WHERE id = $7;
                    """,
                    update_student.first_name,
                    update_student.last_name,
                    update_student.enrollment_id,
                    update_student.gender,
                    update_student.contact_no,
                    update_student.email_id,
                    student_id,
                )
                return result == "UPDATE 1"
            except UniqueViolationError:
                raise StudentAlreadyExistsError()

    @staticmethod
    async def update_student_current_sem(
        update_request: UpdateStudentCurrentSemRequest,
    ):
        async with PGConnection.get_connection() as conn:
            await conn.execute(
                """
                UPDATE students
                SET current_sem = $1
                WHERE batch_id = $2;
                """,
                update_request.current_sem,
                update_request.branch_id,
            )

    @staticmethod
    async def delete_student(student_id: UUID) -> bool:
        async with PGConnection.get_connection() as conn:
            result = await conn.execute(
                """
                UPDATE students
                SET active = false
                WHERE id = $1;
                """,
                student_id,
            )
            return result == "UPDATE 1"

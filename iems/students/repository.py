from random import randint
from uuid import UUID
from typing import Optional
from asyncpg import ForeignKeyViolationError, UniqueViolationError
from iems.base.postgres import PGConnection
from iems.batch.repository import BatchRepository
from iems.semister.repository import SemisterRepository
from iems.students.exceptions import StudentAlreadyExistsError

from iems.students.schemas import (
    CreateStudentRequest,
    CreateStudentResponse,
    GetStudentResponse,
    UpdateStudentCurrentSemRequest,
    UpdateStudentRequest,
    GetAllStudentsResponse,
)
from iems.users.exceptions import UserNotFoundException
from iems.users.repository import UserRepository
from iems.users.schemas import CreateUserRequest, RoleEnum


class StudentRepository:
    @staticmethod
    async def create_student(create_student: CreateStudentRequest) -> CreateStudentResponse:
        uid = await UserRepository.create_user(CreateUserRequest(username=f"student112q7",password="Student@123",role=RoleEnum.STUDENT))
        branch = await BatchRepository.get_batch(create_student.batch_id)
        branch_name = branch.branch.split(",")[1];
        seq_name = f"{branch_name}_{branch.year}"
        semister = await SemisterRepository.get_semister_by_branch(create_student.batch_id)
        semister.sort(key=lambda x: x.sem_no)
        semister_id = semister[0].id
        async with PGConnection.get_connection() as conn:
            try:
                enrollment_id =  await conn.fetchval("SELECT nextval($1)",seq_name)
                enrollment_id = f"{branch.year}{branch_name}{enrollment_id}"
                await conn.execute(
                    """
                    INSERT INTO students (
                        id, first_name, last_name, enrollment_id,
                        gender, contact_no, email_id,batch_id,current_sem
                    )
                    VALUES ($1, $2, $3, $4, $5 ,$6, $7,$8,$9);
                    """,
                    uid,
                    create_student.first_name,
                    create_student.last_name,
                    enrollment_id,
                    create_student.gender,
                    create_student.contact_no,
                    create_student.email_id,
                    create_student.batch_id,
                    semister_id
                )
                await conn.execute("UPDATE users SET username = $1 WHERE id = $2",f"student.{enrollment_id}",uid)
                return CreateStudentResponse(uid = str(uid), enrollment_id=enrollment_id)
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
                       gender, contact_no, email_id, active,batch_id
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
                    batch_id=str(row["batch_id"]),
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
    async def get_students_by_sem_id(sem_id:UUID) -> GetAllStudentsResponse:
        async with PGConnection.get_connection() as conn:
            rows = await conn.fetch(
                """
                SELECT id, enrollment_id, first_name, last_name
                FROM students
                WHERE current_sem = $1 AND active = true;
                """,
                sem_id
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

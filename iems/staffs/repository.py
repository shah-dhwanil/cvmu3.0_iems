from uuid import UUID
from typing import Optional
from asyncpg import ForeignKeyViolationError, UniqueViolationError
from iems.base.postgres import PGConnection

from iems.staffs.schemas import (
    CreateStaffRequest,
    GetStaffResponse,
    UpdateStaffRequest,
    GetAllStaffResponse,
)

from iems.staffs.exceptions import StaffAlreadyExistsError, UserNotFoundError


class StaffRepository:
    @staticmethod
    async def create_staff(create_staff: CreateStaffRequest) -> UUID:
        async with PGConnection.get_connection() as conn:
            try:
                await conn.execute(
                    """
                    INSERT INTO staff (
                        id, first_name, last_name, contact_no, 
                        email_id, qualification, experience
                    )
                    VALUES ($1, $2, $3, $4, $5, $6, $7)
                    """,
                    create_staff.id,
                    create_staff.first_name,
                    create_staff.last_name,
                    create_staff.contact_no,
                    create_staff.email_id,
                    create_staff.qualification,
                    create_staff.experience,
                )
                return create_staff.id
            except UniqueViolationError:
                raise StaffAlreadyExistsError()
            except ForeignKeyViolationError:
                raise UserNotFoundError()

    @staticmethod
    async def get_staff(staff_id: UUID) -> Optional[GetStaffResponse]:
        async with PGConnection.get_connection() as conn:
            row = await conn.fetchrow(
                """
                SELECT id, first_name, last_name, contact_no, 
                       email_id, qualification, experience, active
                FROM staff
                WHERE id = $1
                """,
                staff_id,
            )
            if row:
                return GetStaffResponse(
                    id=row["id"],
                    first_name=row["first_name"],
                    last_name=row["last_name"],
                    contact_no=row["contact_no"],
                    email_id=row["email_id"],
                    qualification=row["qualification"],
                    experience=row["experience"],
                    active=row["active"],
                )
            return None

    @staticmethod
    async def get_all_staff() -> GetAllStaffResponse:
        async with PGConnection.get_connection() as conn:
            rows = await conn.fetch(
                """
                SELECT id, first_name, last_name
                FROM staff
                WHERE active = true
                """
            )
            staff_members = [
                GetAllStaffResponse.Staff(
                    id=row["id"], name=f"{row['first_name']} {row['last_name']}"
                )
                for row in rows
            ]
            return GetAllStaffResponse(staff_members=staff_members)

    @staticmethod
    async def update_staff(staff_id: UUID, update_staff: UpdateStaffRequest) -> bool:
        async with PGConnection.get_connection() as conn:
            try:
                result = await conn.execute(
                    """ --sql
                    UPDATE staff 
                    SET first_name = $1,
                        last_name = $2,
                        contact_no = $3,
                        email_id = $4,
                        qualification = $5,
                        experience = $6
                    WHERE id = $7
                    """,
                    update_staff.first_name,
                    update_staff.last_name,
                    update_staff.contact_no,
                    update_staff.email_id,
                    update_staff.qualification,
                    update_staff.experience,
                    staff_id,
                )
                return result == "UPDATE 1"
            except UniqueViolationError:
                raise StaffAlreadyExistsError()

    @staticmethod
    async def delete_staff(staff_id: UUID) -> bool:
        async with PGConnection.get_connection() as conn:
            result = await conn.execute(
                """
                UPDATE staff
                SET active = false
                WHERE id = $1
                """,
                staff_id,
            )
            return result == "UPDATE 1"

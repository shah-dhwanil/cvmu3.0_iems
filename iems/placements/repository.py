from uuid import UUID
from typing import Optional, List
from iems.base.postgres import PGConnection

from iems.placements.schemas import (
    CreatePlacementEnrollRequest,
    CreatePlacementRequest,
    GetPlacementResponse,
    UpdatePlacementRequest,
    PlacementStatus,
    UpdatePlacementStatusRequest,
)


class PlacementRepository:
    @staticmethod
    async def create_placement(create_placement: CreatePlacementRequest) -> UUID:
        async with PGConnection.get_connection() as conn:
            row = await conn.fetchrow(
                """
                INSERT INTO placement (
                    student_id, company_name, role, package, 
                    status, letter_uid
                )
                VALUES ($1, $2, $3, $4, $5, $6)
                RETURNING id;
                """,
                create_placement.student_id,
                create_placement.company_name,
                create_placement.role,
                create_placement.package,
                create_placement.status,
                create_placement.letter_uid,
            )
            return str(row["id"])
    @staticmethod
    async def create_placement_by_student(create_placement: CreatePlacementEnrollRequest) -> UUID:
        async with PGConnection.get_connection() as conn:
            uid = await conn.fetchval("SELECT id FROM students WHERE enrollment_id = $1",create_placement.enroll_id)
            row = await conn.fetchrow(
                """
                INSERT INTO placement (
                    student_id, company_name, role, package, 
                    status, letter_uid
                )
                VALUES ($1, $2, $3, $4, $5, $6)
                RETURNING id;
                """,
                uid,
                create_placement.company_name,
                create_placement.role,
                create_placement.package,
                create_placement.status,
                create_placement.letter_uid,
            )
            return str(row["id"])
    @staticmethod
    async def get_placements(student_id: UUID) -> List[GetPlacementResponse]:
        async with PGConnection.get_connection() as conn:
            rows = await conn.fetch(
                """
                SELECT id, student_id, company_name, role, 
                       package, status, letter_uid
                FROM placement
                WHERE student_id = $1;
                """,
                student_id,
            )
            return [
                GetPlacementResponse(
                    id=str(row["id"]),
                    student_id=str(row["student_id"]),
                    company_name=row["company_name"],
                    role=row["role"],
                    package=float(row["package"]),
                    status=PlacementStatus(row["status"]),
                    letter_uid=row["letter_uid"],
                )
                for row in rows
            ]
    @staticmethod
    async def get_placement() -> Optional[GetPlacementResponse]:
        async with PGConnection.get_connection() as conn:
            rows = await conn.fetch(
                """
                SELECT id, student_id, company_name, role, 
                       package, status, letter_uid
                FROM placement;
                """
            )
            return [
                GetPlacementResponse(
                    id=str(row["id"]),
                    student_id=str(row["student_id"]),
                    company_name=row["company_name"],
                    role=row["role"],
                    package=float(row["package"]),
                    status=PlacementStatus(row["status"]),
                    letter_uid=row["letter_uid"],
                )
                for row in rows
            ]


    @staticmethod
    async def get_placements_by_student(student_id: UUID) -> List[GetPlacementResponse]:
        async with PGConnection.get_connection() as conn:
            rows = await conn.fetch(
                """
                SELECT id, student_id, company_name, role, 
                       package, status, letter_uid
                FROM placement
                WHERE student_id = $1;
                """,
                student_id,
            )
            return [
                GetPlacementResponse(
                    id=str(row["id"]),
                    student_id=str(row["student_id"]),
                    company_name=row["company_name"],
                    role=row["role"],
                    package=float(row["package"]),
                    status=PlacementStatus(row["status"]),
                    letter_uid=row["letter_uid"],
                )
                for row in rows
            ]

    @staticmethod
    async def update_placement(
        placement_id: UUID, update_placement: UpdatePlacementRequest
    ) -> bool:
        async with PGConnection.get_connection() as conn:
            result = await conn.execute(
                """
                UPDATE placement
                SET company_name = $2,
                    role = $3,
                    package = $4,
                    letter_uid = $5
                WHERE id = $1;
                """,
                placement_id,
                update_placement.company_name,
                update_placement.role,
                update_placement.package,
                update_placement.letter_uid,
            )
            return True
            #return result == "UPDATE 1"

    @staticmethod
    async def update_placement_status(
        placement_id: UUID, update_status: UpdatePlacementStatusRequest
    ) -> bool:
        async with PGConnection.get_connection() as conn:
            result = await conn.execute(
                """
                UPDATE placement
                SET status = $2
                WHERE id = $1;
                """,
                placement_id,
                update_status.status,
            )
            return True
            return result == "UPDATE 1"

    @staticmethod
    async def delete_placement(placement_id: UUID) -> bool:
        async with PGConnection.get_connection() as conn:
            result = await conn.execute(
                """
                DELETE FROM placement
                WHERE id = $1;
                """,
                str(placement_id),
            )
            return result == "DELETE 1"

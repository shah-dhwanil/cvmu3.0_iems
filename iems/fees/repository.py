from uuid import UUID
from typing import Optional
from iems.base.postgres import PGConnection
from uuid_utils import uuid7

from iems.fees.schemas import (
    CreateFeesRequest,
    CreateFeesResponse,
    GetFeesResponse,
    UpdateFeesRequest,
    GetFeesByStudentResponse,
)


class FeesRepository:
    @staticmethod
    async def create_fees(create_fees: CreateFeesRequest) -> CreateFeesResponse:
        fees_id = uuid7()
        async with PGConnection.get_connection() as conn:
            row = await conn.fetchrow(
                """
                INSERT INTO fees (id, date, student_id, type, payment_type, transaction_id, amount)
                VALUES ($1, $2, $3, $4, $5, $6, $7)
                RETURNING id, recipt_id;
                """,
                str(fees_id),
                create_fees.date,
                create_fees.student_id,
                create_fees.type,
                create_fees.payment_type,
                create_fees.transaction_id,
                create_fees.amount,
            )
            return CreateFeesResponse(id=row["id"], recipt_id=row["recipt_id"])

    @staticmethod
    async def get_fees(fees_id: UUID) -> Optional[GetFeesResponse]:
        async with PGConnection.get_connection() as conn:
            row = await conn.fetchrow(
                """
                SELECT id, recipt_id, date, student_id, type, payment_type, transaction_id, amount
                FROM fees
                WHERE id = $1;
                """,
                fees_id,
            )
            if row:
                return GetFeesResponse(
                    id=row["id"],
                    recipt_id=row["recipt_id"],
                    date=row["date"],
                    student_id=row["student_id"],
                    type=row["type"],
                    payment_type=row["payment_type"],
                    transaction_id=row["transaction_id"],
                    amount=row["amount"],
                )
            return None

    @staticmethod
    async def get_fees_by_student(student_id: UUID) -> GetFeesByStudentResponse:
        async with PGConnection.get_connection() as conn:
            rows = await conn.fetch(
                """
                SELECT id, recipt_id, date, student_id, type, payment_type, transaction_id, amount
                FROM fees
                WHERE student_id = $1
                ORDER BY date DESC;
                """,
                student_id,
            )
            fees_list = [
                GetFeesResponse(
                    id=row["id"],
                    recipt_id=row["recipt_id"],
                    date=row["date"],
                    student_id=row["student_id"],
                    type=row["type"],
                    payment_type=row["payment_type"],
                    transaction_id=row["transaction_id"],
                    amount=row["amount"],
                )
                for row in rows
            ]
            return GetFeesByStudentResponse(fees=fees_list)

    @staticmethod
    async def update_fees(fees_id: UUID, update_fees: UpdateFeesRequest) -> bool:
        async with PGConnection.get_connection() as conn:
            result = await conn.execute(
                """
                UPDATE fees
                SET date = $1, type = $2, payment_type = $3, transaction_id = $4, amount = $5
                WHERE id = $6;
                """,
                update_fees.date,
                update_fees.type,
                update_fees.payment_type,
                update_fees.transaction_id,
                update_fees.amount,
                fees_id,
            )
            return result == "UPDATE 1"

    @staticmethod
    async def delete_fees(fees_id: UUID) -> bool:
        async with PGConnection.get_connection() as conn:
            result = await conn.execute(
                """
                DELETE FROM fees
                WHERE id = $1;
                """,
                fees_id,
            )
            return result == "DELETE 1"

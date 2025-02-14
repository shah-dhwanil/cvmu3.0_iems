from uuid import UUID
from typing import Optional
from datetime import date, time
from iems.base.postgres import PGConnection
from uuid_utils import uuid7

from iems.events.schemas import (
    CreateEventRequest,
    GetEventResponse,
    UpdateEventRequest,
)


class EventRepository:
    @staticmethod
    async def create_event(create_event: CreateEventRequest) -> UUID:
        event_id = uuid7()
        async with PGConnection.get_connection() as conn:
            await conn.execute(
                """
                INSERT INTO events (id, tile, description, date, start_time, end_time, location, docs_id)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8);
                """,
                str(event_id),
                create_event.tile,
                create_event.description,
                create_event.date,
                create_event.start_time,
                create_event.end_time,
                create_event.location,
                create_event.docs_id,
            )
            return event_id

    @staticmethod
    async def get_event(event_id: UUID) -> Optional[GetEventResponse]:
        async with PGConnection.get_connection() as conn:
            row = await conn.fetchrow(
                """
                SELECT id, tile, description, date, start_time, end_time, location, docs_id
                FROM events
                WHERE id = $1;
                """,
                event_id,
            )
            if row:
                return GetEventResponse(
                    id=str(row["id"]),
                    tile=row["tile"],
                    description=row["description"],
                    date=row["date"],
                    start_time=row["start_time"],
                    end_time=row["end_time"],
                    location=row["location"],
                    docs_id=row["docs_id"] if row["docs_id"] else None,
                )
            return None
    @staticmethod
    async def get_all_events() -> list[GetEventResponse]:
        async with PGConnection.get_connection() as conn:
            rows = await conn.fetch(
                """
                SELECT id, tile, description, date, start_time, end_time, location, docs_id
                FROM events
                ORDER BY date DESC, start_time ASC;
                """
            )
            return [
                GetEventResponse(
                    id=str(row["id"]),
                    tile=row["tile"],
                    description=row["description"],
                    date=row["date"],
                    start_time=row["start_time"],
                    end_time=row["end_time"],
                    location=row["location"],
                    docs_id=row["docs_id"] if row["docs_id"] else None,
                )
                for row in rows
            ]
    @staticmethod
    async def update_event(event_id: UUID, update_event: UpdateEventRequest) -> bool:
        update_fields = []
        values = []
        param_count = 1

        # Dynamically build UPDATE query based on provided fields
        for field, value in update_event.dict(exclude_unset=True).items():
            if value is not None:
                update_fields.append(f"{field} = ${param_count}")
                values.append(value)
                param_count += 1

        if not update_fields:
            return False

        query = f"""
            UPDATE events
            SET {", ".join(update_fields)}
            WHERE id = ${param_count}
        """
        values.append(event_id)

        async with PGConnection.get_connection() as conn:
            result = await conn.execute(query, *values)
            return result == "UPDATE 1"

    @staticmethod
    async def delete_event(event_id: UUID) -> bool:
        async with PGConnection.get_connection() as conn:
            result = await conn.execute(
                """
                DELETE FROM events
                WHERE id = $1;
                """,
                event_id,
            )
            return result == "DELETE 1"
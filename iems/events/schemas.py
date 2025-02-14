from pydantic import BaseModel, Field
from typing import Any, Optional
from uuid import UUID
from datetime import date, time

class CreateEventRequest(BaseModel):
    tile: str = Field(..., max_length=255)
    description: Optional[str] = None
    date: date
    start_time: time
    end_time: time
    location: Optional[str] = Field(None, max_length=255)
    docs_id: Optional[UUID] = None


class CreateEventResponse(BaseModel):
    id: UUID


class GetEventRequest(BaseModel):
    id: UUID


class GetEventResponse(BaseModel):
    id: UUID
    tile: str
    description: Optional[str]
    date: date
    start_time: time
    end_time: time
    location: Optional[str]
    docs_id: Optional[UUID]

class GetAllEventsResponse(BaseModel):
    events: list[GetEventResponse]

class UpdateEventRequest(BaseModel):
    tile: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    date: Optional[date] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    location: Optional[str] = Field(None, max_length=255)
    docs_id: Optional[UUID] = None


class DeleteEventRequest(BaseModel):
    id: UUID


class EventNotFoundResponse(BaseModel):
    error: str = "event_not_found"
    message: str = "Event not found"


class EmptyResponse(BaseModel): ...
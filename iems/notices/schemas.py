from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID

class CreateNoticeRequest(BaseModel):
    title: str = Field(..., max_length=32)
    description: str
    target_audience: Optional[str] = Field(None, max_length=32)
    batch_id:Optional[UUID]
    docs_id: Optional[UUID] = None
    created_by: UUID


class CreateNoticeResponse(BaseModel):
    id: UUID


class GetNoticeResponse(BaseModel):
    id: UUID
    created_by: UUID
    title: str
    description: str
    target_audience: Optional[str]
    batch_id:Optional[UUID]
    docs_id: Optional[UUID]


class GetNoticesResponse(BaseModel):
    notices: list[GetNoticeResponse]


class UpdateNoticeRequest(BaseModel):
    title: Optional[str] = Field(None, max_length=32)
    description: Optional[str]
    target_audience: Optional[str] = Field(None, max_length=32)
    batch_id:Optional[UUID]
    docs_id: Optional[UUID]


class NoticeNotFoundResponse(BaseModel):
    error: str = "notice_not_found"
    message: str = "Notice not found"


class EmptyResponse(BaseModel): ...
from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID


class CreateBatchRequest(BaseModel):
    branch: str = Field(..., max_length=255)
    year: int = Field(..., ge=1900, le=2100)
    hod_id: UUID
    counciller_id: UUID
    active: Optional[bool] = True


class CreateBatchResponse(BaseModel):
    id: UUID


class MultipleCreateBatchResponse(BaseModel):
    ids: list[CreateBatchResponse]


class GetBatchResponse(BaseModel):
    id: UUID
    branch: str
    year: int
    hod_id: UUID
    counciller_id: UUID
    active: bool
    created_at: str


class UpdateBatchRequest(BaseModel):
    branch: Optional[str] = Field(None, max_length=255)
    year: Optional[int] = Field(None, ge=1900, le=2100)
    hod_id: Optional[UUID]
    counciller_id: Optional[UUID]
    active: Optional[bool]


class BatchNotFoundResponse(BaseModel):
    error: str = "batch_not_found"
    message: str = "Batch not found"


class EmptyResponse(BaseModel):
    pass

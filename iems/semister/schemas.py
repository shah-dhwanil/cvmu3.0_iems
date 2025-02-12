from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID


class CreateSemisterRequest(BaseModel):
    batch_id: UUID
    sem_no: int = Field(..., ge=1, le=12)
    ongoing: bool


class CreateSemisterResponse(BaseModel):
    id: UUID


class GetSemisterResponse(BaseModel):
    id: UUID
    batch_id: UUID
    sem_no: int
    ongoing: bool

class GetSemisterByBranchResponse(BaseModel):
    semisters: list[GetSemisterResponse]

class UpdateSemisterRequest(BaseModel):
    batch_id: Optional[UUID]
    sem_no: Optional[int] = Field(None, ge=1, le=12)
    ongoing: Optional[bool]


class SemisterNotFoundResponse(BaseModel):
    error: str = "semister_not_found"
    message: str = "Semister not found"


class EmptyResponse(BaseModel):
    pass

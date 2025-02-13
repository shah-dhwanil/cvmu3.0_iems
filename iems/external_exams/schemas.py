from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID

class CreateExternalExamRequest(BaseModel):
    student_id: UUID
    name: str = Field(..., max_length=64)
    score: float = Field(..., ge=0, le=100)
    seat_no: str = Field(..., max_length=64)
    yoa: int
    marksheet_uuid: Optional[UUID]
    rank: Optional[int] = None


class CreateExternalExamResponse(BaseModel):
    id: UUID


class GetExternalExamResponse(BaseModel):
    id: UUID
    student_id: UUID
    name: str
    score: float
    seat_no: str
    yoa: int
    rank: Optional[int]
    marksheet_uuid :Optional[UUID]
    created_at: str


class GetExternalExamsByStudentResponse(BaseModel):
    external_exams: list[GetExternalExamResponse]


class UpdateExternalExamRequest(BaseModel):
    name: str = Field( max_length=64)
    score: float = Field(ge=0, le=100)
    seat_no: str = Field(max_length=64)
    yoa: int
    rank: int


class ExternalExamNotFoundResponse(BaseModel):
    error: str = "external_exam_not_found"
    message: str = "External exam not found"


class EmptyResponse(BaseModel): ...
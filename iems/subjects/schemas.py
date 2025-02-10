from pydantic import BaseModel, Field
from uuid import UUID


class CreateSubjectRequest(BaseModel):
    code: str = Field(..., max_length=16)
    name: str = Field(..., max_length=64)
    credits: int = Field(..., ge=1, le=10)


class CreateSubjectResponse(BaseModel):
    id: UUID


class GetSubjectResponse(BaseModel):
    id: UUID
    code: str
    name: str
    credits: int


class GetAllSubjectsResponse(BaseModel):
    subjects: list[GetSubjectResponse]


class UpdateSubjectRequest(BaseModel):
    id: UUID
    code: str = Field(max_length=16)
    name: str = Field(max_length=64)
    credits: int = Field(ge=1, le=10)


class SubjectNotFoundResponse(BaseModel):
    error: str = "subject_not_found"
    message: str = "Subject not found"


class EmptyResponse(BaseModel): ...

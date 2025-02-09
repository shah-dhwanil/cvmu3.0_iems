from uuid import UUID
from pydantic import BaseModel, EmailStr, Field


# Create operations
class CreateParentRequest(BaseModel):
    id: UUID
    student_id: UUID
    father_name: str = Field(..., max_length=32)
    mother_name: str = Field(..., max_length=32)
    contact_no: str = Field(..., max_length=16)
    email_id: EmailStr = Field(..., max_length=32)


class GetParentResponse(BaseModel):
    id: UUID
    student_id: UUID
    father_name: str = Field(..., max_length=32)
    mother_name: str = Field(..., max_length=32)
    contact_no: str = Field(..., max_length=16)
    email_id: EmailStr = Field(..., max_length=32)
    active: bool


class GetAllParentsResponse(BaseModel):
    class Parent(BaseModel):
        id: UUID
        student_id: UUID
        father_name: str
        mother_name: str

    parents: list[Parent]


# Update operations
class UpdateParentRequest(BaseModel):
    father_name: str = Field(None, max_length=32)
    mother_name: str = Field(None, max_length=32)
    contact_no: str = Field(None, max_length=16)
    email_id: EmailStr = Field(None, max_length=32)


class DeleteParentRequest(BaseModel):
    id: UUID


class EmptyResponse(BaseModel):
    pass


# Error responses
class ParentAlreadyExistsResponse(BaseModel):
    error: str = "duplicate_parent"
    message: str = "A parent with this student ID already exists"


class ParentNotFoundResponse(BaseModel):
    error: str = "parent_not_found"
    message: str = "Parent not found"

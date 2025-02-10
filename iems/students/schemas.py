from uuid import UUID
from pydantic import BaseModel, EmailStr, Field


# Create operations
class CreateStudentRequest(BaseModel):
    id: UUID
    first_name: str = Field(..., max_length=32)
    last_name: str = Field(..., max_length=32)
    enrollment_id: str = Field(..., max_length=16)
    gender: str = Field(..., max_length=1)
    contact_no: str = Field(..., max_length=16)
    email_id: EmailStr = Field(..., max_length=32)
    batch_id: UUID
    current_sem: UUID


class GetStudentResponse(BaseModel):
    id: UUID
    first_name: str = Field(..., max_length=32)
    last_name: str = Field(..., max_length=32)
    enrollment_id: str = Field(..., max_length=16)
    gender: str = Field(..., max_length=1)
    contact_no: str = Field(..., max_length=16)
    email_id: EmailStr = Field(..., max_length=32)
    active: bool


class GetAllStudentsResponse(BaseModel):
    class Student(BaseModel):
        id: UUID
        enrollment_id: str
        name: str

    students: list[Student]


# Update operations
class UpdateStudentRequest(BaseModel):
    first_name: str = Field(None, max_length=32)
    last_name: str = Field(None, max_length=32)
    enrollment_id: str = Field(None, max_length=16)
    gender: str = Field(None, max_length=1)
    contact_no: str = Field(None, max_length=16)
    email_id: EmailStr = Field(None, max_length=32)


class UpdateStudentCurrentSemRequest(BaseModel):
    branch_id: UUID
    current_sem: UUID


class EmptyResponse(BaseModel):
    pass


# Error responses
class StudentAlreadyExistsResponse(BaseModel):
    error: str = "duplicate_student"
    message: str = (
        "A student with this email, enrollment ID or mobile no already exists"
    )


class StudentNotFoundResponse(BaseModel):
    error: str = "student_not_found"
    message: str = "Student not found"

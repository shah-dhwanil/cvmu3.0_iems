from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field


# Create operations
class CreateStaffRequest(BaseModel):
    id: UUID
    first_name: str = Field(..., max_length=32)
    last_name: str = Field(..., max_length=32)
    contact_no: str = Field(..., max_length=16)
    email_id: EmailStr = Field(..., max_length=32)
    qualification: Optional[str]
    experience: Optional[str]


class GetStaffResponse(BaseModel):
    id: UUID
    first_name: str = Field(..., max_length=32)
    last_name: str = Field(..., max_length=32)
    contact_no: str = Field(..., max_length=16)
    email_id: EmailStr = Field(..., max_length=32)
    qualification: Optional[str]
    experience: Optional[str]
    active: bool


class GetAllStaffResponse(BaseModel):
    class Staff(BaseModel):
        id: UUID
        name: str

    staff_members: list[Staff]


# Update operations
class UpdateStaffRequest(BaseModel):
    first_name: str = Field(None, max_length=32)
    last_name: str = Field(None, max_length=32)
    contact_no: str = Field(None, max_length=16)
    email_id: EmailStr = Field(None, max_length=32)
    qualification: Optional[str]
    experience: Optional[str]


class EmptyResponse(BaseModel):
    pass


# Error responses
class StaffAlreadyExistsResponse(BaseModel):
    error: str = "duplicate_staff"
    message: str = "A staff member with this email or mobile no already exists"


class StaffNotFoundResponse(BaseModel):
    error: str = "staff_not_found"
    message: str = "Staff member not found"

from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from enum import Enum
from datetime import date


class LeaveStatusEnum(str, Enum):
    SUBMITTED = "submitted"
    DECLINED_COUNCILLER = "declined_counciller"
    APPROVED_COUNCILLER = "approved_counciller"
    DECLINED_HOD = "declined_hod"
    APPROVED = "approved"


class CreateLeaveRequest(BaseModel):
    student_id: UUID
    from_date: date
    to_date: date 
    reason: str
    document_id: Optional[UUID] = None


class CreateLeaveResponse(BaseModel):
    id: UUID


class GetLeaveResponse(BaseModel, use_enum_values=True):
    id: UUID
    student_id: UUID
    student_name: str
    from_date: date
    to_date: date
    reason: str
    status: LeaveStatusEnum
    document_id: Optional[UUID]


class GetLeaveByStudentResponse(BaseModel):
    leaves: list[GetLeaveResponse]


class UpdateLeaveRequest(BaseModel):
    from_date: Optional[date] = Field(None, alias="from")
    to_date: Optional[date] = Field(None, alias="to")
    reason: Optional[str] = None
    document_id: Optional[UUID] = None


class UpdateLeaveStatusRequest(BaseModel):
    accepted: bool


class LeaveNotFoundResponse(BaseModel):
    error: str = "leave_not_found"
    message: str = "Leave not found"

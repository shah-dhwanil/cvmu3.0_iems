from pydantic import BaseModel, Field
from typing import Any, Optional
from uuid import UUID
from enum import Enum


class RoleEnum(str, Enum):
    admin = "admin"
    principal = "principal"
    hod = "hod"
    academic_staff = "academic_staff"
    teacher = "teacher"
    student = "student"
    parents = "parents"
    account_staff = "account_staff"
    others = "others"


class CreateUserRequest(BaseModel, use_enum_values=True):
    username: str = Field(..., max_length=32)
    password: str = Field(..., min_length=8)
    role: RoleEnum
    active: Optional[bool] = True


class CreateUserResponse(BaseModel):
    id: UUID


class GetUserRequest(BaseModel):
    id: UUID


class GetUserResponse(BaseModel):
    id: UUID
    username: str
    role: RoleEnum
    active: bool


class UpdateUserRoleRequest(BaseModel, use_enum_values=True):
    role: RoleEnum


class UpdateUserPasswordRequest(BaseModel):
    password: str = Field(..., min_length=8)


class DeleteUserRequest(BaseModel):
    id: UUID


class UsernameAlreadyExistsResponse(BaseModel):
    error_slug: str = "duplicate_username"
    error: str = "A user with this username already exists"
    # status_code: int = 409
    context: dict[str, Any]


class EmptyResponse(BaseModel): ...

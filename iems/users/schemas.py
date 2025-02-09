from pydantic import BaseModel, Field
from typing import Any, Optional
from uuid import UUID
from enum import Enum


class RoleEnum(str, Enum):
    ADMIN = "admin"
    PRINCIPAL = "principal"
    HOD = "hod"
    ACADEMIC_STAFF = "academic_staff"
    TEACHER = "teacher"
    STUDENT = "student"
    PARENTS = "parents"
    ACCOUNT_STAFF = "account_staff"
    OTHERS = "others"


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

from decimal import Decimal
from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from enum import Enum


class PlacementStatus(str, Enum):
    OFFERED = "offered"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class CreatePlacementRequest(BaseModel, use_enum_values=True):
    student_id: UUID
    company_name: str = Field(..., max_length=64)
    role: str = Field(..., max_length=64)
    package: Decimal = Field(..., decimal_places=2)
    status: Optional[PlacementStatus] = PlacementStatus.OFFERED
    letter_uid: Optional[UUID] = None


class CreatePlacementResponse(BaseModel):
    id: UUID


class GetPlacementResponse(BaseModel):
    id: UUID
    student_id: UUID
    company_name: str
    role: str
    package: float
    status: PlacementStatus
    letter_uid: Optional[UUID]


class GetPlacementByStudentResponse(BaseModel):
    placements : list[GetPlacementResponse]


class UpdatePlacementRequest(BaseModel):
    company_name: str = Field(max_length=64)
    role: str = Field(max_length=64)
    package: float = Field(decimal_places=2)
    letter_uid: UUID


class UpdatePlacementStatusRequest(BaseModel, use_enum_values=True):
    status: PlacementStatus


class PlacementNotFoundResponse(BaseModel):
    error: str = "placement_not_found"
    message: str = "Placement not found"


class EmptyResponse(BaseModel): ...

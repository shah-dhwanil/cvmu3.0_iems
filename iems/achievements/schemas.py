from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from enum import Enum


class AchievementTypeEnum(str, Enum):
    ACADEMIC = "academic"
    SPORTS = "sports"
    CULTURAL = "cultural"
    OTHER = "other"


class AchievementRankEnum(str, Enum):
    PARTICIPATION = "participation"
    FIRST = "first"
    SECOND = "second"
    THIRD = "third"
    OTHERS = "others"


class CreateAchievementRequest(BaseModel, use_enum_values=True):
    student_id: Optional[UUID]
    name: str = Field(..., max_length=32)
    type: AchievementTypeEnum
    pos: AchievementRankEnum
    docs_id: Optional[UUID] = None


class CreateAchievementResponse(BaseModel):
    id: UUID


class GetAchievementResponse(BaseModel, use_enum_values=True):
    id: UUID
    student_id: UUID
    name: str
    type: AchievementTypeEnum
    pos: AchievementRankEnum
    docs_id: Optional[UUID]


class GetAchievementByStudentResponse(BaseModel, use_enum_values=True):
    achievements: list[GetAchievementResponse]


class UpdateAchievementRequest(BaseModel, use_enum_values=True):
    name: str = Field(max_length=32)
    type: AchievementTypeEnum
    pos: AchievementRankEnum
    docs_id: UUID


class AchievementNotFoundResponse(BaseModel):
    error: str = "achievement_not_found"
    message: str = "Achievement not found"


class EmptyResponse(BaseModel): ...

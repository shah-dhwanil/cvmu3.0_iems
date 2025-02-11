from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from enum import Enum
from datetime import datetime

class ResourceTypeEnum(str, Enum):
    LECTURE_NOTES = "lecture_notes"
    LAB_MANUAL = "lab_manual"
    BOOKS = "books"
    REFERENCE_MATERIAL = "reference_material"
    SYLLABUS = "syllabus"
    OTHERS = "others"


class CreateResourceRequest(BaseModel,use_enum_values=True):
    subject_id: UUID
    title: str
    shared_by: Optional[UUID]
    type: ResourceTypeEnum
    docs_id: UUID


class CreateResourceResponse(BaseModel):
    id: UUID


class GetResourceResponse(BaseModel,use_enum_values=True):
    id: UUID
    subject_id: UUID
    title: str
    shared_at: datetime
    shared_by: UUID
    type: ResourceTypeEnum
    docs_id: UUID

class GetResourceBySubject(BaseModel):
    resources: list[GetResourceResponse]


class UpdateResourceRequest(BaseModel,use_enum_values=True):
    title: str
    type:ResourceTypeEnum


class ResourceNotFoundResponse(BaseModel):
    error: str = "resource_not_found"
    message: str = "Resource not found"


class EmptyResponse(BaseModel):
    ...
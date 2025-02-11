from pydantic import BaseModel, Field
from typing import Any, Optional
from uuid import UUID
from datetime import datetime

class CreateCourseRequest(BaseModel):
    sem_id: UUID
    subject_id: UUID
    taught_by: UUID


class CreateCourseResponse(BaseModel):
    id: UUID


class GetCourseRequest(BaseModel):
    id: UUID


class GetCourseResponse(BaseModel):
    id: UUID
    sem_id: UUID
    subject_id: UUID
    taught_by: UUID
    active: bool

class GetCourseTaughtBy(BaseModel):
    id:UUID
    name:str
    branch:str
    year:int

class GetCourseTaughtByResponse(BaseModel):
    courses: list[GetCourseTaughtBy]

class UpdateCourseRequest(BaseModel):
    sem_id: UUID
    subject_id: UUID
    taught_by: UUID


class CourseNotFoundResponse(BaseModel):
    error: str = "course_not_found"
    message: str = "Course not found"


class EmptyResponse(BaseModel): ...
from pydantic import BaseModel
from uuid import UUID


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


class GetCourseTaughtBy(BaseModel):
    id: UUID
    name: str
    sem_id:UUID
    branch: str
    year: int



class GetCouseByStudentId(BaseModel):
    class Course(BaseModel):
        id: UUID
        name: str
        by: UUID

    courses: list[Course]


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

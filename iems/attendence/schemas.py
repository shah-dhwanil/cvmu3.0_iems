from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class MarkAttendence(BaseModel):
    course_id: UUID
    class_time: datetime
    present_student_ids: list[UUID]
    absent_student_ids: list[UUID]


class GetAttendenceByCourseIdAndClassTimeResponse(BaseModel):
    class AttendenceRecord(BaseModel):
        id: UUID
        student_id: UUID
        present: bool
        dont_care: bool

    attendence_records: list[AttendenceRecord]


class GetAttendenceByStudentId(BaseModel):
    class AttendenceRecord(BaseModel):
        course_id: UUID
        present_no: int
        dont_care_no: int
        total_no: int

    attendence_records: list[AttendenceRecord]


class UpdateAttendence(BaseModel):
    id: UUID
    present: bool


class EmptyResponse(BaseModel):
    pass

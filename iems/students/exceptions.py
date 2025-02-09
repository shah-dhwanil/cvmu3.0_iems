from iems.base.exceptions import IEMSException


class StudentAlreadyExistsError(IEMSException):
    error: str = "duplicate_student"
    message: str = (
        "A student with this email, enrollment ID or mobile no already exists"
    )


class StudentNotFoundError(IEMSException):
    error: str = "student_not_found"
    message: str = "Student not found"

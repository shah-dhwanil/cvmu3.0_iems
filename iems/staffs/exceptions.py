from iems.base.exceptions import IEMSException


class StaffAlreadyExistsError(IEMSException):
    error: str = "duplicate_staff"
    message: str = "A staff member with this email or mobile no already exists"


class StaffNotFoundError(IEMSException):
    error: str = "staff_not_found"
    message: str = "Staff member not found"

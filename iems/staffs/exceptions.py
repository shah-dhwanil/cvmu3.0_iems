from iems.base.exceptions import IEMSException


class StaffAlreadyExistsError(IEMSException):
    error: str = "duplicate_staff"
    message: str = "A staff member with this email or mobile no already exists"


class UserNotFoundError(IEMSException):
    error: str = "user_not_found"
    message: str = "User member not found"

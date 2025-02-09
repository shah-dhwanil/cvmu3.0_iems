from iems.base.exceptions import IEMSException


class ParentAlreadyExistsError(IEMSException):
    error: str = "duplicate_parent"
    message: str = "A parent with this student ID already exists"


class ParentNotFoundError(IEMSException):
    error: str = "parent_not_found"
    message: str = "Parent not found"

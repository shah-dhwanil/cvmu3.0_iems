from iems.base.exceptions import IEMSException


class SemisterNotFoundError(IEMSException):
    slug = "semister_not_found"
    description = "Semister not found"

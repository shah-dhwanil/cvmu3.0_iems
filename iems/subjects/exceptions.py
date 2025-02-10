from iems.base.exceptions import IEMSException


class SubjectNotFoundResponse(IEMSException):
    slug = "subject_not_found"
    description = "Subject not found"

from iems.base.exceptions import IEMSException


class BatchNotFoundError(IEMSException):
    slug = "batch_not_found"
    description = "Batch not found"

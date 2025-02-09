from iems.base.exceptions import IEMSException


class UsernameAlreadyExistsException(IEMSException):
    slug = "duplicate_username"
    description = "A user with this username already exists"

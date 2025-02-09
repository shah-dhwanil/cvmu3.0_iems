from iems.base.exceptions import IEMSException


class UsernameAlreadyExistsException(IEMSException):
    slug = "duplicate_username"
    description = "A user with this username already exists"


class UserNotFoundException(IEMSException):
    error: str = "user_not_found"
    message: str = "User not found"

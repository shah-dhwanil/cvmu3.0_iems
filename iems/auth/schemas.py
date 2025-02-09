from uuid import UUID
from pydantic import BaseModel, Field
from datetime import datetime, timezone


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    token: str
    role: str


class TokenPayload(BaseModel):
    user_id: UUID
    role: str
    exp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class InvalidCredentials(BaseModel):
    error: str = "invalid_credentials"
    message: str = "The provided credentials are invalid"


class TokenNotFound(BaseModel):
    error: str = "token_not_found"
    message: str = "Authentication token was not provided"


class TokenExpired(BaseModel):
    error: str = "token_expired"
    message: str = "Authentication token has expired"


class InvalidToken(BaseModel):
    error: str = "invalid_token"
    message: str = "Authentication token is invalid"


class AccessDenied(BaseModel):
    error: str = "access_denied"
    message: str = "Access denied. You do not have the required permissions to access this resource"

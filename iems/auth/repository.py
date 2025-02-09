from typing import Optional
from uuid import UUID
from argon2 import PasswordHasher
from argon2.exceptions import VerificationError, VerifyMismatchError
from iems.base.postgres import PGConnection
from iems.auth.schemas import LoginRequest, LoginResponse, TokenPayload

class AuthRepository:
    @staticmethod
    async def authenticate_user(login_request: LoginRequest) -> Optional[TokenPayload]:
        ph = PasswordHasher()
        async with PGConnection.get_connection() as conn:
            row = await conn.fetchrow(
                """
                SELECT id, password, role, active
                FROM users
                WHERE username = $1;
                """,
                login_request.username,
            )
            
            if not row or not row['active']:
                return None
                
            try:
                if ph.verify(row['password'], login_request.password):
                    return TokenPayload(
                        user_id=row['id'],
                        role=row['role']
                    )
            except VerificationError :
                return None
            except VerifyMismatchError:
                return None
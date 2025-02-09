from sanic import Request
from pyseto import DecryptError, Key, VerifyError, decode
from datetime import datetime, timezone
from iems.auth.schemas import InvalidToken, TokenNotFound, TokenExpired, TokenPayload
from iems.base.config import Config
from iems.base.response import JSONResponse

# Use the same secret key as in views.py
SECRET_KEY = Key.new(version=4, purpose="local", key=Config.get_config().PASETO_SECRET_KEY)

def auth_middleware(request: Request):
    """
    Middleware to verify PASETO token
    """
    # Skip authentication for certain endpoints if needed
    
    if request.endpoint in Config.get_config().PUBLIC_ROUTES:  # Add your public endpoints
        request.ctx.user = None
        return
    token = request.token
    if not token:
        return JSONResponse(TokenNotFound().model_dump_json(), 401)
    try:
        # Decode and verify token
        payload = decode(SECRET_KEY, token)
        token_data = TokenPayload.model_validate_json(payload.payload)
        # Check if token is expired
        if token_data.exp < datetime.now(timezone.utc):
            return JSONResponse(TokenExpired().model_dump_json(), 401)
        # Add token data to request for use in route handlers
        request.ctx.user = token_data
    except DecryptError as e:
        return JSONResponse(InvalidToken().model_dump_json(), 401)
    except VerifyError as e:
        return JSONResponse(InvalidToken().model_dump_json(), 401)

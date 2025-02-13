from pyseto import Key, encode
from datetime import datetime, timedelta
from datetime import timezone
from iems.auth.blueprint import auth_bp
from iems.auth.schemas import LoginRequest, LoginResponse, InvalidCredentials
from iems.auth.repository import AuthRepository
from iems.base.config import Config
from iems.base.decorators import validate
from iems.base.response import JSONResponse

# Secret key for PASETO token (in production, use secure key management)
SECRET_KEY = Key.new(
    version=4, purpose="local", key=Config.get_config().PASETO_SECRET_KEY
)


@auth_bp.post("/login")
@validate(body=LoginRequest)
async def login(request, data: LoginRequest, **_):
    """Handle user login and return PASETO token"""
    # Authenticate user
    token_payload = await AuthRepository.authenticate_user(data)
    if not token_payload:
        return JSONResponse(InvalidCredentials().model_dump_json(), 401)
    token_payload.exp = datetime.now(timezone.utc) + timedelta(hours=15)
    token = encode(SECRET_KEY, token_payload.model_dump_json())
    return JSONResponse(
        LoginResponse(token=token, role=token_payload.role,user_id=token_payload.user_id).model_dump_json(), 200
    )

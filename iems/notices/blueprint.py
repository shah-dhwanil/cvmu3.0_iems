from sanic import Blueprint

# Create a blueprint for user routes with API version v1 and common URI /users
notices_bp = Blueprint("notices", url_prefix="/notices", version=1)

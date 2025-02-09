from sanic import Blueprint

# Create a blueprint for user routes with API version v1 and common URI /users
users_bp = Blueprint("users", url_prefix="/users", version=1)

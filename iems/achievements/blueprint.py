from sanic import Blueprint

# Create a blueprint for user routes with API version v1 and common URI /users
achievements_bp = Blueprint("achievements", url_prefix="/achievements", version=1)

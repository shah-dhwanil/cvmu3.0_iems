from sanic import Blueprint

# Create a blueprint for user routes with API version v1 and common URI /users
parent_bp = Blueprint("parents", url_prefix="/parents", version=1)

from sanic import Blueprint

# Create a blueprint for user routes with API version v1 and common URI /users
staff_bp = Blueprint("staff", url_prefix="/staff", version=1)

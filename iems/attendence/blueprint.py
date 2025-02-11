from sanic import Blueprint

# Create a blueprint for user routes with API version v1 and common URI /users
attendence_bp = Blueprint("attendence", url_prefix="/attendence", version=1)

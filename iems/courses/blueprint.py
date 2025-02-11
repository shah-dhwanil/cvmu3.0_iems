from sanic import Blueprint

# Create a blueprint for user routes with API version v1 and common URI /users
courses_bp = Blueprint("courses", url_prefix="/courses", version=1)

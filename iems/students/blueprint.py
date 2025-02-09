from sanic import Blueprint

# Create a blueprint for user routes with API version v1 and common URI /users
student_bp = Blueprint("students", url_prefix="/students", version=1)

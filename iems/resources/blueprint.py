from sanic import Blueprint

# Create a blueprint for user routes with API version v1 and common URI /users
resources_bp = Blueprint("resources", url_prefix="/resources", version=1)

from sanic import Blueprint

# Create a blueprint for user routes with API version v1 and common URI /users
leave_bp = Blueprint("leave", url_prefix="/leave", version=1)

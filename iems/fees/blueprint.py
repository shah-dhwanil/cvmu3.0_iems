from sanic import Blueprint

# Create a blueprint for user routes with API version v1 and common URI /users
fees_bp = Blueprint("fees", url_prefix="/fees", version=1)

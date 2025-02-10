from sanic import Blueprint

# Create a blueprint for user routes with API version v1 and common URI /users
batch_bp = Blueprint("batch", url_prefix="/batch", version=1)

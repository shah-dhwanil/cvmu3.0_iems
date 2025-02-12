from sanic import Blueprint

# Create a blueprint for user routes with API version v1 and common URI /users
files_bp = Blueprint("files", url_prefix="/files", version=1)

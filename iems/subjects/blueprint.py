from sanic import Blueprint

# Create a blueprint for user routes with API version v1 and common URI /users
subjects_bp = Blueprint("subjects", url_prefix="/subjects", version=1)

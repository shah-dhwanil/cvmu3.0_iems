from sanic import Blueprint

# Create a blueprint for user routes with API version v1 and common URI /users
placements_bp = Blueprint("placements", url_prefix="/placements", version=1)

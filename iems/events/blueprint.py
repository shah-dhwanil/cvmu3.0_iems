from sanic import Blueprint

# Create a blueprint for user routes with API version v1 and common URI /users
events_bp = Blueprint("events", url_prefix="/events", version=1)

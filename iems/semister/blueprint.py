from sanic import Blueprint

# Create a blueprint for user routes with API version v1 and common URI /users
semister_bp = Blueprint("semister", url_prefix="/semister", version=1)

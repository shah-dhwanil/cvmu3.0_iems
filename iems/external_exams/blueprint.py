from sanic import Blueprint

# Create a blueprint for user routes with API version v1 and common URI /users
external_exams_bp = Blueprint("external_exams", url_prefix="/external_exams", version=1)

from sanic import Blueprint
# Create a blueprint for user routes with API version v1 and common URI /users
auth_bp = Blueprint('auth',url_prefix='/auth', version=1)
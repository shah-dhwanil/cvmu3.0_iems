from functools import wraps
from typing import List, Union
from sanic import Request
from iems.auth.schemas import AccessDenied, TokenNotFound
from iems.base.response import JSONResponse
from iems.users.schemas import RoleEnum


def require_roles(allowed_roles: Union[str, RoleEnum, List[str], List[RoleEnum]]):
    """
    Decorator to check if the current user has the required role(s)

    Args:
        allowed_roles: Single role string or list of role strings that are allowed to access the endpoint

    Returns:
        Decorator function that checks user roles
    """
    if isinstance(allowed_roles, str):
        allowed_roles = [allowed_roles]
    if isinstance(allowed_roles, RoleEnum):
        allowed_roles = [allowed_roles]

    def decorator(f):
        @wraps(f)
        async def decorated_function(request: Request, *args, **kwargs):
            # Check if user exists in request context (set by auth_middleware)
            if not hasattr(request.ctx, "user") or request.ctx.user is None:
                return JSONResponse(TokenNotFound().model_dump_json(), 401)

            # Check if user has any of the allowed roles
            user_role = request.ctx.user.role
            if user_role not in allowed_roles:
                return JSONResponse(AccessDenied().model_dump_json(), 403)

            # If role check passes, proceed to the handler
            return await f(request, *args, **kwargs)

        return decorated_function

    return decorator


def not_allowed_roles(
    not_allowed_roles: Union[str, RoleEnum, List[str], List[RoleEnum]],
):
    """
    Decorator to check if the current user does not have the specified role(s)

    Args:
        not_allowed_roles: Single role string or list of role strings that are not allowed to access the endpoint

    Returns:
        Decorator function that checks user roles
    """
    if isinstance(not_allowed_roles, str):
        not_allowed_roles = [not_allowed_roles]
    if isinstance(not_allowed_roles, RoleEnum):
        not_allowed_roles = [not_allowed_roles]

    def decorator(f):
        @wraps(f)
        async def decorated_function(request: Request, *args, **kwargs):
            # Check if user exists in request context
            if not hasattr(request.ctx, "user") or request.ctx.user is None:
                return JSONResponse(TokenNotFound().model_dump_json(), 401)

            # Check if user has any of the not allowed roles
            user_role = request.ctx.user.role
            if user_role in not_allowed_roles:
                return JSONResponse(AccessDenied().model_dump_json(), 403)

            # If role check passes, proceed to the handler
            return await f(request, *args, **kwargs)

        return decorated_function

    return decorator

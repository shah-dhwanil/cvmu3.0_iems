from uuid import UUID
from iems.users.blueprint import users_bp
from iems.users.exceptions import UsernameAlreadyExistsException
from iems.users.repository import UserRepository
from iems.base.decorators import validate
from iems.base.response import JSONResponse

from iems.users.schemas import (
    CreateUserRequest,
    CreateUserResponse,
    UpdateUserRoleRequest,
    UpdateUserPasswordRequest,
    UsernameAlreadyExistsResponse,
    EmptyResponse,
)


@users_bp.post("/")
@validate(body=CreateUserRequest)
async def create_user(request, data: CreateUserRequest, **_):
    try:
        user_id = await UserRepository.create_user(data)
        return JSONResponse(CreateUserResponse(id=user_id).model_dump_json(), 200)
    except UsernameAlreadyExistsException:
        return JSONResponse(UsernameAlreadyExistsResponse().model_dump_json(), 409)


@users_bp.get("/<user_id:uuid>")
async def get_user(request, user_id: UUID, **_):
    print(user_id)
    user = await UserRepository.get_user(user_id)
    if user is None:
        print(EmptyResponse().model_dump_json())
        return JSONResponse(EmptyResponse().model_dump_json(), 404)
    return JSONResponse(user.model_dump_json(), 200)


@users_bp.patch("/<user_id:uuid>/role")
@validate(body=UpdateUserRoleRequest)
async def update_user_role(request, user_id: UUID, data: UpdateUserRoleRequest, **_):
    success = await UserRepository.update_user_role(user_id, data)
    if not success:
        return JSONResponse(EmptyResponse().model_dump_json(), 404)
    return JSONResponse(EmptyResponse().model_dump_json(), 200)


@users_bp.patch("/<user_id:uuid>/password")
@validate(body=UpdateUserPasswordRequest)
async def update_user_password(
    request, user_id: UUID, data: UpdateUserPasswordRequest, **_
):
    success = await UserRepository.update_user_password(user_id, data)
    if not success:
        return JSONResponse(EmptyResponse().model_dump_json(), 404)
    return JSONResponse(EmptyResponse().model_dump_json(), 200)


@users_bp.delete("/<user_id:uuid>")
async def delete_user(request, user_id: UUID, **_):
    success = await UserRepository.delete_user(user_id)
    if not success:
        return JSONResponse(EmptyResponse().model_dump_json(), 404)
    return JSONResponse(EmptyResponse().model_dump_json(), 200)

from uuid import UUID
from iems.auth.schemas import AccessDenied
from iems.base.response import JSONResponse
from iems.base.decorators import validate
from iems.users.schemas import RoleEnum, UserNotFoundResponse
from iems.auth.decorators import require_roles, not_allowed_roles
from iems.parents.blueprint import parent_bp
from iems.parents.repository import ParentRepository
from iems.parents.exceptions import ParentAlreadyExistsError
from iems.users.exceptions import UserNotFoundException

from iems.parents.schemas import (
    CreateParentRequest,
    UpdateParentRequest,
    EmptyResponse,
    ParentAlreadyExistsResponse,
    ParentNotFoundResponse,
)


@parent_bp.post("/")
@require_roles([RoleEnum.ADMIN, RoleEnum.ACADEMIC_STAFF, RoleEnum.PRINCIPAL])
@validate(body=CreateParentRequest)
async def create_parent(request, data: CreateParentRequest, **_):
    """Create a new parent"""
    try:
        await ParentRepository.create_parent(data)
        return JSONResponse(EmptyResponse().model_dump_json(), 201)
    except ParentAlreadyExistsError:
        return JSONResponse(ParentAlreadyExistsResponse().model_dump_json(), 409)
    except UserNotFoundException:
        return JSONResponse(UserNotFoundResponse().model_dump_json(), 404)


@parent_bp.get("/<parent_id:uuid>")
@not_allowed_roles([RoleEnum.STUDENT])
async def get_parent(request, parent_id: UUID):
    """Get parent by ID"""
    parent = await ParentRepository.get_parent(parent_id)
    if parent:
        return JSONResponse(parent.model_dump_json(), 200)
    return JSONResponse(ParentNotFoundResponse().model_dump_json(), 404)


@parent_bp.get("/student/<student_id:uuid>")
@not_allowed_roles([RoleEnum.PARENTS])
async def get_parent_by_student(request, student_id: UUID):
    """Get parent by student ID"""
    if request.ctx.user.role == RoleEnum.STUDENT:
        student_id = request.ctx.user.id
    parent = await ParentRepository.get_parent_by_student(student_id)
    if parent:
        return JSONResponse(parent.model_dump_json(), 200)
    return JSONResponse(ParentNotFoundResponse().model_dump_json(), 404)


@parent_bp.put("/<parent_id:uuid>")
@require_roles(
    [RoleEnum.ADMIN, RoleEnum.ACADEMIC_STAFF, RoleEnum.PRINCIPAL, RoleEnum.PARENTS]
)
@validate(body=UpdateParentRequest)
async def update_parent(request, parent_id: UUID, data: UpdateParentRequest, **_):
    """Update a parent"""
    if (
        request.ctx.user.role == RoleEnum.PARENTS
        and request.ctx.user.user_id != parent_id
    ):
        return JSONResponse(AccessDenied().model_dump_json(), 403)
    try:
        success = await ParentRepository.update_parent(parent_id, data)
        if success:
            return JSONResponse(EmptyResponse().model_dump_json(), 200)
        return JSONResponse(ParentNotFoundResponse().model_dump_json(), 404)
    except ParentAlreadyExistsError:
        return JSONResponse(ParentAlreadyExistsResponse().model_dump_json(), 409)


@parent_bp.delete("/<parent_id:uuid>")
@require_roles([RoleEnum.ADMIN, RoleEnum.ACADEMIC_STAFF, RoleEnum.PRINCIPAL])
async def delete_parent(request, parent_id: UUID):
    """Delete a parent"""
    success = await ParentRepository.delete_parent(parent_id)
    if success:
        return JSONResponse(EmptyResponse().model_dump_json(), 200)
    return JSONResponse(ParentNotFoundResponse().model_dump_json(), 404)

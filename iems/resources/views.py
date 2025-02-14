from uuid import UUID
from iems.resources.blueprint import resources_bp
from iems.base.decorators import validate
from iems.base.response import JSONResponse
from iems.auth.decorators import not_allowed_roles
from iems.users.schemas import RoleEnum
from iems.resources.repository import ResourceRepository

from iems.resources.schemas import (
    CreateResourceRequest,
    CreateResourceResponse,
    UpdateResourceRequest,
    ResourceNotFoundResponse,
    GetResourceBySubject,
    EmptyResponse,
)


@resources_bp.post("/")
@not_allowed_roles([RoleEnum.STUDENT, RoleEnum.PARENTS])
@validate(body=CreateResourceRequest)
async def create_resource(request, data: CreateResourceRequest, **_):
    resource_id = await ResourceRepository.create_resource(data)
    return JSONResponse(CreateResourceResponse(id=resource_id).model_dump_json(), 200)


@resources_bp.get("/<resource_id:uuid>")
async def get_resource(request, resource_id: UUID, **_):
    resource = await ResourceRepository.get_resource(resource_id)
    if resource is None:
        return JSONResponse(ResourceNotFoundResponse().model_dump_json(), 404)
    return JSONResponse(resource.model_dump_json(), 200)


@resources_bp.get("/subject/<subject_id:uuid>")
async def get_resources_by_subject(request, subject_id: UUID, **_):
    resources = await ResourceRepository.get_resources_by_subject(subject_id)
    return JSONResponse(
        GetResourceBySubject(resources=resources).model_dump_json(), 200
    )


@resources_bp.patch("/<resource_id:uuid>")
@not_allowed_roles([RoleEnum.STUDENT, RoleEnum.PARENTS])
@validate(body=UpdateResourceRequest)
async def update_resource(request, resource_id: UUID, data: UpdateResourceRequest, **_):
    success = await ResourceRepository.update_resource(resource_id, data)
    if not success:
        return JSONResponse(ResourceNotFoundResponse().model_dump_json(), 404)
    return JSONResponse(EmptyResponse().model_dump_json(), 200)


@resources_bp.delete("/<resource_id:uuid>")
@not_allowed_roles([RoleEnum.STUDENT, RoleEnum.PARENTS])
async def delete_resource(request, resource_id: UUID, **_):
    success = await ResourceRepository.delete_resource(resource_id)
    if not success:
        return JSONResponse(ResourceNotFoundResponse().model_dump_json(), 404)
    return JSONResponse(EmptyResponse().model_dump_json(), 200)

@resources_bp.get("/staff/<staff_id:uuid>")
async def get_resources_by_staff(request, staff_id: UUID, **_):
    resources = await ResourceRepository.get_resources_by_teacher(staff_id)
    return JSONResponse(
        GetResourceBySubject(resources=resources).model_dump_json(), 200
    )
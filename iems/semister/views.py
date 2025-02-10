from uuid import UUID
from iems.batch.exceptions import BatchNotFoundError
from iems.batch.schemas import BatchNotFoundResponse
from iems.semister.repository import SemisterRepository
from iems.semister.blueprint import semister_bp
from iems.base.decorators import validate
from iems.base.response import JSONResponse
from iems.auth.decorators import not_allowed_roles, require_roles
from iems.users.schemas import RoleEnum

from iems.semister.schemas import (
    CreateSemisterRequest,
    CreateSemisterResponse,
    UpdateSemisterRequest,
    SemisterNotFoundResponse,
    EmptyResponse,
)


@semister_bp.post("/")
@require_roles([RoleEnum.ADMIN, RoleEnum.PRINCIPAL, RoleEnum.ACADEMIC_STAFF])
@validate(body=CreateSemisterRequest)
async def create_semister(request, data: CreateSemisterRequest, **_):
    try:
        semister_id = await SemisterRepository.create_semister(data)
        return JSONResponse(
            CreateSemisterResponse(id=semister_id).model_dump_json(), 200
        )
    except BatchNotFoundError:
        return JSONResponse(BatchNotFoundResponse().model_dump_json(), 404)


@semister_bp.get("/<semister_id:uuid>")
@not_allowed_roles([RoleEnum.STUDENT, RoleEnum.PARENT])
async def get_semister(request, semister_id: UUID, **_):
    semister = await SemisterRepository.get_semister(semister_id)
    if semister is None:
        return JSONResponse(SemisterNotFoundResponse().model_dump_json(), 404)
    return JSONResponse(semister.model_dump_json(), 200)


@semister_bp.patch("/<semister_id:uuid>")
@require_roles([RoleEnum.ADMIN, RoleEnum.PRINCIPAL, RoleEnum.ACADEMIC_STAFF])
@validate(body=UpdateSemisterRequest)
async def update_semister(request, semister_id: UUID, data: UpdateSemisterRequest, **_):
    success = await SemisterRepository.update_semister(semister_id, data)
    if not success:
        return JSONResponse(SemisterNotFoundResponse().model_dump_json(), 404)
    return JSONResponse(EmptyResponse().model_dump_json(), 200)


@semister_bp.delete("/<semister_id:uuid>")
@require_roles([RoleEnum.ADMIN, RoleEnum.PRINCIPAL, RoleEnum.ACADEMIC_STAFF])
async def delete_semister(request, semister_id: UUID, **_):
    success = await SemisterRepository.delete_semister(semister_id)
    if not success:
        return JSONResponse(SemisterNotFoundResponse().model_dump_json(), 404)
    return JSONResponse(EmptyResponse().model_dump_json(), 200)

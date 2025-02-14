from uuid import UUID
from iems.auth.schemas import AccessDenied
from iems.fees.blueprint import fees_bp
from iems.fees.repository import FeesRepository
from iems.base.decorators import validate
from iems.base.response import JSONResponse
from iems.auth.decorators import require_roles
from iems.users.schemas import RoleEnum

from iems.fees.schemas import (
    CreateFeesRequest,
    UpdateFeesRequest,
    FeesNotFoundResponse,
    EmptyResponse,
    UpdateFeesStatusRequest,
)


@fees_bp.post("/")
@require_roles([RoleEnum.ADMIN, RoleEnum.PRINCIPAL, RoleEnum.ACCOUNT_STAFF, RoleEnum.STUDENT])
@validate(body=CreateFeesRequest)
async def create_fees(request, data: CreateFeesRequest, **_):
    response = await FeesRepository.create_fees(data)
    return JSONResponse(response.model_dump_json(), 200)


@fees_bp.get("/<fees_id:uuid>")
async def get_fees(request, fees_id: UUID, **_):
    fees = await FeesRepository.get_fees(fees_id)
    if fees is None:
        return JSONResponse(FeesNotFoundResponse().model_dump_json(), 404)
    return JSONResponse(fees.model_dump_json(), 200)


@fees_bp.get("/student/<student_id:uuid>")
async def get_fees_by_student(request, student_id: UUID, **_):
    if (
        request.ctx.user.role == RoleEnum.STUDENT
        and request.ctx.user.user_id != student_id
    ):
        return JSONResponse(AccessDenied().model_dump_json(), 403)
    fees = await FeesRepository.get_fees_by_student(student_id)
    return JSONResponse(fees.model_dump_json(), 200)


@fees_bp.patch("/<fees_id:uuid>")
@require_roles([RoleEnum.ADMIN, RoleEnum.PRINCIPAL, RoleEnum.ACCOUNT_STAFF])
@validate(body=UpdateFeesRequest)
async def update_fees(request, fees_id: UUID, data: UpdateFeesRequest, **_):
    success = await FeesRepository.update_fees(fees_id, data)
    if not success:
        return JSONResponse(FeesNotFoundResponse().model_dump_json(), 404)
    return JSONResponse(EmptyResponse().model_dump_json(), 200)


@fees_bp.delete("/<fees_id:uuid>")
@require_roles([RoleEnum.ADMIN, RoleEnum.PRINCIPAL, RoleEnum.ACCOUNT_STAFF])
async def delete_fees(request, fees_id: UUID, **_):
    success = await FeesRepository.delete_fees(fees_id)
    if not success:
        return JSONResponse(FeesNotFoundResponse().model_dump_json(), 404)
    return JSONResponse(EmptyResponse().model_dump_json(), 200)
@fees_bp.get("/pending/")
@require_roles([RoleEnum.ADMIN, RoleEnum.PRINCIPAL, RoleEnum.ACCOUNT_STAFF])
async def get_pending_fees(request, **_):
    fees = await FeesRepository.get_pending_fees()
    return JSONResponse(fees.model_dump_json(), 200)

@fees_bp.patch("/<fees_id:uuid>/status")
@require_roles([RoleEnum.ADMIN, RoleEnum.PRINCIPAL, RoleEnum.ACCOUNT_STAFF])
@validate(body=UpdateFeesStatusRequest)
async def update_fees_status(request, fees_id: UUID, data: UpdateFeesStatusRequest, **_):
    if data.accepted:
        success = await FeesRepository.update_fees_status(fees_id, "ACCEPTED")
    else:
        success = await FeesRepository.update_fees_status(fees_id, "REJECTED")
    if not success:
        return JSONResponse(FeesNotFoundResponse().model_dump_json(), 404)
    return JSONResponse(EmptyResponse().model_dump_json(), 200)
from uuid import UUID
from iems.batch.repository import BatchRepository
from iems.base.decorators import validate
from iems.base.response import JSONResponse
from iems.auth.decorators import not_allowed_roles, require_roles
from iems.staffs.exceptions import StaffNotFoundError
from iems.staffs.schemas import StaffNotFoundResponse
from iems.users.schemas import RoleEnum
from iems.batch.blueprint import batch_bp
from iems.base.config import config

from iems.batch.schemas import (
    CreateBatchRequest,
    CreateBatchResponse,
    EmptyResponse,
    MultipleCreateBatchResponse,
    UpdateBatchRequest,
    BatchNotFoundResponse,
)


@batch_bp.post("/")
@require_roles([RoleEnum.ADMIN, RoleEnum.PRINCIPAL, RoleEnum.ACADEMIC_STAFF])
@validate(body=CreateBatchRequest)
async def create_batch(request, data: CreateBatchRequest, **_):
    try:
        batch_id = await BatchRepository.create_batch(data)
        return JSONResponse(CreateBatchResponse(id=batch_id).model_dump_json(), 200)
    except StaffNotFoundError:
        return JSONResponse(StaffNotFoundResponse().model_dump_json(), 404)


@batch_bp.post("/create_all/<year:int>")
@require_roles([RoleEnum.ADMIN, RoleEnum.PRINCIPAL])
async def create_batch_all(request, year: int, **_):
    created_batches = []
    for branch in config.BRANCH_LIST:
        try:
            batch_id = await BatchRepository.create_batch_all(year, branch)
            created_batches.append(CreateBatchResponse(id=batch_id))
        except StaffNotFoundError:
            return JSONResponse(StaffNotFoundResponse().model_dump_json(), 404)
    return JSONResponse(
        MultipleCreateBatchResponse(ids=create_batch).model_dump_json(), 200
    )


@batch_bp.get("/<batch_id:uuid>")
@not_allowed_roles([RoleEnum.STUDENT, RoleEnum.PARENTS])
async def get_batch(request, batch_id: UUID, **_):
    batch = await BatchRepository.get_batch(batch_id)
    if batch is None:
        return JSONResponse(BatchNotFoundResponse().model_dump_json(), 404)
    return JSONResponse(batch.model_dump_json(), 200)


@batch_bp.get("/<branch_name>/<year:int>")
@not_allowed_roles([RoleEnum.STUDENT, RoleEnum.PARENTS])
async def get_batch_by_branch_and_year(request, branch_name: str, year: int, **_):
    batch = await BatchRepository.get_batch_by_branch_and_year(branch_name, year)
    if batch is None:
        return JSONResponse(BatchNotFoundResponse().model_dump_json(), 404)
    return JSONResponse(batch.model_dump_json(), 200)


@batch_bp.patch("/<batch_id:uuid>")
@require_roles([RoleEnum.ADMIN, RoleEnum.PRINCIPAL, RoleEnum.ACADEMIC_STAFF])
@validate(body=UpdateBatchRequest)
async def update_batch(request, batch_id: UUID, data: UpdateBatchRequest, **_):
    success = await BatchRepository.update_batch(batch_id, data)
    if not success:
        return JSONResponse(BatchNotFoundResponse().model_dump_json(), 404)
    return JSONResponse(EmptyResponse().model_dump_json(), 200)


@batch_bp.delete("/<batch_id:uuid>")
@require_roles([RoleEnum.ADMIN, RoleEnum.PRINCIPAL, RoleEnum.ACADEMIC_STAFF])
async def delete_batch(request, batch_id: UUID, **_):
    success = await BatchRepository.delete_batch(batch_id)
    if not success:
        return JSONResponse(BatchNotFoundResponse().model_dump_json(), 404)
    return JSONResponse(EmptyResponse().model_dump_json(), 200)

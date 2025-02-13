from uuid import UUID
from iems.auth.schemas import AccessDenied
from iems.placements.repository import PlacementRepository
from iems.base.decorators import validate
from iems.base.response import JSONResponse
from iems.auth.decorators import not_allowed_roles, require_roles
from iems.users.schemas import RoleEnum
from iems.placements.blueprint import placements_bp

from iems.placements.schemas import (
    CreatePlacementRequest,
    CreatePlacementResponse,
    GetPlacementByStudentResponse,
    UpdatePlacementRequest,
    PlacementNotFoundResponse,
    EmptyResponse,
    UpdatePlacementStatusRequest,
    CreatePlacementEnrollRequest
)


@placements_bp.post("/")
@not_allowed_roles([RoleEnum.PARENTS])
@validate(body=CreatePlacementRequest)
async def create_placement(request, data: CreatePlacementRequest, **_):
    placement_id = await PlacementRepository.create_placement(data)
    return JSONResponse(CreatePlacementResponse(id=placement_id).model_dump_json(), 200)

@placements_bp.post("/enrollment")
@not_allowed_roles([RoleEnum.PARENTS])
@validate(body=CreatePlacementRequest)
async def create_enroll_placement(request, data:CreatePlacementEnrollRequest , **_):
    placement_id = await PlacementRepository.create_placement(data)
    return JSONResponse(CreatePlacementResponse(id=placement_id).model_dump_json(), 200)


@placements_bp.get("/<placement_id:uuid>")
async def get_placement(request, placement_id: UUID, **_):
    placement = await PlacementRepository.get_placement(placement_id)
    if placement is None:
        return JSONResponse(PlacementNotFoundResponse().model_dump_json(), 404)

    # Students can only view their own placements
    if (
        request.ctx.user.role == RoleEnum.STUDENT
        and request.ctx.user.user_id != placement.student_id
    ):
        return JSONResponse(AccessDenied().model_dump_json(), 403)

    return JSONResponse(placement.model_dump_json(), 200)

@placements_bp.get("/")
@not_allowed_roles([RoleEnum.PARENTS])
async def get_placements(request, **_):
    placements = await PlacementRepository.get_placement()
    return JSONResponse(GetPlacementByStudentResponse(placements=placements).model_dump_json(), 200)


@placements_bp.get("/student/<student_id:uuid>")
@not_allowed_roles([RoleEnum.PARENTS])
async def get_placements_by_student(request, student_id: UUID, **_):
    # Students can only view their own placements
    if (
        request.ctx.user.role == RoleEnum.STUDENT
        and request.ctx.user.user_id != student_id
    ):
        return JSONResponse(AccessDenied().model_dump_json(), 403)

    placements = await PlacementRepository.get_placements_by_student(student_id)
    return JSONResponse(GetPlacementByStudentResponse(placements=placements).model_dump_json(), 200)


@placements_bp.post("/status/<placement_id:uuid>")
#@not_allowed_roles([RoleEnum.PARENTS])
@require_roles([RoleEnum.STUDENT])
@validate(body=UpdatePlacementStatusRequest)
async def update_placement_status(
    request, placement_id: UUID, data: UpdatePlacementStatusRequest, **_
):
    success = await PlacementRepository.update_placement_status(placement_id, data)
    if not success:
        return JSONResponse(PlacementNotFoundResponse().model_dump_json(), 404)
    return JSONResponse(EmptyResponse().model_dump_json(), 200)

@placements_bp.patch("/<placement_id:uuid>")
@not_allowed_roles([RoleEnum.PARENTS])
@validate(body=UpdatePlacementRequest)
async def update_placement(
    request, placement_id: UUID, data: UpdatePlacementRequest, **_
):
    success = await PlacementRepository.update_placement(placement_id, data)
    if not success:
        return JSONResponse(PlacementNotFoundResponse().model_dump_json(), 404)
    return JSONResponse(EmptyResponse().model_dump_json(), 200)




@placements_bp.delete("/<placement_id:uuid>")
@not_allowed_roles([RoleEnum.PARENTS])
async def delete_placement(request, placement_id: UUID, **_):
    success = await PlacementRepository.delete_placement(placement_id)
    if not success:
        return JSONResponse(PlacementNotFoundResponse().model_dump_json(), 404)
    return JSONResponse(EmptyResponse().model_dump_json(), 200)

from uuid import UUID
from iems.notices.blueprint import notices_bp
from iems.notices.repository import NoticeRepository
from iems.base.decorators import validate
from iems.base.response import JSONResponse
from iems.auth.decorators import not_allowed_roles, require_roles
from iems.users.schemas import RoleEnum

from iems.notices.schemas import (
    CreateNoticeRequest,
    CreateNoticeResponse,
    EmptyResponse,
    UpdateNoticeRequest,
    NoticeNotFoundResponse,
    GetNoticesResponse,
    EmptyResponse,
)


@notices_bp.post("/")
@not_allowed_roles([RoleEnum.STUDENT, RoleEnum.PARENTS])
@validate(body=CreateNoticeRequest)
async def create_notice(request, data: CreateNoticeRequest, **_):
    data.created_by = request.ctx.user.user_id
    notice_id = await NoticeRepository.create_notice(data)
    return JSONResponse(
        CreateNoticeResponse(id=notice_id).model_dump_json(), 200
    )


@notices_bp.get("/<notice_id:uuid>")
async def get_notice(request, notice_id: UUID, **_):
    notice = await NoticeRepository.get_notice(notice_id)
    if notice is None:
        return JSONResponse(NoticeNotFoundResponse().model_dump_json(), 404)
    return JSONResponse(notice.model_dump_json(), 200)


@notices_bp.get("/")
async def get_notices(request, **_):
    notices = await NoticeRepository.get_notices()
    return JSONResponse(notices.model_dump_json(), 200)

@notices_bp.get("/batch/<batch_id:int>")
@require_roles([RoleEnum.STUDENT])
async def get_notices_by_batch(request, batch_id: int, **_):
    notices = await NoticeRepository.get_notices_by_target_audience_and_batch_id("student",batch_id)
    notices.append(await NoticeRepository.get_notices_by_target_audience_and_batch_id("student",None))
    notices.append(await NoticeRepository.get_notices_by_target_audience_and_batch_id(None,None))
    return JSONResponse(GetNoticesResponse(notices=notices).model_dump_json(), 200)

@notices_bp.get("/target/<target_audience:str>")
async def get_notices_by_target_audience(request, target_audience: str, **_):

    notices = await NoticeRepository.get_notices_by_target_audience_and_batch_id(target_audience,None)
    notices.append(await NoticeRepository.get_notices_by_target_audience_and_batch_id(None,None))
    if target_audience == "hod":
        notices.append(await NoticeRepository.get_notices_by_target_audience_and_batch_id("hod",None))
    elif target_audience == "academic_staff":
        notices.append(await NoticeRepository.get_notices_by_target_audience_and_batch_id("academic_staff",None))
    elif target_audience == "admin_staff":
        notices.append(await NoticeRepository.get_notices_by_target_audience_and_batch_id("admin_staff",None))
    return JSONResponse(GetNoticesResponse(notices=notices).model_dump_json(), 200)


@notices_bp.patch("/<notice_id:uuid>")
@not_allowed_roles([RoleEnum.STUDENT, RoleEnum.PARENTS])
@validate(body=UpdateNoticeRequest)
async def update_notice(
    request, notice_id: UUID, data: UpdateNoticeRequest, **_
):
    success = await NoticeRepository.update_notice(notice_id, data)
    if not success:
        return JSONResponse(NoticeNotFoundResponse().model_dump_json(), 404)
    return JSONResponse(EmptyResponse().model_dump_json(), 200)


@notices_bp.delete("/<notice_id:uuid>")
@not_allowed_roles([RoleEnum.STUDENT, RoleEnum.PARENTS])
async def delete_notice(request, notice_id: UUID, **_):
    success = await NoticeRepository.delete_notice(notice_id)
    if not success:
        return JSONResponse(NoticeNotFoundResponse().model_dump_json(), 404)
    return JSONResponse(EmptyResponse().model_dump_json(), 200)
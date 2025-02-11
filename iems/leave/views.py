from uuid import UUID
from iems.auth.schemas import AccessDenied
from iems.leave.blueprint import leave_bp
from iems.base.decorators import validate
from iems.base.response import JSONResponse
from iems.auth.decorators import require_roles
from iems.users.schemas import RoleEnum
from iems.leave.repository import LeaveRepository

from iems.leave.schemas import (
    CreateLeaveRequest,
    CreateLeaveResponse,
    GetLeaveByStudentResponse,
    UpdateLeaveRequest,
    UpdateLeaveStatusRequest,
    LeaveNotFoundResponse,
    LeaveStatusEnum,
)


@leave_bp.post("/")
@validate(body=CreateLeaveRequest)
@require_roles([RoleEnum.STUDENT])
async def create_leave(request, data: CreateLeaveRequest, **_):
    leave_id = await LeaveRepository.create_leave(data)
    return JSONResponse(CreateLeaveResponse(id=leave_id).model_dump_json(), 200)


@leave_bp.get("/<leave_id:uuid>")
async def get_leave(request, leave_id: UUID, **_):
    leave = await LeaveRepository.get_leave(leave_id)
    if leave is None:
        return JSONResponse(LeaveNotFoundResponse().model_dump_json(), 404)
    return JSONResponse(leave.model_dump_json(), 200)


@leave_bp.get("/student/<student_id:uuid>")
@require_roles([RoleEnum.STUDENT])
async def get_leaves_by_student(request, student_id: UUID, **_):
    if (
        request.ctx.user.role == RoleEnum.STUDENT
        and request.ctx.user.user_id != student_id
    ):
        return JSONResponse(AccessDenied().model_dump_json(), 403)
    leaves = await LeaveRepository.get_leaves_by_student(student_id)
    return JSONResponse(GetLeaveByStudentResponse(leaves=leaves).model_dump_json(), 200)


@leave_bp.get("/pending")
@require_roles([RoleEnum.HOD, RoleEnum.TEACHER])
async def get_pending_leaves_hod(request, **_):
    if request.ctx.user.role == RoleEnum.TEACHER:
        leaves = await LeaveRepository.get_pending_leaves_by_counciller(
            request.ctx.user.user_id
        )
    else:
        leaves = await LeaveRepository.get_pending_leaves_by_hod(
            request.ctx.user.user_id
        )
    return JSONResponse(GetLeaveByStudentResponse(leaves=leaves).model_dump_json(), 200)


@leave_bp.patch("/<leave_id:uuid>")
@validate(body=UpdateLeaveRequest)
async def update_leave(request, leave_id: UUID, data: UpdateLeaveRequest, **_):
    success = await LeaveRepository.update_leave(leave_id, data)
    if not success:
        return JSONResponse(LeaveNotFoundResponse().model_dump_json(), 404)
    return JSONResponse("{}", 200)


@leave_bp.patch("/<leave_id:uuid>/status")
@require_roles([RoleEnum.TEACHER, RoleEnum.HOD])
@validate(body=UpdateLeaveStatusRequest)
async def update_leave_status_counciller(
    request, leave_id: UUID, data: UpdateLeaveStatusRequest, **_
):
    if request.ctx.user.role == RoleEnum.TEACHER:
        if data.accepted:
            success = await LeaveRepository.update_leave_status(
                leave_id, LeaveStatusEnum.APPROVED_COUNCILLER
            )
        else:
            success = await LeaveRepository.update_leave_status(
                leave_id, LeaveStatusEnum.DECLINED_COUNCILLER
            )
    else:
        if data.accepted:
            success = await LeaveRepository.update_leave_status(
                leave_id, LeaveStatusEnum.APPROVED
            )
            await LeaveRepository.approve_leave(leave_id)
        else:
            success = await LeaveRepository.update_leave_status(
                leave_id, LeaveStatusEnum.DECLINED_HOD
            )
    if not success:
        return JSONResponse(LeaveNotFoundResponse().model_dump_json(), 404)
    return JSONResponse("{}", 200)


@leave_bp.delete("/<leave_id:uuid>")
async def delete_leave(request, leave_id: UUID, **_):
    success = await LeaveRepository.delete_leave(leave_id)
    if not success:
        return JSONResponse(LeaveNotFoundResponse().model_dump_json(), 404)
    return JSONResponse("{}", 200)

from uuid import UUID
from iems.auth.schemas import AccessDenied
from iems.base.response import JSONResponse
from iems.base.decorators import validate
from iems.users.exceptions import UserNotFoundException
from iems.users.schemas import RoleEnum, UserNotFoundResponse
from iems.auth.decorators import require_roles
from iems.staffs.blueprint import staff_bp
from iems.staffs.repository import StaffRepository
from iems.staffs.exceptions import StaffAlreadyExistsError
from iems.staffs.schemas import (
    CreateStaffRequest,
    UpdateStaffRequest,
    EmptyResponse,
    StaffAlreadyExistsResponse,
    StaffNotFoundResponse,
)


@staff_bp.post("/")
@require_roles([RoleEnum.ADMIN, RoleEnum.ACADEMIC_STAFF, RoleEnum.PRINCIPAL])
@validate(body=CreateStaffRequest)
async def create_staff(request, data: CreateStaffRequest, **_):
    """Create a new staff member"""
    try:
        await StaffRepository.create_staff(data)
        return JSONResponse(EmptyResponse().model_dump_json(), 201)
    except StaffAlreadyExistsError:
        return JSONResponse(StaffAlreadyExistsResponse().model_dump_json(), 409)
    except UserNotFoundException:
        return JSONResponse(UserNotFoundResponse().model_dump_json(), 404)


@staff_bp.get("/")
async def get_all_staff(request):
    """Get all staff members"""
    staff_list = await StaffRepository.get_all_staff()
    return JSONResponse(staff_list.model_dump_json(),200)


@staff_bp.get("/<staff_id:uuid>")
async def get_staff(request, staff_id: UUID = None):
    """Get staff member(s)"""
    staff = await StaffRepository.get_staff(staff_id)
    if staff:
        return JSONResponse(staff.model_dump_json(), 200)
    return JSONResponse(StaffNotFoundResponse().model_dump_json(), 404)


@staff_bp.put("/<staff_id:uuid>")
@require_roles(
    [
        RoleEnum.ADMIN,
        RoleEnum.ACADEMIC_STAFF,
        RoleEnum.PRINCIPAL,
        RoleEnum.TEACHER,
        RoleEnum.ACCOUNT_STAFF,
        RoleEnum.HOD,
    ]
)
@validate(body=UpdateStaffRequest)
async def update_staff(request, staff_id: UUID, data: UpdateStaffRequest, **_):
    """Update a staff member"""
    if (
        request.ctx.user.role not in [RoleEnum.ADMIN, RoleEnum.PRINCIPAL]
        and request.ctx.user.user_id != staff_id
    ):
        return JSONResponse(AccessDenied().model_dump_json(), 403)
    try:
        success = await StaffRepository.update_staff(staff_id, data)
        if success:
            return JSONResponse(EmptyResponse().model_dump_json(), 200)
        return JSONResponse(StaffNotFoundResponse().model_dump_json(), 404)
    except StaffAlreadyExistsError:
        return JSONResponse(StaffAlreadyExistsResponse().model_dump_json(), 409)


@staff_bp.delete("/<staff_id:uuid>")
@require_roles([RoleEnum.ADMIN, RoleEnum.ACADEMIC_STAFF, RoleEnum.PRINCIPAL])
async def delete_staff(request, staff_id: UUID):
    """Delete a staff member"""
    success = await StaffRepository.delete_staff(staff_id)
    if success:
        return JSONResponse(EmptyResponse().model_dump_json(), 200)
    return JSONResponse(StaffNotFoundResponse().model_dump_json(), 404)

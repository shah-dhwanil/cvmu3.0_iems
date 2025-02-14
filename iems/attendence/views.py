from uuid import UUID
from datetime import datetime
from iems.attendence.blueprint import attendence_bp
from iems.attendence.repository import AttendenceRepository
from iems.base.decorators import validate
from iems.base.response import JSONResponse
from iems.auth.decorators import require_roles
from iems.users.schemas import RoleEnum
from iems.auth.schemas import AccessDenied

from iems.attendence.schemas import MarkAttendence, UpdateAttendence, EmptyResponse


@attendence_bp.post("/mark")
@require_roles([RoleEnum.TEACHER,RoleEnum.ADMIN])
@validate(body=MarkAttendence)
async def mark_attendence(request, data: MarkAttendence, **_):
    await AttendenceRepository.mark_attendence(data)
    return JSONResponse(EmptyResponse().model_dump_json(), 200)


@attendence_bp.get("/course/<course_id:uuid>/<class_time:datetime>")
@require_roles([RoleEnum.TEACHER])
async def get_attendence_by_course_and_time(
    request, course_id: UUID, class_time: datetime, **_
):
    result = await AttendenceRepository.get_attendence_by_course_and_time(
        course_id, class_time
    )
    return JSONResponse(result.model_dump_json(), 200)


@attendence_bp.get("/student/<student_id:uuid>")
async def get_student_attendence(request, student_id: UUID, **_):
    if (
        request.ctx.user.role == RoleEnum.STUDENT
        and request.ctx.user.user_id != student_id
    ):
        return JSONResponse(AccessDenied().model_dump_json(), 403)

    result = await AttendenceRepository.get_attendence_by_student(student_id)
    return JSONResponse(result.model_dump_json(), 200)

@attendence_bp.get("/course/<course_id:uuid>/<student_id:uuid>")
async def get_student_attendence_by_course_id(request,course_id, student_id: UUID, **_):
    if (
        request.ctx.user.role == RoleEnum.STUDENT
        and request.ctx.user.user_id != student_id
    ):
        return JSONResponse(AccessDenied().model_dump_json(), 403)

    result = await AttendenceRepository.get_attendence_by_course_and_student_id(course_id, student_id)
    return JSONResponse(result.model_dump_json(), 200)



@attendence_bp.patch("/<attendence_id:uuid>")
@require_roles([RoleEnum.TEACHER])
@validate(body=UpdateAttendence)
async def update_attendence(request, attendence_id: UUID, data: UpdateAttendence, **_):
    if data.id != attendence_id:
        return JSONResponse({"error": "Path ID does not match body ID"}, 400)

    success = await AttendenceRepository.update_attendence(data)
    if not success:
        return JSONResponse(EmptyResponse().model_dump_json(), 404)
    return JSONResponse(EmptyResponse().model_dump_json(), 200)

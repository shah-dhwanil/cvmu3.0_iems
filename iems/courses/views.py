from uuid import UUID
from iems.courses.blueprint import courses_bp
from iems.courses.repository import CourseRepository
from iems.base.decorators import validate
from iems.base.response import JSONResponse
from iems.auth.decorators import require_roles
from iems.users.schemas import RoleEnum

from iems.courses.schemas import (
    CreateCourseRequest,
    CreateCourseResponse,
    CourseNotFoundResponse,
    GetCourseTaughtByResponse,
    UpdateCourseRequest,
    EmptyResponse,
)


@courses_bp.post("/")
@require_roles([RoleEnum.ADMIN, RoleEnum.PRINCIPAL,RoleEnum.ACADEMIC_STAFF])
@validate(body=CreateCourseRequest)
async def create_course(request, data: CreateCourseRequest, **_):
    course_id = await CourseRepository.create_course(data)
    return JSONResponse(CreateCourseResponse(id=course_id).model_dump_json(), 200)


@courses_bp.get("/<course_id:uuid>")
async def get_course(request, course_id: UUID, **_):
    course = await CourseRepository.get_course(course_id)
    if course is None:
        return JSONResponse(CourseNotFoundResponse().model_dump_json(), 404)
    return JSONResponse(course.model_dump_json(), 200)

@courses_bp.get("/teacher/<teacher_id:uuid>")
@require_roles([RoleEnum.ADMIN, RoleEnum.PRINCIPAL, RoleEnum.ACADEMIC_STAFF, RoleEnum.TEACHER])
async def get_course_by_teacher(request, teacher_id: UUID, **_):
    courses = await CourseRepository.get_course_by_teacher_id(teacher_id)
    return JSONResponse(GetCourseTaughtByResponse(courses=courses).model_dump_json(), 200)

@courses_bp.patch("/<course_id:uuid>")
@require_roles([RoleEnum.ADMIN, RoleEnum.PRINCIPAL,RoleEnum.ACADEMIC_STAFF])
@validate(body=UpdateCourseRequest)
async def update_course(request, course_id: UUID, data: UpdateCourseRequest, **_):
    success = await CourseRepository.update_course(course_id, data)
    if not success:
        return JSONResponse(CourseNotFoundResponse().model_dump_json(), 404)
    return JSONResponse(EmptyResponse().model_dump_json(), 200)


@courses_bp.delete("/<course_id:uuid>")
@require_roles([RoleEnum.ADMIN, RoleEnum.PRINCIPAL,RoleEnum.ACADEMIC_STAFF])
async def delete_course(request, course_id: UUID, **_):
    success = await CourseRepository.delete_course(course_id)
    if not success:
        return JSONResponse(CourseNotFoundResponse().model_dump_json(), 404)
    return JSONResponse(EmptyResponse().model_dump_json(), 200)
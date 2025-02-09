from uuid import UUID
from iems.auth.schemas import AccessDenied
from iems.base.response import JSONResponse
from iems.base.decorators import validate
from iems.users.exceptions import UserNotFoundException
from iems.users.schemas import RoleEnum, UserNotFoundResponse
from iems.auth.decorators import not_allowed_roles, require_roles
from iems.students.blueprint import student_bp
from iems.students.repository import StudentRepository
from iems.students.exceptions import StudentAlreadyExistsError

from iems.students.schemas import (
    CreateStudentRequest,
    UpdateStudentRequest,
    EmptyResponse,
    StudentAlreadyExistsResponse,
    StudentNotFoundResponse,
)


@student_bp.post("/")
@require_roles([RoleEnum.ADMIN, RoleEnum.ACADEMIC_STAFF, RoleEnum.PRINCIPAL])
@validate(body=CreateStudentRequest)
async def create_student(request, data: CreateStudentRequest, **_):
    """Create a new student"""
    try:
        await StudentRepository.create_student(data)
        return JSONResponse(EmptyResponse().model_dump_json(), 201)
    except StudentAlreadyExistsError:
        return JSONResponse(StudentAlreadyExistsResponse().model_dump_json(), 409)
    except UserNotFoundException:
        return JSONResponse(UserNotFoundResponse().model_dump_json(), 404)


@student_bp.get("/")
@not_allowed_roles([RoleEnum.STUDENT, RoleEnum.PARENTS])
async def get_all_students(request):
    """Get all students"""
    student_list = await StudentRepository.get_all_students()
    return JSONResponse(student_list.model_dump_json())


@student_bp.get("/<student_id:uuid>")
@not_allowed_roles([RoleEnum.STUDENT, RoleEnum.PARENTS])
async def get_student(request, student_id: UUID = None):
    """Get student by ID"""
    if (
        request.ctx.user.role == RoleEnum.STUDENT
        and request.ctx.user.user_id != student_id
    ):
        return JSONResponse(AccessDenied().model_dump_json(), 403)
    student = await StudentRepository.get_student(student_id)
    if student:
        return JSONResponse(student.model_dump_json(), 200)
    return JSONResponse(StudentNotFoundResponse().model_dump_json(), 404)


@student_bp.put("/<student_id:uuid>")
@require_roles(
    [RoleEnum.ADMIN, RoleEnum.ACADEMIC_STAFF, RoleEnum.PRINCIPAL, RoleEnum.STUDENT]
)
@validate(body=UpdateStudentRequest)
async def update_student(request, student_id: UUID, data: UpdateStudentRequest, **_):
    """Update a student"""
    if (
        request.ctx.user.role == RoleEnum.STUDENT
        and request.ctx.user.user_id != student_id
    ):
        return JSONResponse(AccessDenied().model_dump_json(), 403)
    try:
        success = await StudentRepository.update_student(student_id, data)
        if success:
            return JSONResponse(EmptyResponse().model_dump_json(), 200)
        return JSONResponse(StudentNotFoundResponse().model_dump_json(), 404)
    except StudentAlreadyExistsError:
        return JSONResponse(StudentAlreadyExistsResponse().model_dump_json(), 409)


@student_bp.delete("/<student_id:uuid>")
@require_roles([RoleEnum.ADMIN, RoleEnum.ACADEMIC_STAFF, RoleEnum.PRINCIPAL])
async def delete_student(request, student_id: UUID):
    """Delete a student"""
    success = await StudentRepository.delete_student(student_id)
    if success:
        return JSONResponse(EmptyResponse().model_dump_json(), 200)
    return JSONResponse(StudentNotFoundResponse().model_dump_json(), 404)

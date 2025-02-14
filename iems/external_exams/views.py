from uuid import UUID
from iems.auth.schemas import AccessDenied
from iems.external_exams.blueprint import external_exams_bp
from iems.external_exams.repository import ExternalExamRepository
from iems.base.decorators import validate
from iems.base.response import JSONResponse
from iems.auth.decorators import require_roles
from iems.users.schemas import RoleEnum

from iems.external_exams.schemas import (
    CreateExternalExamRequest,
    UpdateExternalExamRequest,
    ExternalExamNotFoundResponse,
    EmptyResponse,
)


@external_exams_bp.post("/")
@require_roles([RoleEnum.STUDENT])
@validate(body=CreateExternalExamRequest)
async def create_external_exam(request, data: CreateExternalExamRequest, **_):
    data.student_id = request.ctx.user.user_id
    exam_id = await ExternalExamRepository.create_external_exam(data)
    return JSONResponse(
        exam_id.model_dump_json(), 200
    )


@external_exams_bp.get("/<exam_id:uuid>")
async def get_external_exam(request, exam_id: UUID, **_):
    exam = await ExternalExamRepository.get_external_exam(exam_id)
    if exam is None:
        return JSONResponse(ExternalExamNotFoundResponse().model_dump_json(), 404)
    return JSONResponse(exam.model_dump_json(), 200)


@external_exams_bp.get("/student/<student_id:uuid>")
async def get_external_exams_by_student(request, student_id: UUID, **_):
    # if (
    #     request.ctx.user.role == RoleEnum.STUDENT
    #     and request.ctx.user.user_id != student_id
    # ):
    #     return JSONResponse(AccessDenied().model_dump_json(), 403)
    exams = await ExternalExamRepository.get_external_exams_by_student(student_id)
    return JSONResponse(exams.model_dump_json(), 200)


@external_exams_bp.patch("/<exam_id:uuid>")
@require_roles([RoleEnum.STUDENT])
@validate(body=UpdateExternalExamRequest)
async def update_external_exam(
    request, exam_id: UUID, data: UpdateExternalExamRequest, **_
):
    success = await ExternalExamRepository.update_external_exam(exam_id, data)
    if not success:
        return JSONResponse(ExternalExamNotFoundResponse().model_dump_json(), 404)
    return JSONResponse(EmptyResponse().model_dump_json(), 200)


@external_exams_bp.delete("/<exam_id:uuid>")
@require_roles([RoleEnum.STUDENT])
async def delete_external_exam(request, exam_id: UUID, **_):
    success = await ExternalExamRepository.delete_external_exam(exam_id)
    if not success:
        return JSONResponse(ExternalExamNotFoundResponse().model_dump_json(), 404)
    return JSONResponse(EmptyResponse().model_dump_json(), 200)
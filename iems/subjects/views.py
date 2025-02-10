from uuid import UUID
from iems.subjects.blueprint import subjects_bp
from iems.base.decorators import validate
from iems.base.response import JSONResponse
from iems.auth.decorators import require_roles
from iems.users.schemas import RoleEnum
from iems.subjects.repository import SubjectRepository

from iems.subjects.schemas import (
    CreateSubjectRequest,
    CreateSubjectResponse,
    GetAllSubjectsResponse,
    UpdateSubjectRequest,
    SubjectNotFoundResponse,
    EmptyResponse,
)


@subjects_bp.post("/")
@require_roles([RoleEnum.ADMIN, RoleEnum.PRINCIPAL, RoleEnum.ACADEMIC_STAFF])
@validate(body=CreateSubjectRequest)
async def create_subject(request, data: CreateSubjectRequest, **_):
    subject_id = await SubjectRepository.create_subject(data)
    return JSONResponse(CreateSubjectResponse(id=subject_id).model_dump_json(), 200)


@subjects_bp.get("/<subject_id:uuid>")
async def get_subject(request, subject_id: UUID, **_):
    subject = await SubjectRepository.get_subject(subject_id)
    if subject is None:
        return JSONResponse(SubjectNotFoundResponse().model_dump_json(), 404)
    return JSONResponse(subject.model_dump_json(), 200)


@subjects_bp.get("/")
async def get_all_subjects(request, **_):
    subjects = await SubjectRepository.get_all_subjects()
    return JSONResponse(
        GetAllSubjectsResponse(subjects=subjects).model_dump_json(), 200
    )


@subjects_bp.patch("/<subject_id:uuid>")
@require_roles([RoleEnum.ADMIN, RoleEnum.PRINCIPAL, RoleEnum.ACADEMIC_STAFF])
@validate(body=UpdateSubjectRequest)
async def update_subject(request, subject_id: UUID, data: UpdateSubjectRequest, **_):
    success = await SubjectRepository.update_subject(subject_id, data)
    if not success:
        return JSONResponse(SubjectNotFoundResponse().model_dump_json(), 404)
    return JSONResponse(EmptyResponse().model_dump_json(), 200)


@subjects_bp.delete("/<subject_id:uuid>")
@require_roles([RoleEnum.ADMIN, RoleEnum.PRINCIPAL, RoleEnum.ACADEMIC_STAFF])
async def delete_subject(request, subject_id: UUID, **_):
    success = await SubjectRepository.delete_subject(subject_id)
    if not success:
        return JSONResponse(SubjectNotFoundResponse().model_dump_json(), 404)
    return JSONResponse(EmptyResponse().model_dump_json(), 200)

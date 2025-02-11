from uuid import UUID
from iems.auth.schemas import AccessDenied
from iems.achievements.blueprint import achievements_bp
from iems.achievements.repository import AchievementRepository
from iems.base.decorators import validate
from iems.base.response import JSONResponse
from iems.auth.decorators import require_roles
from iems.users.schemas import RoleEnum

from iems.achievements.schemas import (
    CreateAchievementRequest,
    CreateAchievementResponse,
    UpdateAchievementRequest,
    AchievementNotFoundResponse,
    EmptyResponse,
)


@achievements_bp.post("/")
@require_roles([RoleEnum.STUDENT])
@validate(body=CreateAchievementRequest)
async def create_achievement(request, data: CreateAchievementRequest, **_):
    data.student_id = request.ctx.user.user_id
    achievement_id = await AchievementRepository.create_achievement(data)
    return JSONResponse(
        CreateAchievementResponse(id=achievement_id).model_dump_json(), 200
    )


@achievements_bp.get("/<achievement_id:uuid>")
async def get_achievement(request, achievement_id: UUID, **_):
    achievement = await AchievementRepository.get_achievement(achievement_id)
    if achievement is None:
        return JSONResponse(AchievementNotFoundResponse().model_dump_json(), 404)
    return JSONResponse(achievement.model_dump_json(), 200)


@achievements_bp.get("/student/<student_id:uuid>")
async def get_achievements_by_student(request, student_id: UUID, **_):
    if (
        request.ctx.user.role == RoleEnum.STUDENT
        and request.ctx.user.user_id != student_id
    ):
        return JSONResponse(AccessDenied().model_dump_json(), 403)
    achievements = await AchievementRepository.get_achievements_by_student(student_id)
    return JSONResponse(achievements.model_dump_json(), 200)


@achievements_bp.patch("/<achievement_id:uuid>")
@require_roles([RoleEnum.STUDENT])
@validate(body=UpdateAchievementRequest)
async def update_achievement(
    request, achievement_id: UUID, data: UpdateAchievementRequest, **_
):
    success = await AchievementRepository.update_achievement(achievement_id, data)
    if not success:
        return JSONResponse(AchievementNotFoundResponse().model_dump_json(), 404)
    return JSONResponse(EmptyResponse().model_dump_json(), 200)


@achievements_bp.delete("/<achievement_id:uuid>")
@require_roles([RoleEnum.STUDENT])
async def delete_achievement(request, achievement_id: UUID, **_):
    success = await AchievementRepository.delete_achievement(achievement_id)
    if not success:
        return JSONResponse(AchievementNotFoundResponse().model_dump_json(), 404)
    return JSONResponse(EmptyResponse().model_dump_json(), 200)

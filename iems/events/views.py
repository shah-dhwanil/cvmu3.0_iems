from uuid import UUID
from iems.auth.decorators import not_allowed_roles
from iems.events.blueprint import events_bp
from iems.events.repository import EventRepository
from iems.base.decorators import validate
from iems.base.response import JSONResponse

from iems.events.schemas import (
    CreateEventRequest,
    CreateEventResponse,
    GetAllEventsResponse,
    UpdateEventRequest,
    EventNotFoundResponse,
    EmptyResponse,
    GetEventResponse,
)
from iems.users.schemas import RoleEnum

@events_bp.post("/")
@validate(body=CreateEventRequest)
@not_allowed_roles([RoleEnum.STUDENT])
async def create_event(request, data: CreateEventRequest, **_):
    event_id = await EventRepository.create_event(data)
    return JSONResponse(CreateEventResponse(id=str(event_id)).model_dump_json(), 200)

@events_bp.get("/<event_id:uuid>")
async def get_event(request, event_id: UUID, **_):
    event = await EventRepository.get_event(event_id)
    if event is None:
        return JSONResponse(EventNotFoundResponse().model_dump_json(), 404)
    return JSONResponse(event.model_dump_json(), 200)

@events_bp.get("/")
async def get_all_events(request, **_):
    events = await EventRepository.get_all_events()
    return JSONResponse(GetAllEventsResponse(events=events).model_dump_json(), 200)

@events_bp.patch("/<event_id:uuid>")
@not_allowed_roles([RoleEnum.STUDENT])
@validate(body=UpdateEventRequest)
async def update_event(request, event_id: UUID, data: UpdateEventRequest, **_):
    success = await EventRepository.update_event(event_id, data)
    if not success:
        return JSONResponse(EventNotFoundResponse().model_dump_json(), 404)
    return JSONResponse(EmptyResponse().model_dump_json(), 200)

@events_bp.delete("/<event_id:uuid>")
@not_allowed_roles([RoleEnum.STUDENT])
async def delete_event(request, event_id: UUID, **_):
    success = await EventRepository.delete_event(event_id)
    if not success:
        return JSONResponse(EventNotFoundResponse().model_dump_json(), 404)
    return JSONResponse(EmptyResponse().model_dump_json(), 200)
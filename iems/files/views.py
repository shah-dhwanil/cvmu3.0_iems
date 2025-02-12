from json import dumps
from pathlib import Path
from uuid import UUID

from sanic import Request, html
from iems.base.postgres import PGConnection
from iems.base.response import JSONResponse
from iems.files.blueprint import files_bp
from sanic.response import file
from iems.files.repository import FilesRepository

@files_bp.get("/<uid:uuid>")
async def get_file(request, uid: UUID):
    response = await FilesRepository.get_file(uid)
    if response is None:
        return JSONResponse('{"message": "File not found"}', 404)
    path,file_name,file_type = response
    return await file(path, filename=file_name, mime_type=file_type)


@files_bp.route("/", methods=["POST"])
async def save_file(request:Request):
    files = request.files.getlist("file_upload")
    if files is None:
        return JSONResponse('{"message": "No file uploaded"}', 400)
    file = files[0]
    uid = await FilesRepository.save_file(file)
    return JSONResponse(dumps({"id":str(uid)}), 200)
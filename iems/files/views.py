from json import dumps
from pathlib import Path
from uuid import UUID

from sanic import Request, html
from iems.base.postgres import PGConnection
from iems.base.response import JSONResponse
from iems.files.blueprint import files_bp
from sanic.response import file

@files_bp.get("/<uid:uuid>")
async def get_file(request, uid: UUID):
    async with PGConnection.get_connection() as conn:
        record = await conn.fetchrow("SELECT * FROM files WHERE id = $1", uid)
        if not record:
            return JSONResponse('{"message": "File not found"}', 404)
        file_type = record["file_type"]
        file_name = record["file_name"]
        path = Path(f"./documents")
        path.mkdir(exist_ok=True)
        path = path.joinpath(f"{uid}")
    return await file(path, filename=file_name, mime_type=file_type)


@files_bp.route("/", methods=["POST"])
async def save_file(request:Request):
    files = request.files.getlist("file_upload")
    if files is None:
        return JSONResponse('{"message": "No file uploaded"}', 400)
    file = files[0]
    async with PGConnection.get_connection() as conn:
        uuid = await conn.fetchval(
            "INSERT INTO files (file_name, file_type) VALUES ($1, $2) RETURNING id",
            file.name,
            file.type
        )
        path = Path(f"./documents")
        path.mkdir(exist_ok=True)
        path = path.joinpath(f"{uuid}")
        path.write_bytes(file.body)
    return JSONResponse(dumps({"id":str(uuid)}), 200)
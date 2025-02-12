from pathlib import Path
from uuid import UUID
from iems.base.postgres import PGConnection


class FilesRepository:

    @staticmethod
    async def get_file(uid: UUID):
        async with PGConnection.get_connection() as conn:
            record = await conn.fetchrow("SELECT * FROM files WHERE id = $1", uid)
            if not record:
                return None
            file_type = record["file_type"]
            file_name = record["file_name"]
            path = Path(f"./documents")
            path.mkdir(exist_ok=True)
            path = path.joinpath(f"{uid}")
            return(path, file_name, file_type)
    @staticmethod
    async def save_file(file):
        async with PGConnection.get_connection() as conn:
            uid = await conn.fetchval(
                "INSERT INTO files (file_name, file_type) VALUES ($1, $2) RETURNING id",
                file.name,
                file.type
            )
            path = Path(f"./documents")
            path.mkdir(exist_ok=True)
            path = path.joinpath(f"{uid}")
            path.write_bytes(file.body)
        return uid
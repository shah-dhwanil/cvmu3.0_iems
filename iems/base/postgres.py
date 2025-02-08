from typing import Optional
from asyncpg import create_pool
from asyncpg import Pool, Connection
from uvloop import Loop
from iems.base.config import Config


class PGConnection:
    __pg_pool: Optional[Pool] = None

    @classmethod
    async def initiate(cls, loop: Loop):
        if not cls.__pg_pool:
            config = Config.get_config()
            cls.__pg_pool = await create_pool(
                config.POSTGRES_DSN,
                min_size=config.POSTGRES_MIN_CONN,
                max_size=config.POSTGRES_MAX_CONN,
                loop=loop,
            )

    @classmethod
    async def close(cls):
        if cls.__pg_pool is not None:
            await cls.__pg_pool.close()
            cls.__pg_pool = None

    @classmethod
    def get_connection(cls) -> Connection:
        if not cls.__pg_pool:
            raise ValueError(
                "Connection has not been setuped yet. Please setup the connection pool."
            )
        return cls.__pg_pool.acquire()

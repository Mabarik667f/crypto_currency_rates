import logging
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorClient
from pymongo.errors import CollectionInvalid
from core.config import settings


logger = logging.getLogger("cons")


async def init_db() -> tuple[AsyncIOMotorClient, AsyncIOMotorDatabase]:
    client = AsyncIOMotorClient(settings.MONGO_DB_URI)
    db = client.new_db
    ping = await db.command("ping")
    if int(ping["ok"]) != 1:
        raise Exception("ERROR connect")
    await db_struct_init(db)
    return client, db


async def db_struct_init(db: AsyncIOMotorDatabase) -> None:
    await create_collections(db)
    await create_indexes(db)


async def create_collections(db: AsyncIOMotorDatabase) -> None:
    try:
        await db.create_collection("coins")
    except CollectionInvalid:
        ...
    except Exception as e:
        logger.error(e)


async def create_indexes(db: AsyncIOMotorDatabase) -> None:
    pass

import logging
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorClient
from pymongo.errors import CollectionInvalid
from core.config import settings
from pymongo import IndexModel, ASCENDING


logger = logging.getLogger("cons")


async def init_db() -> tuple[AsyncIOMotorClient, AsyncIOMotorDatabase]:
    client = AsyncIOMotorClient(settings.MONGO_DB_URI)
    db = client[settings.MONGO_INITDB_DATABASE]
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
        await db.create_collection("accounts")
    except CollectionInvalid:
        ...
    except Exception as e:
        logger.error(e)


async def create_indexes(db: AsyncIOMotorDatabase) -> None:
    coin_index = IndexModel([("id", ASCENDING)], unique=True)
    try:
        async for i in db.coins.list_indexes():
            logger.info(i)
        await db.coins.create_indexes([coin_index])
    except Exception as e:
        logger.error(e)

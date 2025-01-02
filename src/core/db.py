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
    coin_indexes = IndexModel([("id", ASCENDING)], unique=True)
    account_indexes = IndexModel([("user_id", ASCENDING)], unique=True)
    try:
        await db.coins.create_indexes([coin_indexes])
        await db.accounts.create_indexes([account_indexes])
    except Exception as e:
        logger.error(e)

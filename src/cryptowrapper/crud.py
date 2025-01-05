from motor.motor_asyncio import AsyncIOMotorDatabase
from .schemas import BaseCoin
from .exceptions import CoinNotFoundError
from loguru import logger


async def insert_coins(db: AsyncIOMotorDatabase, coins: list[dict]):
    await db.coins.insert_many(coins, ordered=False)


async def get_coin_by_id(db: AsyncIOMotorDatabase, coin_id: str) -> dict:
    coin = await db.coins.find_one({"id": coin_id})
    if coin is None:
        raise CoinNotFoundError(field="coin_id", msg="Coin not found")
    return coin


async def get_coins_by_ids(
    db: AsyncIOMotorDatabase, coins_ids: list[str]
) -> list[dict]:
    coins = await db.coins.find({"id": {"$in": coins_ids}}).to_list()
    if not coins:
        raise CoinNotFoundError(field="coin_id", msg="Coins not found")
    return coins


async def get_all_coins(db: AsyncIOMotorDatabase) -> list[BaseCoin]:
    coins = await db.coins.find({}).to_list()
    if not coins:
        raise CoinNotFoundError(field="coin_id", msg="Coins not found")
    return coins


async def get_coins_by_query(
    db: AsyncIOMotorDatabase,
    query: str,
    limit: int = 5,
) -> list[BaseCoin]:
    coins = (
        await db.coins.find({"$text": {"$search": query}})
        .sort({"score": {"$meta": "textScore"}})
        .limit(limit)
        .to_list()
    )
    return (
        [BaseCoin(id=c["id"], name=c["name"], symbol=c["symbol"]) for c in coins]
        if coins
        else []
    )

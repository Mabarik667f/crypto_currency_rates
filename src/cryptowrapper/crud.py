from motor.motor_asyncio import AsyncIOMotorDatabase
from .schemas import BaseCoin
from .exceptions import CoinNotFoundError
from loguru import logger


async def insert_coins(db: AsyncIOMotorDatabase, coins: list[BaseCoin]):
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


async def update_observe_coins_for_user(
    db: AsyncIOMotorDatabase, coins: list[dict], user_id: str | int
) -> dict:
    observed_coins = [c["_id"] for c in coins]
    await db.accounts.find_one_and_update(
        {"user_id": str(user_id)}, {"$push": {"_id": {"$each": observed_coins}}}
    )

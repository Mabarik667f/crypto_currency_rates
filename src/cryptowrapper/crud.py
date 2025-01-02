from cryptowrapper.schemas import BaseCoin
from motor.motor_asyncio import AsyncIOMotorDatabase


async def insert_coins(db: AsyncIOMotorDatabase, coins: list[BaseCoin]):
    await db.coins.insert_many(coins, ordered=False)

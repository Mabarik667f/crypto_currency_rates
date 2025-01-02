from cryptowrapper.schemas import BaseCoin
from motor.motor_asyncio import AsyncIOMotorDatabase
from loguru import logger


async def insert_coins(db: AsyncIOMotorDatabase, coins: list[BaseCoin]):
    await db.coins.insert_many(coins, ordered=False)


async def set_all_data_about_coins(db: AsyncIOMotorDatabase):
    pass

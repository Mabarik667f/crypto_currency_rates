from motor.motor_asyncio import AsyncIOMotorDatabase
from cryptowrapper.crud import get_coin_by_id

async def observe_coin(db: AsyncIOMotorDatabase, coin_id: str):
    coin = await get_coin_by_id(db, coin_id)

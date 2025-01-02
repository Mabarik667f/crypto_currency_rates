import aiohttp
import asyncio
from core import settings
from loguru import logger
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo.errors import BulkWriteError
from .exceptions import CoinApiError
from .schemas import BaseCoin
from .crud import insert_coins


class BaseCoinsSet:

    def __init__(self, db: AsyncIOMotorDatabase) -> None:
        self.db = db

    async def set_coins(self) -> int:
        coins = await self._get_coins_list()
        return await self._write_base_coins(coins)

    @staticmethod
    async def _get_coins_list() -> list[BaseCoin]:
        async with aiohttp.ClientSession() as session:
            url = f"{settings.BASE_COINS_API}/coins/list"
            async with session.get(url, headers=settings.BASE_HEADERS) as r:
                body = await r.json()
                if not r.ok:
                    raise CoinApiError(field="coins", msg="CoinGecko api get error")
                return [BaseCoin(**c) for c in body]

    async def _write_base_coins(self, coins: list[BaseCoin]) -> int:
        tasks = [
            asyncio.create_task(insert_coins(self.db, coins[i : i + 500]))
            for i in range(0, len(coins), 500)
        ]
        for done in asyncio.as_completed(tasks):
            try:
                await done
            except BulkWriteError:
                ...
            except Exception as e:
                logger.info(type(e))
                logger.info(e)
        return len(coins)

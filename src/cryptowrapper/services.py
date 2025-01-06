import aiohttp
import asyncio
from core import settings
from circuitbreaker import circuit
from cryptowrapper.schemas import DescribedCoin
from loguru import logger
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo.errors import BulkWriteError
from .exceptions import CoinApiError
from .crud import insert_coins


class BaseCoinsSet:

    def __init__(self, db: AsyncIOMotorDatabase) -> None:
        self.db = db

    async def set_coins(self) -> int:
        coins = await self._get_coins_list()
        return await self._write_base_coins(coins)

    @staticmethod
    @circuit(failure_threshold=3, recovery_timeout=3, expected_exception=CoinApiError)
    async def _get_coins_list() -> list[dict]:
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{settings.BASE_COINS_API}/coins/list"
                async with session.get(url, headers=settings.BASE_HEADERS) as r:
                    body = await r.json()
                    if not r.ok:
                        raise CoinApiError(field="coins", msg="CoinGecko api get error")
                    return body
        except aiohttp.ClientError as e:
            raise CoinApiError(field="coins", msg=f"Aiohttp client error: {str(e)}")
        except Exception as e:
            raise CoinApiError(field="coins", msg=f"Unexpected error: {str(e)}")

    async def _write_base_coins(self, coins: list[dict]) -> int:
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
                logger.info(e)
        return len(coins)


class DescribedCoinsData:

    def __init__(
        self,
        db: AsyncIOMotorDatabase,
        coins_ids: list[str],
    ) -> None:
        self.db = db
        self.coins_ids = coins_ids
        self.url = f"{settings.BASE_COINS_API}/coins/markets"
        self.headers = settings.BASE_HEADERS

    async def get_coins_data(self) -> list[DescribedCoin]:
        async with aiohttp.ClientSession() as session:
            return await self.coins_market_data(session)

    @circuit(failure_threshold=3, recovery_timeout=3, expected_exception=CoinApiError)
    async def coins_market_data(
        self, session: aiohttp.ClientSession
    ) -> list[DescribedCoin]:
        params = {
            "vs_currency": "usd",
            "ids": ",".join(self.coins_ids),
            "price_change_percentage": "1h",
        }
        try:
            async with session.get(
                self.url, headers=self.headers, params=params
            ) as resp:
                if not resp.ok:
                    raise CoinApiError(field="coins", msg="CoinGecko api get error")
                body = await resp.json()
                return [DescribedCoin(**c) for c in body]
        except aiohttp.ClientError as e:
            raise CoinApiError(field="coins", msg=f"Aiohttp client error: {str(e)}")
        except Exception as e:
            raise CoinApiError(field="coins", msg=f"Unexpected error: {str(e)}")

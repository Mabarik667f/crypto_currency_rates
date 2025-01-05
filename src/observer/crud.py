from motor.motor_asyncio import AsyncIOMotorDatabase
from loguru import logger


class ObserverCrud:

    def __init__(self, db: AsyncIOMotorDatabase, user_id: str | int) -> None:
        self.db = db
        self.user_id = str(user_id)

    async def get_count_observed_coins(self) -> int:
        try:
            coins = await self.db.accounts.aggregate(
                [
                    {"$match": {"user_id": self.user_id}},
                    {"$addFields": {"size": {"$size": "$observedCoins"}}},
                    {"$group": {"_id": None, "coins_count": {"$sum": "$size"}}},
                ]
            ).__anext__()
            return coins["coins_count"]
        except StopAsyncIteration as e:
            logger.exception(e)
            return 0

    async def add_observed_coins(self, coins_ids: list[str]):
        await self.db.accounts.update_one(
            {"user_id": self.user_id},
            {"$push": {"observedCoins": {"$each": coins_ids}}},
        )

    async def del_observed_coins(self, coins_ids: list[str]):
        await self.db.accounts.update_one(
            {"user_id": self.user_id}, {"$pull": {"observedCoins": {"$in": coins_ids}}}
        )

    async def get_observed_coins(self) -> list[dict]:
        pipeline = [
            {"$match": {"user_id": self.user_id}},
            {
                "$lookup": {
                    "from": "coins",
                    "localField": "observedCoins",
                    "foreignField": "id",
                    "as": "observed_coins",
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "observed_coins": {
                        "$map": {
                            "input": "$observed_coins",
                            "as": "coin",
                            "in": {
                                "id": "$$coin.id",
                                "name": "$$coin.name",
                                "symbol": "$$coin.symbol",
                            },
                        }
                    },
                }
            },
        ]
        try:
            coins = await self.db.accounts.aggregate(pipeline).__anext__()
            return coins["observed_coins"]
        except StopAsyncIteration:
            return []

    async def clear_observe_coins(self) -> None:
        await self.db.accounts.update_one(
            {"user_id": self.user_id}, {"$set": {"observedCoins": []}}
        )

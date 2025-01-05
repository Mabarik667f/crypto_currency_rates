from motor.motor_asyncio import AsyncIOMotorDatabase
from accounts.schemas import MongoBaseUser
from cryptowrapper.crud import get_coins_by_ids
from cryptowrapper.exceptions import CoinNotFoundError
from cryptowrapper.schemas import BaseCoin
from observer.crud import ObserverCrud


class ObserverService:

    def __init__(self, db: AsyncIOMotorDatabase, user: MongoBaseUser) -> None:
        self.db = db
        self.user = user
        self.crud = ObserverCrud(db, user.user_id)

    # async def set_observe_for_coins(self, coins_ids: list[str]) -> list[BaseCoin]:
    #     try:
    #         coins = [c["id"] for c in await get_coins_by_ids(self.db, coins_ids)]
    #         #check
    #         ids = set(coins) | set(coins_ids)
    #         await self.crud.add_observed_coins(coins_ids)
    #         observed_coins = await self.crud.get_observed_coins()
    #         return [
    #             BaseCoin(id=c["id"], symbol=c["symbol"], name=c["name"])
    #             for c in observed_coins
    #         ]
    #     except CoinNotFoundError:
    #         return []

    async def del_observe_for_coins(self, coins_ids: list[str]) -> list[BaseCoin]:
        pass

    async def clear_observer(self) -> None:
        await self.crud.clear_observe_coins()

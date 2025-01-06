from cryptowrapper.services import DescribedCoinsData
from motor.motor_asyncio import AsyncIOMotorDatabase
from accounts.schemas import MongoBaseUser
from cryptowrapper.crud import get_coins_by_ids
from cryptowrapper.exceptions import CoinNotFoundError
from cryptowrapper.schemas import BaseCoin, DescribedCoin
from observer.crud import ObserverCrud
from observer.exceptions import ObserverLimitError
from loguru import logger


class ObserverService:

    def __init__(self, db: AsyncIOMotorDatabase, user: MongoBaseUser) -> None:
        self.db = db
        self.user = user
        self.crud = ObserverCrud(db, user.user_id)

    async def add_observe_for_coins(self, coins_ids: list[str]) -> list[BaseCoin]:
        try:
            coins_ids = await ObserverOpChecker(
                self.db,
                self.user,
            ).add_checker(coins_ids)
            await self.crud.add_observed_coins(coins_ids)
        except (CoinNotFoundError, ObserverLimitError) as e:
            logger.warning(e)
        finally:
            return await self.get_observed_coins()

    async def del_observe_for_coins(self, coins_ids: list[str]) -> list[BaseCoin]:
        try:
            coins_ids = await ObserverOpChecker(
                self.db,
                self.user,
            ).del_checker(coins_ids)
            await self.crud.del_observed_coins(coins_ids)
        except CoinNotFoundError as e:
            logger.warning(e)
        finally:
            return await self.get_observed_coins()

    async def get_observed_coins(self) -> list[BaseCoin]:
        observed_coins = await self.crud.get_observed_coins()
        return [
            BaseCoin(id=c["id"], symbol=c["symbol"], name=c["name"])
            for c in observed_coins
        ]

    async def get_describe_observed_coins(self) -> list[DescribedCoin]:
        observed_coins = await self.crud.get_observed_coins()
        if not observed_coins:
            return []
        return await DescribedCoinsData(
            self.db, [c["id"] for c in observed_coins]
        ).get_coins_data()

    async def clear_observer(self) -> None:
        await self.crud.clear_observe_coins()


class ObserverOpChecker:

    def __init__(
        self,
        db: AsyncIOMotorDatabase,
        user: MongoBaseUser,
    ) -> None:
        self.db = db
        self.user = user
        self.crud = ObserverCrud(db, user.user_id)

    async def del_checker(self, coins_ids: list[str]) -> list[str]:
        del_checker = ObserverDelChecker(self.db, self.user)
        coins_ids = await del_checker._check_coins_is_real(coins_ids)
        coins_ids = await del_checker._check_del_coins(coins_ids)
        return coins_ids

    async def add_checker(self, coins_ids: list[str]) -> list[str]:
        add_checker = ObserverAddChecker(self.db, self.user)
        coins_ids = await add_checker._check_coins_is_real(coins_ids)
        coins_ids = await add_checker._check_add_coins(coins_ids)
        return coins_ids

    async def _check_coins_is_real(self, coins_ids: list[str]) -> list[str]:
        real_coins_ids = [c["id"] for c in await get_coins_by_ids(self.db, coins_ids)]
        ids = list(set(coins_ids) & set(real_coins_ids))
        if not ids:
            raise CoinNotFoundError(field="coins_ids", msg="Haven't real coins!")
        return ids


class ObserverDelChecker(ObserverOpChecker):

    async def _check_del_coins(self, coins_ids: list[str]) -> list[str]:
        observed_coins = await self.crud.get_observed_coins()
        observed_ids = {c["id"] for c in observed_coins}
        ids = list(set(coins_ids) & observed_ids)
        if not ids:
            raise CoinNotFoundError(field="coins_ids", msg="No coins to delete")
        return ids


class ObserverAddChecker(ObserverOpChecker):

    async def _check_add_coins(self, coins_ids: list[str]) -> list[str]:
        observed_coins = await self.crud.get_observed_coins()
        observed_ids = {c["id"] for c in observed_coins}
        ids = list(set(coins_ids) - observed_ids)
        if not ids:
            raise CoinNotFoundError(field="coins_ids", msg="No coins to add")
        if len(ids) + len(observed_ids) > 10:
            raise ObserverLimitError(
                field="coins_ids", msg="You have exceeded the maximum limit"
            )
        return ids

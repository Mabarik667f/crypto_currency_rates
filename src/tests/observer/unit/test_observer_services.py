from accounts.schemas import MongoUser
from motor.motor_asyncio import AsyncIOMotorDatabase
from cryptowrapper.schemas import BaseCoin
from observer.crud import ObserverCrud
from observer.services import ObserverService
from loguru import logger


async def test_observe_coins(
    test_coins: list[BaseCoin], get_observer_service: ObserverService
):
    service = get_observer_service
    new_coins = ["bitcoin", "ethereum"]
    # await service.set_observe_for_coins(new_coins)
    # assert db.accounts.aggregator([
    #     {
    #         "$addFields": {
    #             "size": {
    #                 "$size": "$observedCoins"
    #             }
    #         }
    #     }
    # ])

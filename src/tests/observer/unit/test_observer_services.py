from accounts.schemas import MongoUser
from motor.motor_asyncio import AsyncIOMotorDatabase
from cryptowrapper.schemas import BaseCoin
from observer.crud import ObserverCrud
from observer.services import ObserverService
from loguru import logger


async def test_clear_observed_coins_service(
    get_observer_service: ObserverService, set_observed_coins
):
    service = get_observer_service
    crud = get_observer_service.crud

    cnt = await crud.get_count_observed_coins()
    assert cnt == 3

    await service.clear_observer()
    cnt = await crud.get_count_observed_coins()
    assert cnt == 0

    await service.clear_observer()
    cnt = await crud.get_count_observed_coins()
    assert cnt == 0


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

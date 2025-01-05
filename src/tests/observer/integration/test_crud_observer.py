from cryptowrapper.schemas import BaseCoin
from observer.crud import ObserverCrud
from loguru import logger


async def test_get_count_observed_coins(
    get_observer_crud: ObserverCrud, set_observed_coins
):
    crud = get_observer_crud
    cnt = await crud.get_count_observed_coins()
    assert cnt == 3


async def test_get_count_observed_coins_empty(
    get_observer_crud: ObserverCrud, test_coins: list[BaseCoin]
):
    crud = get_observer_crud
    cnt = await crud.get_count_observed_coins()
    assert cnt == 0


async def test_add_observed_coins(
    get_observer_crud: ObserverCrud, test_coins: list[BaseCoin]
):
    crud = get_observer_crud
    coins_ids = ["bitcoin", "ethereum"]
    await crud.add_observed_coins(coins_ids)
    cnt = await crud.get_count_observed_coins()
    assert cnt == 2

    coins_ids = ["aboba", "raven"]
    await crud.add_observed_coins(coins_ids)
    cnt = await crud.get_count_observed_coins()
    assert cnt == 4


async def test_get_observed_coins(get_observer_crud: ObserverCrud, set_observed_coins):
    crud = get_observer_crud
    coins = await crud.get_observed_coins()
    assert len(coins) == 2


async def test_clear_observed_coins(
    get_observer_crud: ObserverCrud, set_observed_coins
):
    crud = get_observer_crud
    await crud.clear_observe_coins()
    cnt = await crud.get_count_observed_coins()
    assert cnt == 0

    await crud.clear_observe_coins()
    cnt = await crud.get_count_observed_coins()
    assert cnt == 0


async def test_del_observed_coins(get_observer_crud: ObserverCrud, set_observed_coins):
    crud = get_observer_crud
    coins_ids = ["bitcoin", "bnb"]
    await crud.del_observed_coins(coins_ids)
    cnt = await crud.get_count_observed_coins()
    assert cnt == 1

    coins_ids = ["bitcoin"]
    await crud.del_observed_coins(coins_ids)
    cnt = await crud.get_count_observed_coins()
    assert cnt == 1

    coins_ids = ["ethereum"]
    await crud.del_observed_coins(coins_ids)
    cnt = await crud.get_count_observed_coins()
    assert cnt == 0

from observer.exceptions import ObserverLimitError
import pytest
from cryptowrapper.exceptions import CoinNotFoundError
from cryptowrapper.schemas import BaseCoin, DescribedCoin
from observer.services import ObserverOpChecker, ObserverService
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


async def test_get_observed_coins_service(
    get_observer_service: ObserverService, set_observed_coins
):
    service = get_observer_service
    coins = await service.get_observed_coins()
    assert len(coins) == 3
    assert isinstance(coins[0], BaseCoin)


async def test_del_checker_service(
    get_observer_op_checker: ObserverOpChecker, set_observed_coins
):
    checker = get_observer_op_checker
    del_coins = ["ethereum"]
    assert len(await checker.del_checker(del_coins)) == 1

    del_coins = ["ethereum", "bitcoin", "litecoin"]
    assert len(await checker.del_checker(del_coins)) == 3

    del_coins = ["ethereum", "bitcoin", "dasdadadada"]
    assert len(await checker.del_checker(del_coins)) == 2

    del_coins = ["dadaddaw32s"]
    with pytest.raises(CoinNotFoundError) as exc:
        await checker.del_checker(del_coins)
        assert exc.value == "Coins not found"

    del_coins = ["21x"]
    with pytest.raises(CoinNotFoundError) as exc:
        await checker.del_checker(del_coins)
        assert exc.value == "No coins to delete"


async def test_del_observed_coins_service(
    get_observer_service: ObserverService, set_observed_coins
):
    service = get_observer_service
    crud = service.crud

    del_coins = ["dsadada"]
    await service.del_observe_for_coins(del_coins)
    cnt = await crud.get_count_observed_coins()
    assert cnt == 3

    del_coins = ["ethereum", "dsadada"]
    await service.del_observe_for_coins(del_coins)
    cnt = await crud.get_count_observed_coins()
    assert cnt == 2

    del_coins = ["ethereum", "bitcoin"]
    await service.del_observe_for_coins(del_coins)
    cnt = await crud.get_count_observed_coins()
    assert cnt == 1

    del_coins = ["litecoin", "sdad"]
    await service.del_observe_for_coins(del_coins)
    cnt = await crud.get_count_observed_coins()
    assert cnt == 0


async def test_add_checker_service(
    get_observer_op_checker: ObserverOpChecker, set_observed_coins
):
    checker = get_observer_op_checker

    add_coins = ["0x", "16dao"]
    assert len(await checker.add_checker(add_coins)) == 2

    add_coins = ["0x", "16dao", "1ex", "1guy", "1sol", "2080", "20ex"]
    assert len(await checker.add_checker(add_coins)) == 7

    add_coins = ["ethereum", "bitcoin", "litecoin"]
    with pytest.raises(CoinNotFoundError) as exc:
        await checker.add_checker(add_coins)
        assert exc.value == "No coins to add"

    add_coins = ["dadaddaw32s"]
    with pytest.raises(CoinNotFoundError) as exc:
        await checker.add_checker(add_coins)
        assert exc.value == "Coins not found"

    add_coins = ["0x", "16dao", "1ex", "1guy", "1sol", "2080", "20ex", "21x"]
    with pytest.raises(ObserverLimitError) as exc:
        await checker.add_checker(add_coins)
        assert exc.value == "You have exceeded the maximum limit"


async def test_add_coins_service(
    get_observer_service: ObserverService, set_observed_coins
):
    service = get_observer_service
    crud = service.crud

    add_coins = ["ethereum", "dsadada"]
    await service.add_observe_for_coins(add_coins)
    cnt = await crud.get_count_observed_coins()
    assert cnt == 3

    add_coins = ["20ex", "21x", "dadadsdasda32s"]
    await service.add_observe_for_coins(add_coins)
    cnt = await crud.get_count_observed_coins()
    assert cnt == 5

    add_coins = ["0x", "16dao", "1ex", "1guy", "1sol", "2080", "20ex", "21x"]
    await service.add_observe_for_coins(add_coins)
    cnt = await crud.get_count_observed_coins()
    assert cnt == 5


async def test_described_observed_coins_service(
    get_observer_service: ObserverService, set_observed_coins
):
    service = get_observer_service
    crud = service.crud

    coins = await service.get_describe_observed_coins()
    assert len(coins) == 3
    assert isinstance(coins[0], DescribedCoin)

    await crud.clear_observe_coins()
    coins = await service.get_describe_observed_coins()
    assert len(coins) == 0

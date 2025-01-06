from cryptowrapper.schemas import DescribedCoin
from cryptowrapper.services import BaseCoinsSet, DescribedCoinsData
from loguru import logger

async def test_set_coins(mongo_test_data):
    client, db = mongo_test_data
    coins = [{"id": i} for i in range(17000)]
    res = await BaseCoinsSet(db)._write_base_coins(coins)  # type: ignore
    assert res == 17000

    coins = [{"id": i} for i in range(18000)]
    res = await BaseCoinsSet(db)._write_base_coins(coins)  # type: ignore
    assert res == 18000


async def test_described_coins_data(
    mongo_test_data,
    set_observed_coins
):
    _, db = mongo_test_data
    dcd = DescribedCoinsData(db, ["bitcoin", "ethereum"])
    coins = await dcd.get_coins_data()
    assert len(coins) == 2
    assert isinstance(coins[0], DescribedCoin)

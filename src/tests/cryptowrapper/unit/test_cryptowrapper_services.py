from cryptowrapper.services import BaseCoinsSet


async def test_set_coins(mongo_test_data):
    client, db = mongo_test_data
    coins = [{"id": i} for i in range(17000)]
    res = await BaseCoinsSet(db)._write_base_coins(coins)  # type: ignore
    assert res == 17000

    coins = [{"id": i} for i in range(18000)]
    res = await BaseCoinsSet(db)._write_base_coins(coins)  # type: ignore
    assert res == 18000

import pytest
from cryptowrapper.exceptions import CoinNotFoundError
from cryptowrapper.crud import insert_coins, get_coin_by_id, get_coins_by_ids
from loguru import logger


async def test_insert_coins(mongo_test_data):
    client, db = mongo_test_data
    test_data = [{"id": i} for i in range(500)]
    await insert_coins(db, test_data)  # type: ignore
    count = await db.coins.count_documents({})
    assert count == 500


async def test_get_coin_by_id(mongo_test_data):
    client, db = mongo_test_data
    await db.coins.insert_one({"id": "bitcoin"})
    coin_id = "bitcoin"
    coin = await get_coin_by_id(db, coin_id)

    assert coin["id"] == "bitcoin"
    coin_id = "adasdadasb321easda"
    with pytest.raises(CoinNotFoundError) as exc:
        await get_coin_by_id(db, coin_id)
    assert str(exc.value) == "Coin not found"


async def test_get_coins_by_ids(mongo_test_data):
    client, db = mongo_test_data
    await db.coins.insert_many([{"id": "bitcoin"}, {"id": "ethereum"}])
    coins_ids = ["bitcoin", "ethereum"]
    coins = await get_coins_by_ids(db, coins_ids)

    assert len(coins) == 2
    coins_ids[1] = "adasdadasb321easda"
    assert len(await get_coins_by_ids(db, coins_ids)) == 1

    coins_ids[0] = "dsadasdadada223f"
    with pytest.raises(CoinNotFoundError) as exc:
        coins = await get_coins_by_ids(db, coins_ids)
    assert str(exc.value) == "Coins not found"


async def test_observe_coins(mongo_test_data):
    pass


async def test_unobserve_coins(mongo_test_data):
    pass


async def test_clean_coins(mongo_test_data):
    pass
